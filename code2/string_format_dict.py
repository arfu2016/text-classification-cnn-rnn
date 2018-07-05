"""
@Project   : text-classification-cnn-rnn
@Module    : string_format_dict.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/4/18 3:45 PM
@Desc      : 
"""

key_words = dict()
key_words['person'] = 'Messy'

print("Who is {person}".format(**key_words))
