"""
@Project   : text-classification-cnn-rnn
@Module    : spacy_pipeline.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/29/18 4:24 PM
@Desc      : 
"""
import spacy


def my_component(doc):
    print("After tokenization, this doc has %s tokens." % len(doc))
    if len(doc) < 10:
        print("This is a pretty short document.")
    return doc


nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(my_component, name='print_info', first=True)
print(nlp.pipe_names)  # ['print_info', 'tagger', 'parser', 'ner']
doc = nlp(u"This is a sentence.")
