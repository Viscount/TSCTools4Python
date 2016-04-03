#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from util import xmlutil, constants
from util import consoleutil as console

__author__ = 'Liao Zhenyu'

"""
对数据源进行操作，如获取数据源等等。
"""


def getDataSource(method):
    if method == "xml":
        console.ConsoleUtil.print_console_info("Get data from xml files at " + constants.FILE_PATH)
        return xmlutil.getDanmakuListFromFile(constants.FILE_PATH)
    elif method == "database":
        console.ConsoleUtil.print_console_info("Get data from database")
        pass
    else:
        raise ValueError("数据源参数错误")