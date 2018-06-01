"""
@Project   : text-classification-cnn-rnn
@Module    : entity_extract2.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/1/18 5:37 PM
@Desc      : 
"""

import random
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span


def retrain_entity(nlp, train_data):

    with nlp.disable_pipes(
            *[pipe for pipe in nlp.pipe_names if pipe != 'ner']):
        optimizer = nlp.begin_training()
        for i in range(10):
            random.shuffle(train_data)
            for text, annotations in train_data:
                nlp.update([text], [annotations], sgd=optimizer)
                # sgd is the optimizer option
    nlp.to_disk('/home/deco/Documents/spacy/model')
    return nlp


class EntityMatcher(object):
    name = 'entity_matcher'

    def __init__(self, nlp, terms, label):
        patterns = [nlp(text) for text in terms]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(label, None, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            doc.ents = list(doc.ents) + [span]
        return doc


def train_with_matcher(nlp, terms, entity):
    # terms = ('Uber',)
    # entity_matcher = EntityMatcher(nlp, terms, 'ORG')
    entity_matcher = EntityMatcher(nlp, terms, entity)

    nlp.add_pipe(entity_matcher, after='ner')
    print(nlp.pipe_names)  # the components in the pipeline
    return nlp


def train_matcher_text(nlp, raw_text):
    doc = nlp(raw_text)
    print([(ent.text, ent.start_char, ent.end_char, ent.label_)
           for ent in doc.ents])

    train_data = [
        (raw_text, {'entities': [(ent.start_char, ent.end_char, ent.label_)]})
        for ent in doc.ents]
    return train_data


def train_position_text(raw_text, entity, start_p, end_p):

    train_data = [
        (raw_text, {'entities': [(start_p, end_p, entity)]})]
    return train_data


def load_pipeline():
    lang = 'en'
    cls = spacy.util.get_lang_class(lang)
    # 1. get Language instance, e.g. English()
    nlp = cls()
    # 2. initialise it
    pipeline = ['tagger', 'parser', 'ner']
    for name in pipeline:
        component = nlp.create_pipe(name)
        # 3. create the pipeline components
        nlp.add_pipe(component)
        # 4. add the component to the pipeline
    model_data_path = ('/home/deco/miniconda2/envs/tf17/lib/python3.6/'
                       'site-packages/en_core_web_md/en_core_web_md-2.0.0')
    nlp.from_disk(model_data_path)

    nlp = train_with_matcher(nlp, ('Uber',), 'ORG')
    train_text = "Uber blew through $1 million"
    train_data = train_matcher_text(nlp, train_text)
    nlp = retrain_entity(nlp, train_data)

    return nlp


def process_text(nlp):

    doc = nlp('Uber is looking at buying U.K. startup for $1 billion')

    print('token, pos and dependency parsing, entity bio and entity type:')
    for token in doc:
        print(token.text, token.pos_, token.dep_,
              token.ent_iob_, token.ent_type_)

    print('entities:')
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

    for ent in doc.ents:
        ent.merge()
        # type(ent) is Span or a subclass of Span

    print('token, pos and dependency parsing, entity bio and entity type:')
    for token in doc:
        print(token.text, token.pos_, token.dep_,
              token.ent_iob_, token.ent_type_)

    return doc


if __name__ == '__main__':
    nlp0 = load_pipeline()
    process_text(nlp0)
