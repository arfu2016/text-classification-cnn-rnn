"""
@Project   : text-classification-cnn-rnn
@Module    : lagrange_interpolation.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/21/18 2:52 PM
@Desc      :
https://zhuanlan.zhihu.com/p/31246238
https://zh.wikipedia.org/wiki/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E6%8F%92%E5%80%BC%E6%B3%95
<Python数据分析与挖掘实战>中提到对于平面上已知的n个点，可以构造一个n-1次多项式y来通过
这n个点
书中使用scipy包的lagrange函数，笔者试着自己实现了L(x)的计算如下
"""
import numpy as np
import scipy.interpolate
# you need to explicitly import the subpackage


#Lagrange interpolation method
def Lagrange(x,y,x0):
    n = len(x)
    Result = 0
    for i in range(n):
        ExcluXi = np.append(x[:i],x[(i+1):])
        #might waste memory if the input array is very large
        Numerator = (x0 - ExcluXi).prod()
        Denominator = (x[i] - ExcluXi).prod()
        Result += y[i] * Numerator / Denominator
    return Result


# test function, be careful with the test function when using pycharm
def random_seed(SeedX,SeedY,Size,):
    #generate 10 random numbers
    np.random.seed(seed = SeedY)
    y = np.random.uniform(low = 0, high = 100, size = Size)
    np.random.seed(SeedX)
    x = np.random.uniform(low = 0,high = 500, size = Size)
    return x,y


def scipy_lagrange(x_data, y_data, xx):
    xm = np.mean(x_data)
    xscale = np.std(x_data)
    ym = np.mean(y_data)
    yscale = np.std(y_data)
    x = (x_data - xm) / xscale
    y = (y_data - ym) / yscale
    poly = scipy.interpolate.lagrange(x, y)

    yy = poly((xx - xm) / xscale) * yscale + ym
    return yy


if __name__ == '__main__':

    # test1
    x,y = random_seed(10,100,100)
    Result = Lagrange(x,y,248)
    print(Result)
    print(scipy_lagrange(x, y, 248))

    # test2
    x = np.array([2,3])
    y = np.array([4,6])
    Result = Lagrange(x,y,7)
    print(Result)
    print(scipy_lagrange(x, y, 7))
