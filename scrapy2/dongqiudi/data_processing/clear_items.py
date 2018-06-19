"""
@Project   : text-classification-cnn-rnn
@Module    : clear_items.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/19/18 11:03 AM
@Desc      : 
"""

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fn = os.path.join(base_dir, 'items.json')


if __name__ == '__main__':
    with open(fn, 'w', encoding='utf-8') as f:
        f.write('')
