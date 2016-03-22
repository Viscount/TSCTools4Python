# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# 分词工具，获取一句话的词语和词性

import jieba.posseg as segtool
from Entity.Word import Word
import filter

__author__ = 'Liao Zhenyu'


def wordSegment(sentence):
    words = []
    results = segtool.cut(sentence)
    for result in results:
        word = Word(filter.check_cont(result.word), result.flag)
        if filter.check_flag(word.pos):
            words.append(word)
    return words
