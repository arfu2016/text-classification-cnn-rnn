"""
@Project   : text-classification-cnn-rnn
@Module    : csv2pkl.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/11/18 10:41 AM
@Desc      : 
"""

import os
import string
import pickle
from collections import Counter

import pprint
import pandas as pd


def count_list(list_for_count):
    cnt = Counter()
    for item in list_for_count:
        cnt[item] += 1
    return cnt


def construct_pt():
    sp = string.punctuation
    sp = ''.join(p for p in sp if p not in {'{', '}', })
    # we could also use str.replace
    in_tab = sp + '。，“”‘’（）：；？·—《》【】、\n'
    pt = set(p for p in in_tab)
    return pt


def clean_sentence(pt, st: str) -> str:
    """
    数据预处理
    """
    clean = ''.join([c if c not in pt else '' for c in st])
    # hash search, time complexity m*O(1)
    clean = ''.join(clean.split())
    return clean


def filter_intent(filename):
    df = pd.read_csv(filename, sep='\t')
    tpl_intent = df[['question', 'template', 'intent_name']].values.tolist()
    print('number of samples in the csv:', len(tpl_intent))

    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if type(i) is str]
    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if len(i) > 0]

    print('number of samples if intent is unempty str:', len(tpl_intent))

    _, _, ti_intent = zip(*tpl_intent)
    intent_cnt = count_list(ti_intent)
    intent_num = intent_cnt.most_common()
    print('There are {} different intents'.format(len(intent_num)))
    print('Sample number of different intents:')
    pprint.pprint(intent_num)
    # print()

    neg_label = {'no_idea', 'None', 'ask_back', 'promotion', 'make_choice'}
    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if type(q) is str]
    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if len(q) > 0]
    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if i not in neg_label]
    print('number of samples if intent is not neg_label:', len(tpl_intent))

    qti = []
    question_set = set()
    for q, t, i in tpl_intent:
        if q not in question_set:
            qti.append((q, t, i))
            question_set.add(q)

    print('number of samples after removing duplicated questions:',
          len(qti))

    print('Samples of questions:')
    pprint.pprint(qti[0:10])

    ti = [(t, i) for q, t, i in qti if type(t) is str]
    ti = [(t, i) for t, i in ti if len(t) > 0]
    print('number of samples having no templates:', len(qti) - len(ti))

    ti = {t: i for t, i in ti if len(t) > 0}
    ti = list(ti.items())

    print('number of samples after removing duplicated templates:',
          len(ti))
    print('Samples of templates:')
    pprint.pprint(ti[0:10])

    punctuation = construct_pt()

    ti = {clean_sentence(punctuation, t): i for t, i in ti}
    ti = list(ti.items())

    print('number of samples after cleaning templates:',
          len(ti))
    print('Samples of templates:')
    pprint.pprint(ti[0:10])

    return qti, ti


if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'data/interact_log.csv')

    qti_ti = filter_intent(fn)

    with open(os.path.join(file_dir, 'data/qti_ti.pkl'), 'wb') as f:
        pickle.dump(qti_ti, f)
