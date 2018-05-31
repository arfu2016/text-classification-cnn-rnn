"""
@Project   : text-classification-cnn-rnn
@Module    : LongestPalindromicSubstring.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/31/18 1:16 PM
@Desc      :
5. Longest Palindromic Substring

Given a string s, find the longest palindromic substring in s.
You may assume that the maximum length of s is 1000.

Example:

Input: "babad"

Output: "bab"

Note: "aba" is also a valid answer.


Example:

Input: "cbbd"

Output: "bb"
自己写的代码：

遍历字符串，从中间往两边查找，如果遇到字符不一致的情况则停止查找，跳入下一个字符串。
运行时间1262 ms

"""


class Solution:
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        n = len(s)
        res = ""
        for i, char in enumerate(s):
            tmp1 = tmp2 = ""
            #odd
            left = right = i
            while 1:
                if left is -1 or right == n or s[left] is not s[right]:
                    tmp1 = s[left+1:right]
                    break
                else:
                    left -= 1
                    right += 1
            #even
            left = i
            right = i + 1
            while 1:
                if left is -1 or right == n or s[left] is not s[right]:
                    tmp2 = s[left+1:right]
                    break
                else:
                    left -= 1
                    right += 1
            #compare odd and even str
            if len(tmp2) > len(tmp1):
                tmp = tmp2
            else:
                tmp = tmp1
            #compare res and tmp str
            if len(tmp) > len(res):
                res = tmp
        return res


'''
受讨论区启发后写的代码：

其实思路是一样的，但是用helper函数把代码变得更加简洁
'''


class Solution2:
    def longestPalindrome1(self, s):
        res = ""
        for i in range(len(s)):
            res = max(self.helper(s,i,i), self.helper(s,i,i+1), res, key=len)
        return res

    def helper(self,s,l,r):
        while 0<=l and r < len(s) and s[l]==s[r]:
                l-=1; r+=1
        return s[l+1:r]
