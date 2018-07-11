"""
@Project   : text-classification-cnn-rnn
@Module    : tqdm_example.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/11/18 3:05 PM
@Desc      : 
"""
import time
from tqdm import tqdm
for i in tqdm(range(1000)):
    time.sleep(.01)
