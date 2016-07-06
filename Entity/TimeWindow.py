#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

    def buildUserFeature(self, user_feature):
        self.userFeature = user_feature
