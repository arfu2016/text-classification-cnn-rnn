"""
@Project   : text-classification-cnn-rnn
@Module    : spacy_preprocess.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/29/18 12:00 PM
@Desc      : 
"""
import spacy

nlp = spacy.load('en_core_web_sm')
# !python -m spacy download en_core_web_lg
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
for token in doc:
    print(token.text)


nlp = spacy.load('en_core_web_md')  # make sure to use larger model!
tokens = nlp(u'dog cat banana')

for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))
