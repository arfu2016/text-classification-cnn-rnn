"""
@Project   : text-classification-cnn-rnn
@Module    : read_sentence2.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/1/18 5:33 PM
@Desc      : 
"""
import spacy


def load_pipeline():
    lang = 'en'
    cls = spacy.util.get_lang_class(lang)
    nlp = cls()
    pipeline = ['tagger', 'parser', 'ner']
    for name in pipeline:
        component = nlp.create_pipe(name)
        nlp.add_pipe(component)
    model_data_path = ('/home/deco/miniconda2/envs/tf17/lib/python3.6/'
                       'site-packages/en_core_web_md/en_core_web_md-2.0.0')
    nlp.from_disk(model_data_path)

    doc = nlp.make_doc('This is a sentence')
    # create a Doc from raw text, and another tokenizer can be put here
    for name, proc in nlp.pipeline:
        doc = proc(doc)
    print('token, pos and dependency parsing:')
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    return doc


def load_pipeline2():
    lang = 'en'
    cls = spacy.util.get_lang_class(lang)
    nlp = cls()
    pipeline = ['tagger', 'parser', 'ner']
    for name in pipeline:
        component = nlp.create_pipe(name)
        nlp.add_pipe(component)
    model_data_path = ('/home/deco/miniconda2/envs/tf17/lib/python3.6/'
                       'site-packages/en_core_web_md/en_core_web_md-2.0.0')
    nlp.from_disk(model_data_path)

    doc = nlp('This is a sentence')
    print('token, pos and dependency parsing:')
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    return doc


def load_pipeline3():
    lang = 'en'
    cls = spacy.util.get_lang_class(lang)
    nlp = cls()
    model_data_path = ('/home/deco/miniconda2/envs/tf17/lib/python3.6/'
                       'site-packages/en_core_web_md/en_core_web_md-2.0.0')
    nlp.from_disk(model_data_path)

    doc = nlp('This is a sentence')
    print('token:')
    for token in doc:
        print(token.text)
    return doc


if __name__ == '__main__':
    load_pipeline()
    load_pipeline2()
    load_pipeline3()
