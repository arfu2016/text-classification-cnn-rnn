"""
@Project   : text-classification-cnn-rnn
@Module    : data_explore.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/22/18 11:13 AM
@Desc      : 
"""

import os
import sys
from collections import namedtuple

import pprint
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from data.prepare import (load_raw, process_template_intent, sub_intent)

Sample = namedtuple('Sample', 'template intent')


class ServerSamples:

    def __init__(self, ti):
        self._samples = [Sample(tpl, intent) for tpl, intent in ti]
        self.tpl_lengths = [len(sample.template) for sample in self._samples]

    def __len__(self):
        return len(self._samples)

    def __getitem__(self, position):
        return self._samples[position]

    def select_lengths(self, threshold):
        return [sample.template for sample in self._samples
                if len(sample.template) > threshold]


if __name__ == '__main__':
    data = load_raw()
    ii = intent_int = process_template_intent(data)
    processed_data = sub_intent(data, ii)
    # print('Processed data:')
    # pprint.pprint(processed_data)
    # print()

    samples = ServerSamples(processed_data)

    plt.hist(samples.tpl_lengths, bins='auto')
    # arguments are passed to np.histogram
    plt.title("Histogram with 'auto' bins")
    plt.show()

    large_template = samples.select_lengths(100)
    print('large_template:')
    pprint.pprint(large_template)
    print()
