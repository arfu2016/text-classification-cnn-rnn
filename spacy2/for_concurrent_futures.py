"""
@Project   : text-classification-cnn-rnn
@Module    : for_concurrent_futures.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/10/18 1:37 PM
@Desc      : 
"""
import spacy
from concurrent.futures import ProcessPoolExecutor


def pipeline_tagger_parser_ner(cls, st):
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
    # 5. load in the binary data

    doc = nlp.make_doc(st)
    print('tokens in pipeline_tagger_parser_ner:')
    print([token.text for token in doc])
    return 'tagger_parser_ner'


def pipeline_tokenizer(cls, st):
    nlp = cls()
    model_data_path = ('/home/deco/miniconda2/envs/tf17/lib/python3.6/'
                       'site-packages/en_core_web_md/en_core_web_md-2.0.0')
    nlp.from_disk(model_data_path)

    doc = nlp.make_doc(st)
    print('tokens in pipeline_tokenizer:')
    print([token.text for token in doc])
    return 'tokenizer'


def serial_func(cls, st):
    for func in [pipeline_tagger_parser_ner, pipeline_tokenizer]:
        func(cls, st)


def parallel_func(cls, st, executor):
    future = executor.submit(serial_func, cls, st)
    # future.result()


if __name__ == '__main__':

    multi_process = ProcessPoolExecutor()

    lang0 = 'en'
    cls0 = spacy.util.get_lang_class(lang0)
    st0 = 'This is a sentence'

    parallel_func(cls0, st0, multi_process)

    print('finished.')
