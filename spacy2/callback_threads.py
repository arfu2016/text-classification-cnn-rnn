"""
@Project   : text-classification-cnn-rnn
@Module    : callback_threads.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/11/18 1:25 PM
@Desc      : 
"""
import time
import spacy
from concurrent.futures import ThreadPoolExecutor


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


def produce_future3_callback(future):
    def future3_callback():
        print('future3 has results now.')
        print(future.result())

    return future3_callback


def future_callback(future):
    print('{} has results now.'.format(future))
    print('The return value is:', future.result())


def parallel_func(cls, st, executor):
    future = executor.submit(serial_func, cls, st)
    future2 = executor.submit(pipeline_tagger_parser_ner, cls, st)
    future3 = executor.submit(pipeline_tokenizer, cls, st)
    return future, future2, future3


def call_after_parallel(future, callback):
    future.add_done_callback(callback)


if __name__ == '__main__':

    multi_thread = ThreadPoolExecutor(2)

    lang0 = 'en'
    cls0 = spacy.util.get_lang_class(lang0)
    st0 = 'This is a sentence'

    future_res = parallel_func(cls0, st0, multi_thread)
    for future0 in future_res:
        call_after_parallel(future0, future_callback)

    time.sleep(1)
    print(future_res)

    time.sleep(40)
    print(future_res)

    print('finished.')
