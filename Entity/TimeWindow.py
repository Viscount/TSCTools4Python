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
        self.userFeature = dict()

    def buildUsers(self, userList):
        self.users = userList

    def buildTSCs(self, num):
        self.tsc_num = num

    def buildUserFeature(self, user_feature):
        self.userFeature = user_feature
