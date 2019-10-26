# -*- coding:utf-8 -*-

# 功能：Python爬虫练习，目标起点网
# 内置中文检测
# https://blog.csdn.net/JayRoxis/article/details/72669952
# ======================= 库导入 ============================
import re

# ======================== 中文检测 ==========================
def find_chinese(text):
    if isinstance(text, str):
        return ''
    text = text.decode('utf8')
    res = re.findall(u"[\u4e00-\u9fa5]", text)
    # \u4e00-\u9fa5是中文常用字段
    return res


# ======================== 填充指定字符 ==========================
def my_align(un_align_str, length=0, addin=' '):
    assert isinstance(length, int)        # 输入长度是否为整数
    if length <= len(un_align_str):       # 小于输入长度返回原字符
        return un_align_str
    strlen = len(un_align_str)
    chn = find_chinese(un_align_str)
    numchn = len(chn)
    numsp = length - strlen + numchn      # 填充半角字符的的个数
    str = addin * numsp                   # 生成填充字符串

    return str                            # 返回填充的字符串
