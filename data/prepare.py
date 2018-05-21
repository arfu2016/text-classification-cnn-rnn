"""
@Project   : text-classification-cnn-rnn
@Module    : prepare.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/21/18 2:52 PM
@Desc      : 
"""
import pickle
import os
import sys
import logging
import string
import random
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
    file_name = os.path.join(file_dir, 'raw/templates_intents.pkl')
    with open(file_name, 'rb') as f:
        ti = pickle.load(f)

    neg_label = {'no_idea', 'None', 'ask_back', 'promotion'}
    ti = [(tpl, intent)
          for tpl, intent in ti if intent not in neg_label]

    # logger.info('There are {} effective samples'.format(len(ti)))

    _, ti_intent = zip(*ti)

    intent_cnt = count_list(ti_intent)

    intent_num = intent_cnt.most_common(20)

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
    in_tab = string.punctuation + '。，“”‘’（）：；？·—《》、'
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
    class_num = 20
    random.seed(0)

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


def train_val_test(ti):
    train_xy, val_xy = train_test_split(ti, test_size=0.25, random_state=0)
    val_xy, test_xy = train_test_split(val_xy, test_size=0.5, random_state=0)
    return train_xy, val_xy, test_xy


def train_val_test2(ti):
    train_xy, val_xy = train_test_split(ti, test_size=0.25, random_state=0)
    val_xy, test_xy = train_test_split(val_xy, test_size=0.5, random_state=0)

    train_xy = random_compliment(train_xy, 200 * 20 * 0.75)
    val_xy = random_compliment(val_xy, 200 * 20 * 0.125)
    test_xy = random_compliment(test_xy, 200 * 20 * 0.125)

    return train_xy, val_xy, test_xy


def save_sample(ti, file_name):
    lines = [str(intent) + '\t' + tpl for tpl, intent in ti]
    sentences = '\n'.join(lines)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(sentences)


def save_vocab(vocab, file_name):
    vocab_list = list(vocab.keys())
    sentences = '\n'.join(vocab_list)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(sentences)


if __name__ == '__main__':
    data = load_raw()

    ii = intent_int = process_template_intent(data)
    # print('Intent dict:')
    # pprint.pprint(intent_int)
    # print()

    processed_data = sub_intent(data, ii)
    # print('Processed data:')
    # pprint.pprint(processed_data)
    # print()

    compliment_data = random_compliment(processed_data, 200)
    # print('Compliment data:')
    # pprint.pprint(compliment_data)
    # print()

    train_data, val_data, test_data = train_val_test(compliment_data)
    # print('Test data:')
    # pprint.pprint(test_data)
    # print()

    sample_vocab = create_vocab(processed_data)
    print('Vocab size:', len(sample_vocab))
    # print('Vocab:')
    # pprint.pprint(sample_vocab.most_common())
    # print()

    save_sample(train_data, os.path.join(file_dir, 'cnews/cnews.train.txt'))
    save_sample(val_data, os.path.join(file_dir, 'cnews/cnews.val.txt'))
    save_sample(test_data, os.path.join(file_dir, 'cnews/cnews.test.txt'))

    save_vocab(sample_vocab, os.path.join(file_dir, 'cnews/cnews.vocab.txt'))
