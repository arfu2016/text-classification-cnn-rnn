"""
@Project   : text-classification-cnn-rnn
@Module    : test_templates.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/31/18 10:09 AM
@Desc      : 
"""
import os
from collections import Counter
import pprint
import pandas as pd


def count_list(list_for_count):
    cnt = Counter()
    for item in list_for_count:
        cnt[item] += 1
    return cnt


def filter_template(filename):
    df = pd.read_csv(filename, sep='\t')
    df = df[['question', 'template', 'intent_name']]
    # tpl_intent = df.loc[:, ['question', 'template', 'intent_name']]
    neg_label = {'no_idea', 'None'}
    label_neg = [ele in neg_label for ele in df['intent_name'].values.tolist()]
    df = df.loc[label_neg]
    # df = df.loc[label_neg, :]
    # print('Shape:', df.shape)
    # print(df.iloc[0:10, :])
    tpl = df['template'].values.tolist()
    idx_tpl = [(idx, ele) for idx, ele in enumerate(tpl) if type(ele) is str]
    idx_tpl = [idx for idx, ele in idx_tpl if len(ele) > 0]
    df = df.iloc[idx_tpl, :]
    print('Shape:', df.shape)
    # print(df.iloc[0:10, :])
    qti = df[['question', 'template', 'intent_name']].values.tolist()
    t_list = [t for _, t, _ in qti]
    cnt = count_list(t_list)
    # print('Number of templates:', len(cnt))
    tpl_no_idea = [(tpl, num) for tpl, num in cnt.most_common() if num > 9]
    del tpl_no_idea[0]
    print('Number of templates:', len(tpl_no_idea))
    pprint.pprint(tpl_no_idea)


def filter_template_python(filename):
    df = pd.read_csv(filename, sep='\t')
    qti = df[['question', 'template', 'intent_name']].values.tolist()
    neg_label = {'no_idea', 'None'}
    t_list = [t for _, t, i in qti if i in neg_label]
    cnt = count_list(t_list)
    tpl_no_idea = [(tpl, num) for tpl, num in cnt.most_common() if num > 9]
    return tpl_no_idea


if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'raw/interact_log.csv')

    filter_template(fn)
