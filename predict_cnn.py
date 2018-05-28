"""
@Project   : text-classification-cnn-rnn
@Module    : predict_cnn.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/28/18 1:32 PM
@Desc      : Intent classification by a cnn model
"""
import logging
import os
import pickle
import string
import sys

import tensorflow as tf
import tensorflow.contrib.keras as kr

base_dir = os.path.dirname(__file__)
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from run_cnn import (save_path, TCNNConfig, TextCNN,
                     vocab_dir, build_vocab, train_dir,
                     read_category, read_vocab)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
tf.logging.set_verbosity(tf.logging.ERROR)


def process_sentences(sentences, word_to_id, max_length=600):
    contents = sentences

    data_id = []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)

    return x_pad


def clean_sentence(st: str)-> str:
    """
    数据预处理
    """
    in_tab = string.punctuation + '。，“”‘’（）：；？·—《》【】、\n'
    pt = set(p for p in in_tab)
    clean = ''.join([c if c not in pt else ' ' for c in st])
    # hash search, time complexity m*O(1)
    return clean


class CnnClassifer:

    def __init__(self):
        self._set_logger()
        self._create_model()
        self._restore_model()
        file_dir = os.path.dirname(__file__)
        file_name = os.path.join(file_dir, 'data/raw/categories.pkl')
        with open(file_name, 'rb') as f:
            self.categories = pickle.load(f)

    def _set_logger(self):

        self.logger = logging.getLogger("intent_classify")
        # self.logger.setLevel(logging.ERROR)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def _create_model(self):
        config = TCNNConfig()
        if not os.path.exists(vocab_dir):  # 如果不存在词汇表，重建
            build_vocab(train_dir, vocab_dir, config.vocab_size)
        self.categories, self.cat_to_id = read_category()
        words, self.word_to_id = read_vocab(vocab_dir)
        config.vocab_size = len(words)

        self.model = TextCNN(config)
        self.config = config

    def _restore_model(self):
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        self.saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, sentences):
        sentences = [clean_sentence(st) for st in sentences]
        x_test = process_sentences(sentences,
                                   self.word_to_id,
                                   self.config.seq_length)
        feed_dict = {
            self.model.input_x: x_test,
            self.model.keep_prob: 1.0
        }

        pred_prob, pred_cls = self.session.run(
            [self.model.pred_prob, self.model.y_pred_cls], feed_dict=feed_dict)

        pred_prob = pred_prob.tolist()
        pred_cls = [self.categories[item] for item in pred_cls.tolist()]

        return pred_prob, pred_cls

    def predict_wrap(self, sentences):
        try:
            return self.predict(sentences)
        except Exception as e:
            self.logger.exception(e)


intent_classifier = CnnClassifer()
