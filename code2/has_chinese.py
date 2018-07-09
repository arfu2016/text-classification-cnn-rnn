"""
@Project   : text-classification-cnn-rnn
@Module    : has_chinese.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/5/18 4:49 PM
@Desc      : 
"""
import re


def has_chinese(text: str) -> bool:
    """
    判断输入字符串是否包含中文
    :param text: 输入字符串
    :return: True包含中文，False不包含中文
    """
    pattern = re.compile(r".*[\u4e00-\u9fa5].*")
    return True if pattern.match(text) else False
