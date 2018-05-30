"""
@Project   : text-classification-cnn-rnn
@Module    : median_of_two_sorted_arrays.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/29/18 6:41 PM
@Desc      :
4. Median of Two Sorted Arrays

There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity
should be O(log (m+n)).

Example 1:

nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:

Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5
"""
'''
第一版算法复杂度O(n)

两个列表结尾都append一个正无穷作为哨兵，这样就不需要判断列表是否为空。从i=0开始，
不停地将两个列表首个元素的较小者pop出来，直到i=两个数组总长度的一半为止。
判断总长度是奇数还是偶数，返回结果。运行时间205 ms。
'''


class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        a = len(nums1)
        b = len(nums2)
        k = 0
        n, m = divmod(a + b, 2)
        nums1.append(float('inf'))
        nums2.append(float('inf'))
        for i in range(n):
            if nums1[0] < nums2[0]:
                k = nums1.pop(0)
            else:
                k = nums2.pop(0)

        res = min(nums1[0], nums2[0])
        if m is 0:
            res = (k + res) / 2
        return res


'''
第二版算法复杂度O(logn)

两个列表结尾都append一个正无穷作为哨兵，首部append一个负无穷作为哨兵。
利用二分查找的思想寻找数组1的标号，根据两个数组总长度的一半减去数组1的标号i1
得到数组2的标号i2。满足nums1[i1] < nums2[i2+1]且nums2[i2] < nums1[i1+1]时循环停止。
运行时间205 ms。
'''


class Solution2:
    def findMedianSortedArrays(self, nums1, nums2):
        nums1.append(float('inf'))
        nums2.append(float('inf'))
        nums1.insert(0, -float('inf'))
        nums2.insert(0, -float('inf'))

        l1, l2 = len(nums1), len(nums2)
        n, odd = divmod(l1 + l2, 2)
        low = 0
        high = l1 - 1

        while low <= high:
            # 本质上就是二分查找，只是，在数组1中找的不是确定的值，而是数组1和数组2的中位数，
            # 于是就用到了下面的二分查找办法，看这个中位数到底在哪里
            i1 = (low + high) // 2
            i2 = n - i1 - 2
            if i2 < -1:
                high = i1 - 1
            elif i2 > l2 - 1:
                low = i1 + 1
            elif i2 is not l2 - 1 and nums1[i1] > nums2[i2+1]:
                high = i1 - 1
            elif i2 is not -1 and nums2[i2] > nums1[i1+1]:
                low = i1 + 1
            else:
                break
        if odd:
            res = min(nums1[i1+1], nums2[i2+1])
        else:
            res = (max(
                nums1[i1], nums2[i2]) + min(nums1[i1+1], nums2[i2+1])) / 2
        return res
