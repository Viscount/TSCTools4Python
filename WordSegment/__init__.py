# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# 分词工具，获取一句话的词语和词性

import jieba.posseg as segtool
from Entity.Word import Word

__author__ = 'Liao Zhenyu'


def wordSegment(sentence):
    words = []
    results = segtool.cut(sentence)
    for result in results:
        word = Word(result.word, result.flag)
        words.append(word)
    return words
