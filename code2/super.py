"""
@Project   : text-classification-cnn-rnn
@Module    : super.py
@Author    : Deco [deco@cubee.com]
@Created   : 8/3/18 4:24 PM
@Desc      : 
"""


class QuestionGraph:
    """Base class to construct graph queries, 模板，单个模板与一组问题的交互"""
    # module_name = None
    # template_name = None
    words_involved = None
    relations_involved = None
    targets_involved = None

    def __new__(cls, *args, **kwargs):
        cls.template_name = cls.__name__
        return super().__new__(cls)

    def __init__(self, data):
        super(QuestionGraph, self).__init__()
        self.templates = [question.question for question in data]
        self.words_relations = [[question.words, question.postags,
                                 question.arcs] for question in data]
        self.mapping_trees = None
        self.rule_trees = None


# def test0():
#     # 新式类
#     class A(object):
#         def __init__(self):
#             print('A')
#
#     class B(A):
#         def __init__(self):
#             super(B, self).__init__()
#             print('B')
#
#     class C(B, A):
#         def __init__(self):
#             super(C, self).__init__()
#             print('C')
#
#     c = C()


def test1():
    # MRO表
    class A:
        def __init__(self):
            print('A')

    class B(A):
        def __init__(self):
            super(B, self).__init__()
            print('B')

    class C(B, A):
        def __init__(self):
            super(C, self).__init__()
            print('C')

    c = C()


if __name__ == '__main__':
    # test0()
    test1()
