"""
@Project   : text-classification-cnn-rnn
@Module    : hash.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/25/18 8:07 PM
@Desc      : 
"""
import hashlib


def md5(source: str) -> str:
    """计算一个字符串的md5码，输出md5字符串"""
    return hashlib.md5(str(source).encode("utf-8")).hexdigest()
