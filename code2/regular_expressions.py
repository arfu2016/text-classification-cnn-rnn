"""
@Project   : text-classification-cnn-rnn
@Module    : regular_expressions.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/5/18 5:04 PM
@Desc      : 
"""
import re


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
