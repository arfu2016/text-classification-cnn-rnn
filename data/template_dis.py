"""
@Project   : text-classification-cnn-rnn
@Module    : template_dis.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/29/18 1:13 PM
@Desc      : 
"""
import os
import pickle
from collections import Counter

import pprint


if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)

    with open(os.path.join(file_dir, 'raw/qti_ti.pkl'), 'rb') as f:
        qti, _ = pickle.load(f)

    # pprint.pprint(qti[0:10])

    complete_templates = [t for q, t, i in qti]

    cnt = Counter()
    for tpl in complete_templates:
        cnt[tpl] += 1

    asked_items = cnt.most_common()
    asked_items = [(t, count) for t, count in asked_items if count > 9]

    print('Number of useful templates:', len(asked_items))
    print()

    asked_items = [(t, count) for t, count in asked_items
                   if t not in {'需要', '{TEAM}死的'}]
    print('Number of useful templates:', len(asked_items))
    pprint.pprint(asked_items)
