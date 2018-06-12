"""
@Project   : text-classification-cnn-rnn
@Module    : dict2es.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/11/18 2:33 PM
@Desc      : 
"""
import os
import pickle
import json

import elasticsearch
from elasticsearch.helpers import bulk
import requests
import pprint

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])


def put_data(tpl_intent_entity):
    i = 1
    for tie in tpl_intent_entity:
        es.index(index='aiball', doc_type='template', id=i,
                 body=tie)
        if i % 200 == 0:
            print(i)
        i = i + 1


def set_data(tpl_intent_entity, index_name="aiball", doc_type_name="template"):
    """https://github.com/elastic/elasticsearch-py/issues/508"""
    for idx, tie in enumerate(tpl_intent_entity):
        yield {
            "_index": index_name,
            "_type": doc_type_name,
            "_id": idx,
            "_source": tie
        }


def bulk_put(tpl_intent_entity, **kwargs):
    success, _ = bulk(es, set_data(tpl_intent_entity, **kwargs))
    print("insert %s lines" % success)


def update_data():
    i = 1
    while i <= 20:
        update = {"doc": {"tpl_id": i}}
        es.update(index='aiball', doc_type='template', id=i,
                  body=update, version=1, version_type='internal')
        print(i)
        i = i + 1
    # Optimistic concurrency control: 解决并发矛盾问题


def update_data2():
    i = 1
    while i <= 20:
        update = {"script": "ctx._source.tpl_id+=1",
                  "upsert": {
                      "tpl_id": 0
                  }
                  }
        es.update(index='aiball', doc_type='template', id=i,
                  body=update)
        print(i)
        i = i + 1


def count_data():
    r = requests.get('http://localhost:9200/aiball/template/_count?pretty')
    pprint.pprint(json.loads(r.content))


def create_mapping():
    setting = {
        "mappings": {
            "template": {
                "properties": {
                    "entities": {
                        # "type": "text",
                        "type": "keyword",
                        "index": True
                    }
                }
            }
        }
    }
    es.indices.create(index='aiball', body=setting)
    # create mapping必须针对一个index，一个indix下所有的type都是相同的设置
    # 这也是elastic7.0准备去掉type的原因
    # storing different entities that have few or no fields in common in the
    # same index leads to sparse data and interferes with Lucene’s ability
    # to compress documents efficiently.


def dict2es():
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'data/ti_dict.pkl')

    with open(fn, 'rb') as f:
        template_intent_entity = pickle.load(f)

    for ele in template_intent_entity:
        ele.update({'entity_count': len(ele['entities'])})

    # pprint.pprint(template_intent_entity)

    create_mapping()

    # put_data(template_intent_entity)
    bulk_put(template_intent_entity)


def search_data0():
    res = requests.get(
        'http://localhost:9200/aiball/_search?q=PERSON&size=5&pretty')
    pprint.pprint(json.loads(res.content))


def search_data():
    # p5 = es.get(index='aiball', doc_type='template')
    # pprint.pprint(p5)
    res = requests.get(
        'http://localhost:9200/aiball/_search?size=5&from=10&pretty')
    # content_string = res.content.decode('utf-8')
    pprint.pprint(json.loads(res.content))


def search_data1():
    p5 = es.get(index='aiball', doc_type='template', id=1)
    pprint.pprint(p5)


def search_data2():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={"query": {"bool": {
                        "must": {"match": {"template": "{TEAM}的{PERSON}"}},
                        "filter": {"bool": {"must": [
                            {"term": {"entity_count": 2}},
                            {"term": {"entities": "PERSON"}},
                            {"term": {"entities": "TEAM"}},
                        ]}}}}})
    pprint.pprint(p)
    # {"term": {"entity_count": 1}}
    # {"match": {"entities": "PERSON"}
    # body = {"query": {"bool": {"must": [
    #     {"term": {"entity_count": 2}},
    #     {"term": {"entities": "PERSON"}},
    #     {"term": {"entities": "TEAM"}},
    # ]}}}
    # body = {"query": {"bool": {"filter": [
    #     {"term": {"entity_count": 2}},
    #     {"term": {"entities": "PERSON"}},
    #     {"term": {"entities": "TEAM"}},
    # ]}}}
    # body = {"query": {"bool": {"filter": {"bool": {"must": [
    #     {"term": {"entity_count": 2}},
    #     {"term": {"entities": "PERSON"}},
    #     {"term": {"entities": "TEAM"}},
    # ]}}}}}


def search_data3():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={"query": {"bool": {"filter": {"bool": {"must": [
                      {"term": {"template.keyword": "{TEAM}的{PERSON}"}},
                  ]}}}}})
    pprint.pprint(p)


def search_data4():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={"_source": ["intent", "template"],
                        "query": {"bool": {
                         "must": {"match": {"template": "{TEAM}的{PERSON}是谁"}},
                         "filter": {"bool": {"must": [
                          {"term": {"entity_count": 2}},
                          {"term": {"entities": "PERSON"}},
                          {"term": {"entities": "TEAM"}},
                         ]}}}}})
    pprint.pprint(p)


def search_data5():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={"_source": ["intent", "template"],
                        "query": {"bool": {"must": {
                         "more_like_this":
                         {"fields": ["template"],
                             "like": "{TEAM}的{PERSON}",
                             "min_term_freq": 1,  # "min_term_freq": 2,
                             "max_query_terms": 12}},
                         "filter": {"bool": {"must": [
                          {"term": {"entity_count": 2}},
                          {"term": {"entities": "PERSON"}},
                          {"term": {"entities": "TEAM"}},
                         ]}}}}})
    pprint.pprint(p)


def search_data6():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={"_source": ["intent", "template"],
                        "query": {"bool": {"must": {
                         "more_like_this":
                         {"fields": ["template"],
                             "like": ["教练", "主帅"],
                             "min_term_freq": 1,  # "min_term_freq": 2,
                             "max_query_terms": 12}},
                         "filter": {"bool": {"must": [
                          {"term": {"entity_count": 2}},
                          {"term": {"entities": "PERSON"}},
                          {"term": {"entities": "TEAM"}},
                         ]}}}}})
    pprint.pprint(p)


def search_data7():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={"_source": ["intent", "template"],
                        "query": {"bool": {"must": {
                         "more_like_this":
                         {"fields": ["template"],
                             "like": ["克韩", "可汗"],
                             "min_term_freq": 1,  # "min_term_freq": 2,
                             "max_query_terms": 12}},
                         }}})
    pprint.pprint(p)


def word_cloud():
    p = es.search(index="aiball",
                  doc_type="template",
                  body={
                            "aggs": {
                                "tagcloud": {
                                    "terms": {
                                        "field": "entities",
                                        "size": 10
                                    }
                                }
                            },
                         })
    pprint.pprint(p)


def del_aiball():
    es.indices.delete(index='aiball', ignore=[400, 404])


def view_mapping():
    pprint.pprint(es.indices.get_mapping(index='aiball'))


if __name__ == '__main__':

    # del_aiball()
    # dict2es()

    # try:
    #     update_data()
    # except elasticsearch.exceptions.ConflictError:
    #     # exceptions could be a module, and ConflictError is a class
    #     # in that module
    #     # exceptions could be a pacakge, ConflictError is a class
    #     # in the __init__.py of that package
    #     update_data2()

    # print('Search the _all filed:')
    # search_data0()

    # print('Samples from aiball/template:')
    # search_data()

    # print('Number of samples in aiball/template:')
    # count_data()
    # print('One sample from aiball/template:')
    # search_data1()

    # print('Mapping of aiball/template:')
    # view_mapping()

    # print('Approximate search for {TEAM}的{PERSON}:')
    # search_data2()
    # print('Exact search for {TEAM}的{PERSON}:')
    # search_data3()
    # print('Approximate search for {TEAM}的{PERSON}是谁:')
    # search_data4()

    print('More like this:')
    # search_data5()
    # search_data6()
    search_data7()

    print('Word cloud:')
    word_cloud()
