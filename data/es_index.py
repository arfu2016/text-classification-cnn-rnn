"""
@Project   : text-classification-cnn-rnn
@Module    : es_index.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/30/18 11:56 AM
@Desc      : 
"""
# make sure ES is up and running
import requests
res = requests.get('http://localhost:9200')
print(res.content)

#connect to our cluster
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# let's iterate over swapi people documents and index them
import json

r = requests.get('http://localhost:9200')
i = 1
while r.status_code == 200:
    r = requests.get('http://swapi.co/api/people/' + str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    i = i + 1

print(i)


es.search(index="sw", body={"query": {"match": {'name': 'Darth Vader'}}})
