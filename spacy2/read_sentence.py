"""
@Project   : text-classification-cnn-rnn
@Module    : read_sentence.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/31/18 2:02 PM
@Desc      :
!pip install spacy -i https://pypi.mirrors.ustc.edu.cn/simple
!python -m spacy download en_core_web_md
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import spacy

spacy.info()
spacy.info('en_core_web_md')
# /home/deco/miniconda2/envs/tf17/lib/python3.6/site-packages/en_core_web_md


def load_simple():
    # import en_core_web_md
    # nlp = en_core_web_sm.load()
    nlp = spacy.load('en_core_web_md')
    # nlp is a Language instance
    print('pipeline:', nlp.pipeline)
    print('pipe_names:', nlp.pipe_names)

    doc = nlp('Apple is looking at buying U.K. startup for $1 billion')
    # callable instance returning Doc instance
    print('tokens:')
    for token in doc:
        print(token.text)
    return doc


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

    doc = nlp.make_doc('This is a sentence')
    # create a Doc from raw text
    for name, proc in nlp.pipeline:  # iterate over components in order
        doc = proc(doc)  # apply each component
    print('token, pos and dependency parsing:')
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    return doc


def serial_func2(cls, st):
    res = [func(cls, st) for func
           in [pipeline_tagger_parser_ner, pipeline_tokenizer]]
    return res


def map_func_multi_thread(cls, st):
    funcs = [pipeline_tagger_parser_ner, pipeline_tokenizer]
    with ThreadPool(2) as p:
        res = p.map(lambda x: x(cls, st), funcs)
    return res


def map_func_multi_process(cls, st):
    funcs = [pipeline_tagger_parser_ner, pipeline_tokenizer]
    with Pool(2) as p:
        res = p.map(lambda x: x(cls, st), funcs)
    return res


def serial_func(cls, st):
    for func in [pipeline_tagger_parser_ner, pipeline_tokenizer]:
        func(cls, st)


def parallel_func(cls, st, executor):
    future = executor.submit(serial_func, cls, st)
    # print(future.result())
    return future.result()


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

    doc = nlp(st)
    print('tokens in pipeline_tagger_parser_ner:')
    # for token in doc:
    #     print(token.text)
    return 'tagger_parser_ner'


def pipeline_tokenizer(cls, st):
    nlp = cls()
    model_data_path = ('/home/deco/miniconda2/envs/tf17/lib/python3.6/'
                       'site-packages/en_core_web_md/en_core_web_md-2.0.0')
    nlp.from_disk(model_data_path)

    doc = nlp.make_doc(st)
    print('tokens in pipeline_tokenizer:')
    # for token in doc:
    #     print(token.text)
    return 'tokenizer'


def func_runtime(func, n_iter, *args):
    """[summary]

    Arguments:
        func {function object} -- the function to test
        n_iter {int} -- number of iterations

    Returns:
        str -- test result
    """

    start = time()
    for _ in range(n_iter):
        func(*args)
    runtime = (time() - start) / n_iter
    return "Average %.5fs in %d loops" % (runtime, n_iter)


if __name__ == '__main__':
    # load_simple()
    # load_pipeline()

    lang0 = 'en'
    cls0 = spacy.util.get_lang_class(lang0)
    # 1. get Language instance, e.g. English()
    st0 = 'This is a sentence'

    print('serial_func:')
    print(serial_func2(cls0, st0))
    print()

    multi_process = ProcessPoolExecutor()
    multi_thread = ThreadPoolExecutor()

    print('multi_thread:')
    print(map_func_multi_thread(cls0, st0))
    print()
    print(parallel_func(cls0, st0, multi_thread))
    print()

    print('multi_process:')
    print(parallel_func(cls0, st0, multi_process))
    print()
    # print(map_func_multi_process(cls0, st0))
    # print()

    print('func_runtime:')
    print(func_runtime(map_func_multi_thread, 2, cls0, st0))
    print()
    # print(func_runtime(map_func_multi_process, 2, cls0, st0))
    # print()
    print(func_runtime(serial_func, 2, cls0, st0))
    print()
    print(func_runtime(parallel_func, 10 ** 1, cls0, st0, multi_thread))
    print()
    print(func_runtime(parallel_func, 10 ** 1, cls0, st0, multi_process))
