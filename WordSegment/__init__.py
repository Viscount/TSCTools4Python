# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# 分词工具，获取一句话的词语和词性

import jieba.posseg as segtool
from Entity.Word import Word
from util import constants
import filter
import json
import codecs

__author__ = 'Liao Zhenyu'


def wordSegment(sentence):
    words = []
    results = segtool.cut(sentence)
    with codecs.open(constants.PARSE_LOG, mode='a', encoding='utf-8') as f:
        for result in results:
            word = Word(filter.check_cont(result.word), result.flag)
            f.write(json.dumps(word, encoding='UTF-8', default=Word.word2dict, ensure_ascii=False)+" ")
            if filter.check_refuse_flag(word.pos):
                words.append(word)
        f.writelines("\n")
    return words
