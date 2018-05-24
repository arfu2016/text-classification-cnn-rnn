"""
@Project   : text-classification-cnn-rnn
@Module    : load_csv.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/23/18 10:32 AM
@Desc      : 
"""
import pandas as pd
import os
import math
from collections import Counter

import pprint
import numpy as np
import pickle


def load_tpl_from_csv(filename):
    df = pd.read_csv(filename)
    tpl_list = df[['template_content', 'intention_id']].values.tolist()
    tpl_intent = []
    for tpl, intent in tpl_list:
        if intent == 0:
            tpl_intent.append([tpl, 1])
        else:
            tpl_intent.append([tpl, intent])
    return tpl_intent


def explore_csv(filename):
    df = pd.read_csv(filename, sep='\t')
    print('Type of columns.values:', type(df.columns.values))
    print('Table colunmn names:')
    pprint.pprint(df.columns.values.tolist())
    tpl_intent = df[['question', 'template', 'intent_name']].values.tolist()
    print('number of samples:', len(tpl_intent))
    print('Examples:')
    pprint.pprint(tpl_intent[0:10])
    print('Type of question column:', type(tpl_intent[0][0]))
    print('Type of template column:', type(tpl_intent[0][1]))
    print('Type of np.nan:', type(np.nan))
    print("Type of float('nan'):", type(float('nan')))
    print("float('nan'):", float('nan'))
    print('The first element of the first row:', tpl_intent[0][0])
    print('The second element of the first row:', tpl_intent[0][1])
    print('Check if np.nan is nan:', math.isnan(np.nan))
    print('Check if an element is nan:', math.isnan(tpl_intent[0][1]))


def large_file(filename):
    templates = []
    # for df in pd.read_csv(filename, sep='\t', header=None, chunksize=512):
    for df in pd.read_csv(filename, sep='\t', chunksize=512):
        tpl = df[['question']].values.tolist()
        templates.extend(tpl)
    print('number of questions:', len(templates))


def count_list(list_for_count):
    cnt = Counter()
    for item in list_for_count:
        cnt[item] += 1
    return cnt


def filter_intent(filename):
    df = pd.read_csv(filename, sep='\t')
    tpl_intent = df[['question', 'template', 'intent_name']].values.tolist()
    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if type(i) is str]
    tpl_intent = [(q, t, i) for q, t, i in tpl_intent if len(i) > 0]

    print('number of samples if intent is str:', len(tpl_intent))

    _, _, ti_intent = zip(*tpl_intent)
    intent_cnt = count_list(ti_intent)
    intent_num = intent_cnt.most_common()
    print('There are {} different intents'.format(len(intent_num)))
    print('Sample number of different intents:')
    pprint.pprint(intent_num)
    print()

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

    return qti, ti


if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'raw/interact_log.csv')

    # explore_csv(fn)
    # large_file(fn)

    qti_ti = filter_intent(fn)

    with open(os.path.join(file_dir, 'raw/qti_ti.pkl'), 'wb') as f:
        pickle.dump(qti_ti, f)
