"""
@Project   : text-classification-cnn-rnn
@Module    : spacy_multi_threading.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/29/18 5:46 PM
@Desc      : 
"""
import spacy


nlp = spacy.load('en_core_web_sm')

for doc in nlp.pipe(texts, batch_size=10000, n_threads=3):
   pass
