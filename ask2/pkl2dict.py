"""
@Project   : text-classification-cnn-rnn
@Module    : pkl2dict.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/11/18 1:25 PM
@Desc      : 
"""
import os
import pickle
import re


def design_regex():
    entitie_pattern = re.compile(r'{([A-Z0-9]*)}')
    return entitie_pattern


def construct_dict(entitie_pattern, ti):
    template, intent = ti
    entities = entitie_pattern.findall(template)
    # print('entities:', entities)
    info = {'template': template,
            'intent': intent,
            'entities': list(set(entities))}
    return info


if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)
    fn = os.path.join(file_dir, 'data/qti_ti.pkl')

    with open(fn, 'rb') as f:
        qti, template_intent = pickle.load(f)

    pattern = design_regex()
    template_intent_entity = map(
        lambda x: construct_dict(pattern, x), template_intent)
    template_intent_entity = list(template_intent_entity)
    for ti_dict in template_intent_entity:
        print(ti_dict)

    with open(os.path.join(file_dir, 'data/ti_dict.pkl'), 'wb') as f:
        pickle.dump(template_intent_entity, f)
