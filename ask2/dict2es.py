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

from elasticsearch import Elasticsearch
import requests
import pprint

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def put_data(tpl_intent_entity):
    i = 1
    for tie in tpl_intent_entity:
        es.index(index='aiball', doc_type='template', id=i,
                 body=tie)
        if i % 200 == 0:
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


def dict2es():
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'data/ti_dict.pkl')

    with open(fn, 'rb') as f:
        template_intent_entity = pickle.load(f)

    for ele in template_intent_entity:
        ele.update({'entity_count': len(ele['entities'])})

    # pprint.pprint(template_intent_entity)

    create_mapping()

    put_data(template_intent_entity)


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
                  body={"query": {"bool": {
                      "must": {"match": {"template": "{TEAM}的{PERSON}是谁"}},
                      "filter": {"bool": {"must": [
                          {"term": {"entity_count": 2}},
                          {"term": {"entities": "PERSON"}},
                          {"term": {"entities": "TEAM"}},
                      ]}}}}})
    pprint.pprint(p)


def del_aiball():
    es.indices.delete(index='aiball', ignore=[400, 404])


def view_mapping():
    pprint.pprint(es.indices.get_mapping(index='aiball'))


if __name__ == '__main__':

    # del_aiball()

    # dict2es()

    # print('Number of samples in aiball/template:')
    # count_data()
    # print('One sample from aiball/template:')
    # search_data1()

    # print('Mapping of aiball/template:')
    # view_mapping()

    print('Approximate search for {TEAM}的{PERSON}:')
    search_data2()

    print('Exact search for {TEAM}的{PERSON}:')
    search_data3()

    print('Approximate search for {TEAM}的{PERSON}是谁:')
    search_data2()
