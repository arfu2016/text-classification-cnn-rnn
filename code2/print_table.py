"""
@Project   : text-classification-cnn-rnn
@Module    : print_table.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/25/18 6:17 PM
@Desc      : 
"""

for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    # Note use of 'end' on previous line
    print(repr(x*x*x).rjust(4))

for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))

print('12'.zfill(5))
print('-3.14'.zfill(7))

print('This {food} is {adjective}.'.format(
    food='spam', adjective='absolutely horrible'))

# '!a' (apply ascii()), '!s' (apply str()) and '!r' (apply repr()) can be used
# to convert the value before it is formatted

contents = 'eels'
print('My hovercraft is full of {}.'.format(contents))
print('My hovercraft is full of {!r}.'.format(contents))

# An optional ':' and format specifier can follow the field name. This allows
# greater control over how the value is formatted. The following example rounds
# Pi to three places after the decimal.

import math
print('The value of PI is approximately {0:.3f}.'.format(math.pi))

# Passing an integer after the ':' will cause that field to be a minimum number
# of characters wide. This is useful for making tables pretty.
# 10的话是左对齐，10d的话是右对齐

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
for name, phone in table.items():
    print('{0:10} ==> {1:10d}'.format(name, phone))

print('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
      'Dcab: {0[Dcab]:d}'.format(table))

print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))
# This is particularly useful in combination with the built-in function vars(),
# which returns a dictionary containing all local variables.

# In text mode, the default when reading is to convert platform-specific line
# endings (\n on Unix, \r\n on Windows) to just \n. When writing in text mode,
# the default is to convert occurrences of \n back to platform-specific line
# endings. This behind-the-scenes modification to file data is fine for text
# files, but will corrupt binary data like that in JPEG or EXE files. Be very
# careful to use binary mode when reading and writing such files.

# If you’re not using the with keyword, then you should call f.close() to
# close the file and immediately free up any system resources used by it. If
# you don’t explicitly close a file, Python’s garbage collector will eventually
# destroy the object and close the open file for you, but the file may stay
# open for a while. Another risk is that different Python implementations will
# do this clean-up at different times.

# 'r+' opens the file for both reading and writing. The mode argument is
# optional; 'r' will be assumed if it’s omitted.

# It is also insecure by default: deserializing pickle data coming from an
# untrusted source can execute arbitrary code, if the data was crafted by a
# skilled attacker.
