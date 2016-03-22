#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Liao Zhenyu'


class Danmaku(object):

    def __init__(self, param_string, content):
        self.content = content
        paramList = param_string.split(",")
        self.videoSecond = paramList[0]
        self.mode = paramList[1]
        self.fontSize = paramList[2]
        self.color = paramList[3]
        self.timestamp = paramList[4]
        self.poolType = paramList[5]
        self.senderId = paramList[6]
        self.rowId = paramList[7]

