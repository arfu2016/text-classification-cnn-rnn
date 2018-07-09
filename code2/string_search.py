"""
@Project   : text-classification-cnn-rnn
@Module    : string_search.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/5/18 5:07 PM
@Desc      : 
"""

"""
自然语言处理相关函数
"""
import hashlib
import os
import re

import jieba
# jieba.load_userdict(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))) +
#     "/data/userdict.txt"
# )
# from jieba import posseg


# 中间的多余空白
ptn_mult_blank = re.compile("[\s]{2,}")
# 开头的标点符号
ptn_start_puncts = re.compile(
    "^[!\"#$%&\'()*+,-\./:;<=>\?@\[\]^_`{|}~—！，？、￥…（）：“”-《》【】；〜～︶·]+")
# 多余标点符号
ptn_mult_puncts = re.compile(
    "[!\"#$%&\'()*+,-\./:;<=>\?@\[\]^_`{|}~—！，。？、￥…（）：“”-《》【】；〜～︶·]{2,}")
# 最后的标点符号
end_puncts = set("!#$%&(*+,-./\:;<=>?@[^_`{|~—！，？、￥…（：“-《【；〜～︶´·¯°﹏＜＞")


def has_chinese(text: str) -> bool:
    """
    判断输入字符串是否包含中文
    :param text: 输入字符串
    :return: True包含中文，False不包含中文
    """
    pattern = re.compile(r".*[\u4e00-\u9fa5].*")
    return True if pattern.match(text) else False


def kmp_locs(sentence, string, kmp_val):
    """
    拿string在sentence里面进行比对，找出string在sentence里面的位置。
    返回：
    1. sentence里面包含string：[(start0, end0), (start1, end1), ...]；
    2. 如果sentence里面没有该string：[].
    """
    len_sent = len(sentence)
    len_str = len(string)
    locs = []
    idx = 0
    while len_sent - idx >= len_str:
        for i in range(len_str):
            if string[i] != sentence[idx+i]:
            # b = sentence[idx+i]
            # a = string[i]
            # if a != b:
                break
        else:
            locs.append((idx, idx + len_str))

        idx += 1 if i == 0 else i - kmp_val[i-1]

    return locs


def kmp_value(sentence):
    """计算用于kmp算法的部分匹配值"""
    def prefix_and_suffix_list(sent):
        prefix_list = [sent[0:i] for i in range(len(sent))]
        prefix_list = [c for c in prefix_list if c]     # 去掉空字符
        suffix_list = [sent[i+1:] for i in range(len(sent))]
        suffix_list = [c for c in suffix_list if c]     # 去掉空字符
        return prefix_list, suffix_list

    val = []
    for i in range(1, len(sentence)+1):
        prefix_list, suffix_list = prefix_and_suffix_list(sentence[0:i])
        elem_shared = [c for c in prefix_list if c in suffix_list]
        val.append(len(elem_shared[0]) if elem_shared else 0)

    return val


def string_md5(sent):
    """计算一个字符串的md5码，输出md5字符串"""
    return hashlib.md5(sent.encode("utf-8")).hexdigest()


def sentence_standardizing(sentence):
    """标准化输入语句"""
    sentence = sentence.strip().replace("·", "")
    if not sentence:
        return ""

    if has_chinese(sentence):
        sentence = ptn_mult_blank.sub("，", sentence).replace(",", "，")
    sentence = ptn_start_puncts.sub("", sentence).strip()
    sentence = ptn_mult_puncts.sub("，", sentence)

    while sentence and sentence[-1] in end_puncts:
        sentence = sentence[:-1]

    return sentence


def zh_num_convert(zh_num):
    """
    Convert Chinese numerals to Arabic numerals
    Reference: http://www.iplaypython.com/code/base/b2600.html
    """
    CN_NUM = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9,
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
        '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
    }
    CN_UNIT = {
        '十': 10,
        '拾': 10,
        '百': 100,
        '佰': 100,
        '千': 1000,
        '仟': 1000,
        '万': 10000,
        '萬': 10000,
        '亿': 100000000,
        '億': 100000000,
        '兆': 1000000000000,
    }
    lcn = list(zh_num)
    unit = 0  # 当前的单位
    ldig = []  # 临时数组

    while lcn:
        cndig = lcn.pop()
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000:
                ldig.append('w')  # 标示万位
                unit = 1
            elif unit == 100000000:
                ldig.append('y')  # 标示亿位
                unit = 1
            elif unit == 1000000000000:  # 标示兆位
                ldig.append('z')
                unit = 1
            continue
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig = dig * unit
                unit = 0
            ldig.append(dig)

    if unit == 10:  # 处理10-19的数字
        ldig.append(10)

    ret = 0
    tmp = 0

    while ldig:
        x = ldig.pop()
        if x == 'w':
            tmp *= 10000
            ret += tmp
            tmp = 0
        elif x == 'y':
            tmp *= 100000000
            ret += tmp
            tmp = 0
        elif x == 'z':
            tmp *= 1000000000000
            ret += tmp
            tmp = 0
        else:
            tmp += x

    ret += tmp

    return ret


if __name__ == '__main__':
    a = kmp_value("13轮")
    print("a = ", a)
    b = kmp_locs("英超曼联第13轮赛程", "13轮", a)
    print("b = ", b)
