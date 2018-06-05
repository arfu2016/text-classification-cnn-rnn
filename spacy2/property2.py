"""
@Project   : text-classification-cnn-rnn
@Module    : property2.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/5/18 4:05 PM
@Desc      : https://www.python-course.eu/python3_properties.php
"""


class P:

    def __init__(self,x):
        self.x = x
        # 调用.x赋值时，实际是使用 @x.setter

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x


if __name__ == '__main__':
    p1 = P(1001)
    print(p1.x)
    p1.x = -12
    print(p1.x)
