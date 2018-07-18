"""
@Project   : text-classification-cnn-rnn
@Module    : decorators.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/18/18 6:17 PM
@Desc      : 
"""

import threading


def synchronized(func):

    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return lock_func


def singleton(cls):
    """
    定义singleton装饰器，用于装饰类，构成单例类
    :param cls: 需要被装饰的类
    :return:
    """
    instances = {}

    @synchronized
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def singleton2(cls):
    """
    定义singleton装饰器，用于装饰类，构成单例类
    :param cls: 需要被装饰的类
    :return: 装饰一个类，返回一个函数，（用初始化类的参数）调用这个函数会生产类的对象（单例）
    把一个类变成了一个函数，这个函数又不能同时被两个线程调用，就保证了这个类的线程安全
    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    wrapper = synchronized(wrapper)

    return wrapper


if __name__ == '__main__':

    @singleton2
    class A:
        def __init__(self, x):
            self.x = x

    a = A(1)
    b = A(2)

    print(b.x)
