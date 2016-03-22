#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import constants
from Entity import Danmaku
from Entity import TimeWindow
from util import xmlutil
from util import danmakuutil

__author__ = 'Liao Zhenyu'


def getDataSource(method):
    if method == "xml":
        return xmlutil.getDanmakuListFromFile(constants.FILE_PATH)
    elif method == "database":
        pass
    else:
        raise ValueError("数据源参数错误")


def buildWindow(danmaku_list, window_size, step_length):
    window_list = []
    current_start = 0
    current_end = current_start + window_size
    current_danmaku = []
    current_index = 0
    for danmaku in danmaku_list:
        if danmaku.videoSecond <= current_end:
            current_danmaku.append(danmaku)
        else:
            time_window = TimeWindow(current_index, current_start, current_end)
            time_window.buildUserFeature()
            window_list.append(time_window)
            current_index += 1
            current_start += step_length
            current_end = current_start + window_size
            current_danmaku = [danmaku]
    return window_list


if __name__ == "__main__":
    danmaku_list = getDataSource("xml")

