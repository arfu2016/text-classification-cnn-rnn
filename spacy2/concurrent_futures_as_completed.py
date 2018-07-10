"""
@Project   : text-classification-cnn-rnn
@Module    : concurrent_futures_as_completed.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/10/18 6:12 PM
@Desc      : 
"""
import spacy
import time
from concurrent import futures


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


def parallel_func(cls, st):
    func_list = [serial_func, pipeline_tagger_parser_ner, pipeline_tokenizer]
    with futures.ProcessPoolExecutor(max_workers=2) as executor:
        to_do = []
        for func in func_list:
            future = executor.submit(func, cls, st)
            to_do.append(future)
            # time.sleep(0.001)
            msg = 'Scheduled for {}: {}'
            print(msg.format(func.__name__, future))

        time.sleep(2)
        print('to do list:', to_do)

        results = []
        for future in futures.as_completed(to_do, timeout=100):
            res = future.result()
            msg = '{} result: {}'
            print(msg.format(future, res))
            results.append(res)

        print('Is the with part blocked?')

    return len(results)


if __name__ == '__main__':

    lang0 = 'en'
    cls0 = spacy.util.get_lang_class(lang0)
    st0 = 'This is a sentence'

    parallel_func(cls0, st0)

    print('finished.')
