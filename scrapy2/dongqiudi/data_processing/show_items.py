"""
@Project   : text-classification-cnn-rnn
@Module    : show_items.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/15/18 10:54 AM
@Desc      :
scrapy check basic
scrapy crawl basic -o items.json
"""
import json
import os

import pprint

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fn = os.path.join(base_dir, 'items.json')

if __name__ == '__main__':
    try:
        with open(fn, encoding='utf-8') as f:
            items = json.load(f)

        print('Number of items:', len(items))

        for item in items:
            pprint.pprint(item)
    except Exception as e:
        print('An exception has occurred -- {}'.format(e))
