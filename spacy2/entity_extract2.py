"""
@Project   : text-classification-cnn-rnn
@Module    : entity_extract2.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/1/18 5:37 PM
@Desc      : https://spacy.io/usage/training#ner
https://github.com/explosion/spaCy/blob/master/examples/training/train_ner.py
https://github.com/explosion/spacy/blob/master/examples/training/train_new_entity_type.py
"""

import random
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span


def retrain_entity(nlp, train_data, new_label=None):

    with nlp.disable_pipes(
            *[pipe for pipe in nlp.pipe_names if pipe != 'ner']):
        if new_label is not None:
            ner = nlp.get_pipe('ner')
            ner.add_label(new_label)
        optimizer = nlp.begin_training()
        for i in range(10):
            # range(10) could be fewer
            random.shuffle(train_data)
            for text, annotations in train_data:
                nlp.update([text], [annotations], drop=0.5, sgd=optimizer)
                # dropout - make it harder to memorise data
                # sgd is the optimizer option
    nlp.to_disk('/home/deco/Documents/spacy/model')

    # test the trained model
    for text, _ in train_data:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
    return nlp


class EntityMatcher(object):
    name = 'entity_matcher'

    def __init__(self, nlp, terms, label):
        self.nlp = nlp
        patterns = [nlp(text) for text in terms]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(label, None, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        print('before entity_mathcer:', [ent.text for ent in doc.ents])
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            print('span:', span.text)
            print(doc.ents)
            doc.ents = list(doc.ents) + [span]
            # a property setter is used here
            # 适用于span与之前的doc.ents没有重叠的情况，否则非常复杂
            # 当然，即使span与之前的doc.ents有重叠，也可以展示给用户，或者把这些抽出来
            # 的实体交给模型来训练，模型的预测结果不可能有实体的重叠
            # doc.ents = list(doc.ents)
            # print('type of doc.ents:', type(doc.ents))
            # doc.ents.append(span)
            print(doc.ents)
            print('ent.text', [ent.text for ent in doc.ents])
        print('after entity_mathcer:', [ent.text for ent in doc.ents])

        return doc

    def add(self, terms, label):
        patterns = [self.nlp(text) for text in terms]
        self.matcher.add(label, None, *patterns)


def train_with_matcher(nlp, terms_entity):
    # terms = ('Uber',)
    # entity_matcher = EntityMatcher(nlp, terms, 'ORG')

    for idx, (terms, entity) in enumerate(terms_entity):
        if idx == 0:
            entity_matcher = EntityMatcher(nlp, terms, entity)
        else:
            entity_matcher.add(terms, entity)
    if len(terms_entity) > 0:
        nlp.add_pipe(entity_matcher, after='ner')
        # print(nlp.pipe_names)  # the components in the pipeline
    return nlp


def train_matcher_text(nlp, raw_text):
    doc = nlp(raw_text)
    print('entities in raw text:', [(ent.text, ent.start_char,
                                     ent.end_char, ent.label_)
                                    for ent in doc.ents])
    # print(doc.ents)

    train_data = [
        (raw_text, {'entities': [(ent.start_char, ent.end_char, ent.label_)
         for ent in doc.ents]})]
    return train_data


def train_position_text(raw_text, entity_p):
    # print(entity_p)
    # temp = [(start_p, end_p, entity) for entity, start_p, end_p in entity_p]
    # print(temp)
    train_data = [
        (raw_text, {'entities': [(start_p, end_p, entity)
                                 for start_p, end_p, entity in entity_p]})]
    return train_data


def load_pipeline(remove_matcher=False):
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

    # nlp = train_with_matcher(nlp, [[('Uber',), 'ORG']])
    nlp = train_with_matcher(nlp, [[('Uber',), 'ORG'],
                                   [('blew', 'buying'), 'ACTION']])
    # entity_matcher is added
    train_text = "Uber blew through $1 million"
    print(1)
    train_data = train_matcher_text(nlp, train_text)
    print('train_data:', train_data)
    print(2)
    nlp = retrain_entity(nlp, train_data, 'ACTION')
    print(3)
    train_data = train_position_text('I am buying books', [(5, 11, 'ACTION')])
    nlp = retrain_entity(nlp, train_data)

    if remove_matcher:
        ner = nlp.get_pipe('ner')
        cls = spacy.util.get_lang_class(lang)
        nlp = cls()
        for name in ['tagger', 'parser']:
            component = nlp.create_pipe(name)
            nlp.add_pipe(component)
        nlp.from_disk(model_data_path)
        nlp.add_pipe(ner)

    return nlp


def modify_ner_model(nlp):
    train_data = train_position_text('Uber blew through $1 million',
                                     [(0, 4, 'ORG'), (18, 28, 'MONEY')])
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
    # nlp0 = load_pipeline(remove_matcher=False)
    nlp0 = load_pipeline(remove_matcher=True)
    print('nlp0:', nlp0.pipe_names)  # the components in the pipeline
    nlp1 = modify_ner_model(nlp0)
    print('nlp1:', nlp1.pipe_names)
    process_text(nlp1)
