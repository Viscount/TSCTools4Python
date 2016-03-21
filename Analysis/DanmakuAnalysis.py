#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import constants
import os

__author__ = 'Liao Zhenyu'


def getDataSource(method):
    if method == "xml":
        print constants.FILE_PATH

if __name__ == "__main__":
    getDataSource("xml")
