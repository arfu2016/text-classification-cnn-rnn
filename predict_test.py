"""
@Project   : text-classification-cnn-rnn
@Module    : predict_test.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/28/18 2:25 PM
@Desc      : 
"""
import os
import sys

base_dir = os.path.dirname(__file__)
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import predict_cnn


if __name__ == '__main__':
    sts = ['讲一讲 PERSON 的基本情况',
           '能给说一说 TEAM 吗',
           '',
           ]

    pred_prob, pred_cls = predict_cnn.intent_classifier.predict_wrap(sts)

    for i, st in enumerate(sts):
        print("question -- {}:".format(st))
        print("category: {}; ".format(pred_cls[i]),
              "probability: {}".format(pred_prob[i]))
