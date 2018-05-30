"""
@Project   : text-classification-cnn-rnn
@Module    : spacy_sentence_segmentation.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/29/18 5:10 PM
@Desc      : 
"""
import spacy


def sbd_component(doc):
    for i, token in enumerate(doc[:-2]):
        # define sentence start if period + titlecase token
        if token.text == '.' and doc[i+1].is_title:
            doc[i+1].sent_start = True
    return doc


nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(sbd_component, before='parser')  # insert before the parser
doc = nlp(u"This is a sentence. This is another sentence.")
for sent in doc.sents:
    print(sent.text)
