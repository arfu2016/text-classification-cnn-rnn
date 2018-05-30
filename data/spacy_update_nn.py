"""
@Project   : text-classification-cnn-rnn
@Module    : spacy_update_nn.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/30/18 10:32 AM
@Desc      : 
"""
import spacy
import random

nlp = spacy.load('en')
train_data = [("Uber blew through $1 million", {'entities': [(0, 4, 'ORG')]})]

with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != 'ner']):
    optimizer = nlp.begin_training()
    for i in range(10):
        random.shuffle(train_data)
        for text, annotations in train_data:
            nlp.update([text], [annotations], sgd=optimizer)
nlp.to_disk('/model')
