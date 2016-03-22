#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Liao Zhenyu'


class TimeWindow(object):

    def __init__(self, index, start, end):
        self.index = index
        self.startSecond = start
        self.endSecond = end
        self.userFeature = dict()

    def buildUserFeature(self):
        pass

