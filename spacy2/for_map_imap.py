"""
@Project   : text-classification-cnn-rnn
@Module    : for_map_imap.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/30/18 4:49 PM
@Desc      : 
"""

import spacy
from multiprocessing import Pool


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


class RunPipeline:

    def __init__(self, cls, st):
        self.cls = cls
        self.st = st

    def __call__(self, func):
        return func(self.cls, self.st)


def map_func_multi_process(cls, st):
    funcs = [pipeline_tagger_parser_ner, pipeline_tokenizer]
    with Pool(2) as p:
        res = p.imap(RunPipeline(cls, st), funcs)
        # res.wait()
        # asyncronization, blocking with res.wait()
        # nonblocking without res.wait(), but session.run() will not
        # be executed
        # return res
        # not working, res must be executed before return
        for item in res:  # 用next或in可以驱动iterator的session.run()的调用
            # pass
            # print(item)
            yield item


if __name__ == '__main__':

    lang0 = 'en'
    cls0 = spacy.util.get_lang_class(lang0)
    st0 = 'This is a sentence'

    # map_func_multi_process(cls0, st0)

    for value in map_func_multi_process(cls0, st0):
        pass
    # 对于generator，用next或in可以驱动generator的session.run()的调用

    print('finished.')
