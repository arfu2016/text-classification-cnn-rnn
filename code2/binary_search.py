"""
@Project   : text-classification-cnn-rnn
@Module    : binary_search.py
@Author    : Deco [deco@cubee.com]
@Created   : 8/2/18 11:20 AM
@Desc      : 
"""

from bisect import bisect_left


def index(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    print(i)
    raise ValueError("No {} in {}".format(x, a))


if __name__ == '__main__':
    print(index([1, 2, 3], 0))
