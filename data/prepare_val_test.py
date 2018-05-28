"""
@Project   : text-classification-cnn-rnn
@Module    : prepare_val_test.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/25/18 10:09 AM
@Desc      : 
"""
import pickle
import os
import sys
import logging
import string
import random
import pickle
from collections import Counter

import pprint
from sklearn.model_selection import train_test_split

file_dir = os.path.dirname(__file__)


def set_logger():
    # for logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    return logger


def count_list(list_for_count):
    cnt = Counter()
    for item in list_for_count:
        cnt[item] += 1
    return cnt


def load_raw():
    logger = set_logger()
    file_name = os.path.join(file_dir, 'raw/qti_ti.pkl')
    with open(file_name, 'rb') as f:
        _, ti = pickle.load(f)

    # logger.info('There are {} effective samples'.format(len(ti)))

    _, ti_intent = zip(*ti)

    intent_cnt = count_list(ti_intent)

    intent_num = intent_cnt.most_common(30)

    logger.info('There are {} different intents'.format(len(intent_num)))

    print('Sample number of different intents:')
    pprint.pprint(intent_num)
    print()

    _, top_number = zip(*intent_num)
    logger.info('There are {} top samples'.format(sum(top_number)))

    top_dict = dict(intent_num)

    samples_top = [(tpl, intent) for tpl, intent in ti if intent in top_dict]

    return samples_top


def process_template_intent(ti):
    _, ti_intent = zip(*ti)
    counts = Counter(ti_intent)
    intents = sorted(counts, key=counts.get, reverse=True)
    intent_to_int = {word: ii for ii, word in enumerate(intents, 1)}

    return intent_to_int


def create_vocab(ti):
    vocab = Counter()
    for tpl, _ in ti:
        for cha in tpl.strip():
            vocab[cha] += 1
    vocab['<PAD>'] += 1
    return vocab


def clean_sentence5(st):
    """
    数据预处理
    :param st: string
    :return: string
    """
    in_tab = string.punctuation + '。，“”‘’（）：；？·—《》【】、\n'
    pt = set(p for p in in_tab)
    clean = ''.join([c if c not in pt else ' ' for c in st])
    # hash search, time complexity m*O(1)
    return clean


def sub_intent(ti, intent_to_int):
    ti = [(clean_sentence5(tpl), intent_to_int[intent]) for tpl, intent in ti]
    return ti


def random_compliment(tpl_intent, sample_size):
    logger = set_logger()

    # sample_size = 200
    class_num = 30
    # random.seed(0)

    ti = []

    for i in range(1, class_num+1):

        specific_class = [(tpl, intent)
                          for tpl, intent in tpl_intent if intent == i]

        # class_samples = random.choices(specific_class, k=sample_size)

        class_samples = [random.choice(specific_class)
                         for _ in range(sample_size)]

        ti.extend(class_samples)

    logger.info("There are {} random samples".format(len(ti)))

    return ti


if __name__ == '__main__':
    data = load_raw()

    ii = intent_int = process_template_intent(data)
    intent_int2 = sorted(intent_int.items(), key=lambda x: x[1])
    print('Intent dict:')
    pprint.pprint(intent_int2)
    print()

    processed_data = sub_intent(data, ii)

    compliment_data = random_compliment(processed_data, 2)
    print('Val and test samples:')
    pprint.pprint(compliment_data)
    print()

    categories, _ = zip(*intent_int2)
    print('Categories:')
    pprint.pprint(categories)
    print()

    file_name = os.path.join(file_dir, 'raw/categories.pkl')
    with open(file_name, 'wb') as f:
        pickle.dump(categories, f)
