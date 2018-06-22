"""
@Project   : text-classification-cnn-rnn
@Module    : insertion_sort.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/22/18 1:10 PM
@Desc      : https://zhuanlan.zhihu.com/p/31645345
插入排序的原理非常简单，就像码扑克牌一样，让N个待排序的元素中的k个元素成为有序的序列，
然后将第k+1个元素插入到这k个元素中，如此反复从k=1直至n个元素全部有序。
用python实现代码如下，写了比较详细的代码注释，没用过Python的朋友应该也能看懂。
另外，列表在Python中属于可变对象，实际上不写返回值也可以达到排序的目的。
"""
"""
Created on Thu Feb  2 12:26:27 2017

@author: liuzimu
"""


# # 插入排序算法
# 1 自定义插入排序函数
def insertion_sort(A):
    l = len(A)
    for i in range(1,l): #遍历列表，注意在python中第一个元素是A[0]
        key = A[i] #key用于传递数据，起中间人的角色
        j = i-1 #A[j]代表A[i]左侧的第一个元素
        while A[j] > key and j>=0: #遍历A[i]左侧的元素，j为负会导致计算错误
            A[j+1] = A[j] #交换数据的位置
            A[j] = key #交换数据的位置
            j = j-1
    return A #返回排序后的列表A


# 2 对插入排序函数进行测试
x = [8,3,-9,11,6,5,6]
x = insertion_sort(x)
print(x)
