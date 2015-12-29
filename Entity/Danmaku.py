#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Danmaku(object):

    def __init__(self, param_string, content):
        self._content = content
        paramList = param_string.split(",")
        self._video_second = paramList[0]
        self._mode = paramList[1]
        self._font_size = paramList[2]
        self._color = paramList[3]
        self._timestamp = paramList[4]
        self._pool_type = paramList[5]
        self._sender_id = paramList[6]
        self._id = paramList[7]

    @property
    def id(self):
        return self._id

    @property
    def video_second(self):
        return self._video_second

    @property
    def mode(self):
        return self._mode

    @property
    def font_size(self):
        return self._font_size

    @property
    def color(self):
        return self._color

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def pool_type(self):
        return self._pool_type

    @property
    def sender_id(self):
        return self._sender_id

    @property
    def content(self):
        return self._content

