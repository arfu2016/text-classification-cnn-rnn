"""
@Project   : text-classification-cnn-rnn
@Module    : decision_tree_categorical_categorical.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/27/18 1:28 PM
@Desc      : 
"""
import numpy as np
from math import log2
from numpy.random import randint, seed
from scipy import stats

"""
1. function to calculate pk * log2pk
在后面计算信息熵时会用到该函数

求x趋于0时，xlnx的极限
令x=1/y;x（x>0）趋近于0等效为y趋近于正无穷；
xlnx=-lny/y;
令y=e^z;y趋近于正无穷等效于z趋近于正无穷；
xlnx=-lny/y=-z/e^z;
当z趋近于正无穷，e^z的增加要比z的增加快的多，所以z/e^z趋于0
"""


def fun(x):
    if x == 0:
        res = 0
    else:
        res = x * log2(x)
    return res


"""
2. function to calculate information entropy (not infomation gain)
"""


def info(Y):
    # Y是一个一维的numpy array, 长度是初始的长度，但只保留了固定的类别的值
    # 此处Y是二分类值，所以除了p_0就是p_1
    # 在对连续值进行分类时，一般也是做二分类的分割，因此也是除了p_0就是p_1
    p_1 = Y.sum() / Y.size
    # Y中的1所占的比例
    p_0 = 1 - p_1
    # Y中的0所占的比例

    res = - fun(p_0) - fun(p_1)
    # information entropy就是这样定义的
    return res


"""
3. function to calculate conditional information gain
"""


def condition_info(X, Y):
    low_rate = (X == 0).sum() / X.size
    # X中的元素低于split的比例，后来算加权平均的信息熵时要用到的权重
    high_rate = 1 - low_rate

    low_info = info(Y[np.where(X == 0)])
    # X < split所对应的Y的值
    high_info = info(Y[np.where(X == 1)])

    res = low_rate * low_info + high_rate * high_info
    # 加权平均计算分类后的信息熵

    return res


"""
4. function to calculate max gain with different split point of X
"""


def max_split_gain(X, Y):
    n = X.shape[1]
    # X有两列，X1和X2，所以n = 2
    info_Y = info(Y)
    max_gain = - float('inf')

    for i in range(n):
        gain = info_Y - condition_info(X[:, i], Y)
        # information gain for different splits
        if gain > max_gain:
            max_gain = gain
            max_split = i
        else:
            pass
    return max_split, max_gain


def mode_value(i, X, Y):
    return stats.mode(Y[X[:, i] == 0])[0][0], stats.mode(Y[X[:, i] == 1])


"""
test
"""
seed(10)
X = randint(0, 2, size=(100, 2))
Y = randint(0, 2, 100)
X[:, 1] = Y
X[0, 1] = 1 - Y[0]


max_split, max_gain = max_split_gain(X, Y)
print("%.2f" % info(Y))
print("%.2f" % condition_info(X[:, 1], Y))
print("%d" % max_split, "%.2f" % max_gain)
print(mode_value(1, X, Y))

from sklearn.tree import DecisionTreeClassifier

# X2 = np.array([[ele] for ele in X])
X2 = X

clf = DecisionTreeClassifier(criterion="entropy", max_depth=1)
# criterion: “entropy” for the information gain.
# max_depth: The maximum depth of the tree. If None, then nodes are expanded
# until all leaves are pure or until all leaves contain less than
# min_samples_split samples
# http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier.fit

clf.fit(X2, Y)
categories = clf.predict([[0, 1], [1, 0], [1, 1], [0, 0]])
print(categories)
