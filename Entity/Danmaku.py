#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Liao Zhenyu'


class Danmaku(object):

    def __init__(self, param_string, content):
        self._content = content
        paramList = param_string.split(",")
        self._videoSecond = paramList[0]
        self._mode = paramList[1]
        self._fontSize = paramList[2]
        self._color = paramList[3]
        self._timestamp = paramList[4]
        self._poolType = paramList[5]
        self._senderId = paramList[6]
        self._rowId = paramList[7]

    @property
    def rowId(self):
        return self._rowId

    @property
    def videoSecond(self):
        return self._videoSecond

    @property
    def mode(self):
        return self._mode

    @property
    def fontSize(self):
        return self._fontSize

    @property
    def color(self):
        return self._color

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def poolType(self):
        return self._poolType

    @property
    def senderId(self):
        return self._senderId

    @property
    def rowId(self):
        return self._rowId
