#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import constants
from Entity.TimeWindow import TimeWindow
from util import danmakuutil
from util import simutil
from util import consoleutil as console
from util.datasourceutil import getDataSource
import jieba
import numpy as np
import os
from util.fileutil import FileUtil

__author__ = 'Liao Zhenyu'


def buildWindow(danmaku_list, window_size, step_length):
    window_list = []
    current_start = 0
    current_end = current_start + window_size
    current_danmaku = []
    current_index = 0
    while current_start < danmaku_list[-1].videoSecond:
        console.ConsoleUtil.print_console_info("Building time window " + str(current_index) + "...")
        for danmaku in danmaku_list:
            if current_start <= danmaku.videoSecond <= current_end:
                current_danmaku.append(danmaku)
            elif danmaku.videoSecond > current_end:
                break
        time_window = TimeWindow(current_index, current_start, current_end)
        time_window.buildUsers(danmakuutil.extract_users(current_danmaku))
        time_window.buildTSCs(len(current_danmaku))
        time_window.buildUserFeature(danmakuutil.extract_user_feature(current_danmaku))
        window_list.append(time_window)

        current_index += 1
        current_start += step_length
        current_danmaku = []
        current_end = current_start + window_size

    return window_list


def getStatistics(window_list):
    with open(constants.STATISTIC_LOG+"numOfTsc.txt", "w") as f:
        for time_window in window_list:
            f.write(str(time_window.tsc_num))
            f.write(" ")


def generateMatrix(time_window):
    user_num = len(constants.USERID)
    cmatrix = np.zeros((user_num, user_num))
    count = 0
    for user in time_window.users:
        for com_user in time_window.users:
            index1 = constants.USERID.index(user)
            index2 = constants.USERID.index(com_user)
            feature1 = time_window.userFeature.get(user)
            feature2 = time_window.userFeature.get(com_user)
            if feature1 is not None and feature2 is not None:
                sim = simutil.word_frequency_sim(feature1, feature2)
                if sim > 0:
                    count += 1
                cmatrix[index1, index2] = sim
                cmatrix[index2, index1] = sim
    print count
    return cmatrix


if __name__ == "__main__":
    # 首先检查弹幕的输出文件夹是否存在，如不存在，那么创建该文件夹。
    FileUtil.create_dir_if_not_exist(constants.DUMP_PATH)
    danmakuList = getDataSource(constants.DATASOURCE)
    constants.USERID = list(danmakuutil.extract_users(danmakuList))
    jieba.load_userdict(constants.USER_DICT_PATH)
    windowList = buildWindow(danmakuList, constants.WINDOW_SIZE, constants.STEP_LENGTH)
    getStatistics(windowList)
    for time_window in windowList:
        console.ConsoleUtil.print_console_info("Start generating matrix" + str(time_window.index) + "...")
        matrix = generateMatrix(time_window)
        matrix_file_name = "matrix"+str(time_window.index)+".txt"
        with open(os.path.join(constants.DUMP_PATH, matrix_file_name), mode="w") as f:
            np.savetxt(f, matrix, fmt='%.2f', newline='\n')
