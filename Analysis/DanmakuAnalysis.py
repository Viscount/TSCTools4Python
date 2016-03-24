#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import constants
from Entity.TimeWindow import TimeWindow
from util import xmlutil
from util import danmakuutil
from util import simutil
import jieba
import numpy as np
import os

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
            time_window.buildUsers(danmakuutil.extract_users(current_danmaku))
            time_window.buildUserFeature(danmakuutil.extract_user_feature(current_danmaku))
            window_list.append(time_window)
            current_index += 1
            current_start += step_length
            current_end = current_start + window_size
            current_danmaku = [danmaku]
    if len(current_danmaku) > 0:
        time_window = TimeWindow(current_index, current_start, current_end)
        time_window.buildUsers(danmakuutil.extract_users(current_danmaku))
        time_window.buildUserFeature(danmakuutil.extract_user_feature(current_danmaku))
        window_list.append(time_window)
    return window_list


def generateMatrix(time_window):
    user_num = len(constants.USERID)
    cmatrix = np.zeros((user_num, user_num))
    for user in time_window.users:
        for com_user in time_window.users:
            index1 = constants.USERID.index(user)
            index2 = constants.USERID.index(com_user)
            feature1 = time_window.userFeature[user]
            feature2 = time_window.userFeature[com_user]
            cmatrix[index1, index2] = simutil.word_frequency_sim(feature1, feature2)
            cmatrix[index2, index1] = cmatrix[index1, index2]
    return cmatrix


if __name__ == "__main__":
    danmakuList = getDataSource(constants.DATASOURCE)
    constants.USERID = danmakuutil.extract_users(danmakuList)
    jieba.load_userdict(constants.USER_DICT_PATH)
    windowList = buildWindow(danmakuList, constants.WINDOW_SIZE, constants.STEP_LENGTH)
    for time_window in windowList:
        matrix = generateMatrix(time_window)
        matrix_file_name = "matrix"+time_window.index+".txt"
        matrix.dump(os.join(constants.DUMP_PATH, matrix_file_name))
