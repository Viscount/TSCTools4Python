#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import constants
from Entity.TimeWindow import TimeWindow
from util import danmakuutil
from util import simutil
from util.datasourceutil import getDataSource
import WordSegment
import GensimSupport
import numpy as np
import os
import codecs
import logging
from util.fileutil import FileUtil

__author__ = 'Liao Zhenyu'


# 根据弹幕列表和预设参数生成时间窗口列表
# 参数说明：
# danmaku_list 弹幕列表
# window_size 时间窗口大小
# step_length 时间窗口
# parse_dict 分词词典
def buildWindow(danmaku_list, window_size, step_length, parse_dict):
    window_list = []
    current_start = 0
    current_end = current_start + window_size
    current_danmaku = []
    current_index = 0
    while current_start < danmaku_list[-1].videoSecond:
        logging.info("Building time window " + str(current_index) + "...")
        for danmaku in danmaku_list:
            if current_start <= danmaku.videoSecond <= current_end:
                current_danmaku.append(danmaku)
            elif danmaku.videoSecond > current_end:
                break
        time_window = TimeWindow(current_index, current_start, current_end)
        time_window.buildUsers(danmakuutil.extract_users(current_danmaku))
        time_window.buildTSCs(len(current_danmaku))
        time_window.buildUserFeature(danmakuutil.extract_user_feature(current_danmaku, parse_dict, "TF-IDF"))
        window_list.append(time_window)

        current_index += 1
        current_start += step_length
        current_danmaku = []
        current_end = current_start + window_size

    return window_list


# 获取时间窗口的统计指标
def getStatistics(window_list):
    with open(constants.STATISTIC_LOG, "w") as f:
        for time_window in window_list:
            f.write(str(time_window.tsc_num))
            f.write(" ")


# 根据时间窗口生成相似度矩阵
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
                sim = simutil.tf_idf_cos_sim(feature1, feature2)
                if sim > 0:
                    count += 1
                cmatrix[index1, index2] = sim
                cmatrix[index2, index1] = sim
    print count
    return cmatrix


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # 首先检查弹幕的输出文件夹是否存在，如不存在，那么创建该文件夹。
    FileUtil.create_dir_if_not_exist(constants.DUMP_PATH)
    danmakuList = getDataSource(constants.DATASOURCE)
    constants.USERID = list(danmakuutil.extract_users(danmakuList))
    parse_dict = WordSegment.get_parse_dict(danmakuList)
    # GensimSupport.get_corpus(parse_dict)
    windowList = buildWindow(danmakuList, constants.WINDOW_SIZE, constants.STEP_LENGTH, parse_dict)
    # getStatistics(windowList)
    # for time_window in windowList:
    #     logging.info("Start generating matrix" + str(time_window.index) + "...")
    #     matrix = generateMatrix(time_window)
    #     matrix_file_name = "matrix"+str(time_window.index)+".txt"
    #     with open(os.path.join(constants.DUMP_PATH, matrix_file_name), mode="w") as f:
    #         np.savetxt(f, matrix, fmt='%.2f', newline='\n')

    with codecs.open("seg-result.txt", "wb", "utf-8") as output_file:
        for time_window in windowList:
            str_info = str(time_window.index) + u"\t"
            for user_id, word_frequency in time_window.userFeature.items():
                str_info += (user_id + u"\t")
                for word, frequency in word_frequency.items():
                    str_info += (word + u"\t" + str(frequency) + u"\t")
            print str_info
            output_file.write(str_info)
