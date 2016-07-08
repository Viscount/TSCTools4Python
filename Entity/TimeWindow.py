#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gensim import corpora
from util import constants
import math


__author__ = 'Liao Zhenyu'


class TimeWindow(object):

    def __init__(self, index, start, end):
        self.index = index
        self.startSecond = start
        self.endSecond = end
        self.users = []
        self.tsc_num = 0
        self.tsc_avg_length = 0
        self.userFeature = dict()
        self.entropy = 0.0

    def buildUsers(self, userList):
        self.users = userList

    def buildTSCs(self, num):
        self.tsc_num = num

    def buildTSCLength(self, danmaku_list):
        overall_length = 0.0
        for danmaku in danmaku_list:
            if danmaku.content is not None:
                overall_length += len(danmaku.content)
        if len(danmaku_list) == 0:
            self.tsc_avg_length = 0.0
        else:
            self.tsc_avg_length = overall_length/len(danmaku_list)

    def buildEntropy(self, danmaku_list, parse_dict):
        text_all = list()
        danmaku_count = 0
        for danmaku in danmaku_list:
            if danmaku.content is not None:
                danmaku_count += 1
                word_list = parse_dict[danmaku.rowId]
                for word in word_list:
                    text_all.append(word.content)
        dictionary = corpora.Dictionary.load(constants.DANMAKU_DICT)
        word_count = dictionary.doc2bow(text_all)
        word_dict = dict()
        for (token, count) in word_count:
            word_dict[token] = count
        total_words = len(text_all)
        entropy_sum = 0.0
        for danmaku in danmaku_list:
            if danmaku.content is not None:
                entropy = 0.0
                word_list = parse_dict[danmaku.rowId]
                for word in word_list:
                    token_id = dictionary.token2id[word.content]
                    prob = word_dict[token_id] * 1.0 / total_words
                    entropy += prob * math.log(prob, 2)
                entropy_sum += -entropy
        self.entropy = entropy_sum / danmaku_count

    def buildUserFeature(self, user_feature):
        self.userFeature = user_feature
