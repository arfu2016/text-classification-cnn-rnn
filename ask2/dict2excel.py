"""
@Project   : text-classification-cnn-rnn
@Module    : dict2excel.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/13/18 10:26 AM
@Desc      : 
"""
import os
import pickle

import pandas as pd


def dict2excel():
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'data/ti_dict.pkl')

    with open(fn, 'rb') as f:
        template_intent_entity = pickle.load(f)

    t_value = [item['template'] for item in template_intent_entity]
    i_value = [item['intent'] for item in template_intent_entity]
    df = pd.DataFrame({'template': t_value, 'intent': i_value},
                      columns=['template', 'intent'])

    df.to_excel(os.path.join(file_dir, 'data/tpl_intent.xlsx'),
                sheet_name='Sheet1', header=True, index=False)


if __name__ == '__main__':
    dict2excel()
