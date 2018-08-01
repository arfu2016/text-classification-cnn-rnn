"""
@Project   : text-classification-cnn-rnn
@Module    : test_sequence.py
@Author    : Deco [deco@cubee.com]
@Created   : 8/1/18 11:25 AM
@Desc      : 
"""
from collections import Sequence
from collections import Container
from collections import Collection
import random
import json
import pickle

a_list = list()
len(a_list)
b = a_list[0] if len(a_list) > 0 else None

print(isinstance(a_list, Sequence))
print(isinstance(a_list, Collection))
print(isinstance(a_list, Container))

a_set = set()

print(isinstance(a_set, Collection))
print(isinstance(a_set, Container))

a_list = list('abc')
a_set = set('abc')

print(random.choice(a_list))
try:
    print(random.choice(a_set))
except Exception as e:
    print('Error message: {}'.format(e))

b_list = [1, 2, 4, 3]
print(list(reversed(b_list)))

a = [1, 2, 3]
d = [4, 5, 6]
c = a + d
print(a)

a_string = 'bar'
print(str(a_string))
print(repr(a_string))
print(json.dumps(a_string))
print(pickle.dumps(a_string))
print(a_string.encode('utf-8'))

print(a_string)
print(eval(repr(a_string)))
print(json.loads(json.dumps(a_string)))
print(pickle.loads(pickle.dumps(a_string)))
print(a_string.encode('utf-8').decode('utf-8'))

print(isinstance(str(a_string), str))
print(isinstance(repr(a_string), str))
print(isinstance(json.dumps(a_string), str))
print(isinstance(pickle.dumps(a_string), bytes))
print(isinstance(a_string.encode('utf-8'), bytes))

(m, n) = (1, 2)
m1, n1 = [1, 2]
m0, n0 = 1, 2
(m2, n2) = [1, 2]
[m3, n3] = [1, 2]

a, b, *rest = range(5)
print(rest)

a, b, *rest = range(3)
print(rest)
