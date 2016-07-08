# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# 分词工具，获取一句话的词语和词性

import codecs
import json

import jieba
import jieba.posseg as segtool

import filter
import logging
import os
from Entity.Word import Word
from util import constants
from util.datasourceutil import getDataSource
from util.fileutil import FileUtil

__author__ = 'Liao Zhenyu'


# 对一个句子进行词性划分，返回词性划分后的列表；sentence 为需要划分的句子，
# emotion_dict，用于对句子划分出的结果进行情感词过滤，只有在情感词词典中的划分结果才被接受。
def wordSegment(emotion_dict, sentence):
    words = []
    results = segtool.cut(sentence)
    with codecs.open(constants.PARSE_LOG, mode='a', encoding='utf-8') as f:
        for result in results:
            # 对一些错别词以及2333...这样的词做替换，用相近的词语代替。
            word = Word(filter.check_cont(result.word), result.flag)
            # 检查分词分出的词语是否在情感词典中，如果该词不在情感词典中，就将该词舍弃。
            # if in_emotion_dict(emotion_dict, word.content) is None:  # 该词语在情感词典中不存在。
            #     continue

            # if filter.check_refuse_flag(word.pos):
            words.append(word)
            f.write(json.dumps(word, encoding='UTF-8', default=Word.word2dict, ensure_ascii=False) + " ")
    return words


# 读入情感词词典，读入的情感词词典以字典的形式存储，key为情感词的类别，为String；
# value是一个set实体，set实体中是具体的情感词，为String。最后返回字典格式存储的情感词典。
# emotion_dict_file_path 情感词典的路径信息。
def load_emotion_dict(emotion_dict_file_path):
    emotion_dict = {}
    with codecs.open(emotion_dict_file_path, "rb", "utf-8") as input_file:
        for line in input_file:
            split_line = line.strip().split("\t")
            if len(split_line) < 2:  # 情感词典的每一行最少有两个部分，第一部分为该情感词的分类（必有）；第二部分为情感词（必有）；第三部分为该情感词的描述信息（可选）。
                continue
            key = split_line[0]
            word = split_line[1]
            if key in emotion_dict.keys():
                value_set = emotion_dict[key]
                value_set.add(word)
                emotion_dict[key] = value_set
            else:
                emotion_dict[key] = set([word])
    return emotion_dict


# 检查某一个词语是否在情感词典中，若该词不在情感词典中，那么返回None。
# 若该词存在于情感词典中，则返回(词语类别, 词语)形式的元组对象。
# emotion_dict 情感词典，word 词语String
def in_emotion_dict(emotion_dict, word):
    for key in emotion_dict.keys():
        value_set = emotion_dict[key]
        if word in value_set:
            return key, word
    return None


# 建立分词结果dict
def get_parse_dict(danmaku_list):
    logging.info("Starting parsing sentences in Danmaku...")
    parse_dict = dict()
    jieba.load_userdict(constants.USER_DICT_PATH)
    emotion_dict_path = os.path.join(FileUtil.get_project_root_path(), "WordSegment", "emotion_dict.txt")
    emotion_dict = load_emotion_dict(emotion_dict_path)
    for danmaku in danmaku_list:
        rowId = danmaku.rowId
        if danmaku.content is not None:
            words = wordSegment(emotion_dict, danmaku.content)
            parse_dict[rowId] = words
        else:
            parse_dict[rowId] = None
    logging.info("parse dictionary has generated!")
    return parse_dict


if __name__ == "__main__":
    # 测试代码
    danmaku_list = getDataSource(constants.DATASOURCE)
    emotion_dict_path = os.path.join(FileUtil.get_project_root_path(), "WordSegment", "emotion_dict.txt")
    emotion_dict = load_emotion_dict(emotion_dict_path)
    for (key, value_set) in emotion_dict.items():
        print key, u"\t", u"\t".join(value for value in value_set), u"\n"
    for danmaku in danmaku_list:
        if danmaku.content is None:
            continue
        words = wordSegment(emotion_dict, danmaku.content)
        for word in words:
            print word.content
