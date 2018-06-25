"""
@Project   : text-classification-cnn-rnn
@Module    : bubble_sort.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/25/18 5:38 PM
@Desc      :
冒泡排序的原理，第一次遍历进行两两比较，找出最小值，第二次遍历找出次小值，注意刚才的最小
值不需参与比较……直至列表变为有序。网上的示例大多用两个for循环实现了降序排列，
笔者用for循环+while循环实现了升序排列，配以详尽的注释。注意，很多人写冒泡排序都会写错，
重点是内层循环和外层循环的遍历方向是反的。代码如下：
"""

# # 冒泡排序算法
# 1 自定义冒泡排序函数
def bubble_sort(A):
    l = len(A) #计算列表A的长度
    for i in range(1,l):
        # 外循环遍历列表，外循环从左向右，用for循环
        j = l-1
        while j >= i:
            # 内循环从右至左遍历到A[i]，用while循环
            key = A[j]#key起到传递A[j]的左右
            if A[j] < A[j-1]:  # 如果是反序，则交换
                # 如果A[j]比较小，就换到前面去
                # 因为用到j-1，所以i从1开始算起
                A[j] = A[j-1]
                A[j-1] = key
            j = j-1
    return A #返回排序后的列表A

# 2 对插入排序函数进行测试
x = [10,3,2,8,1,9,5,8,-1,-3]
x = bubble_sort(x)
print(x)

# bubble sort可以用来部分排序，比如只找最小值，就只有内循环，没有外循环，时间复杂度为O(n)
# 如果只找最小的k个值，时间复杂度为O(k*n)，如果完全排序，时间复杂度为O(n^2)
