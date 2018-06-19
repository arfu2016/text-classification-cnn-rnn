"""
@Project   : text-classification-cnn-rnn
@Module    : add_dongqiudi.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/15/18 4:53 PM
@Desc      : 
"""
import os
import json
import sys
import logging

import elasticsearch
from elasticsearch.helpers import bulk
import requests
import pprint

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])


def put_data(tpl_intent_entity):
    i = 1
    for tie in tpl_intent_entity:
        es.index(index='dongqiudi', doc_type='news', id=i,
                 body=tie)
        if i % 200 == 0:
            print(i)
        i = i + 1


def set_data(list_data_dict, index_name="dongqiudi", doc_type_name="news"):
    """https://github.com/elastic/elasticsearch-py/issues/508"""

    for data_dict in list_data_dict:
        yield {
            "_index": index_name,
            "_type": doc_type_name,
            "_source": data_dict
        }

    # for idx, data_dict in enumerate(list_data_dict):
    #     yield {
    #         "_index": index_name,
    #         "_type": doc_type_name,
    #         "_id": idx,
    #         "_source": data_dict
    #     }


def bulk_put(tpl_intent_entity, **kwargs):
    success, _ = bulk(es, set_data(tpl_intent_entity, **kwargs))
    print("insert %s lines" % success)


def construct_query(list_data_dict):

    search_arr = []

    for data_dict in list_data_dict:
        # req_head
        search_arr.append({'index': 'dongqiudi', 'type': 'news'})
        # req_body
        search_arr.append({"query": {"bool": {"filter": {"bool": {"must": [
                      {"term": {"title.keyword": data_dict['title'][0]}},
                  ]}}}}})

    request = ''
    for each in search_arr:
        request += '%s \n' % json.dumps(each)

    return request


def check_existence(list_data_dict):
    res = es.msearch(body=construct_query(list_data_dict))
    # pprint.pprint(res)
    return [item['hits']['total'] for item in res['responses']]


def test_check_existence():
    file_dir = os.path.dirname(os.path.dirname(__file__))
    fn = os.path.join(file_dir, 'scrapy2/dongqiudi/items.json')
    with open(fn, 'r', encoding='utf-8') as f:
        list_news_dict = json.load(f)

    tags = check_existence(list_news_dict)
    list_news_dict = [news_dict for idx, news_dict in enumerate(list_news_dict)
                      if tags[idx] == 0]
    # print('list_news_dict in test_check_existence():')
    # pprint.pprint(list_news_dict)

    bulk_put(list_news_dict)


def dict2es():
    file_dir = os.path.dirname(os.path.dirname(__file__))
    fn = os.path.join(file_dir, 'scrapy2/dongqiudi/items.json')
    with open(fn, 'r', encoding='utf-8') as f:
        list_news_dict = json.load(f)

    bulk_put(list_news_dict)


def search_data():
    res = requests.get(
        'http://localhost:9200/dongqiudi/_search?size=5&from=10&pretty')
    pprint.pprint(json.loads(res.content))


def count_data():
    logger = set_logger()
    r = requests.get('http://localhost:9200/dongqiudi/_count?pretty')
    info = json.loads(r.content)
    pprint.pprint(info)
    logger.info(
        'There are {} records in dongqiudi index'.format(info['count']))


def set_logger():
    # for logging

    log_path = 'logs/dongqiudi.txt'  # ''

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def del_dongqiudi():
    es.indices.delete(index='dongqiudi', ignore=[400, 404])


if __name__ == '__main__':
    # del_dongqiudi()

    # dict2es()

    # search_data()

    # count_data()

    test_check_existence()
