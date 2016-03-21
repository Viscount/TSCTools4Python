#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Liao Zhenyu'


class Word(object):

    def __init__(self, word, pos):
        self._content = word
        self._pos = pos

    @property
    def content(self):
        return self._content

    @property
    def pos(self):
        return self._pos
