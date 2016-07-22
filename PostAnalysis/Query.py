# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import codecs
from util import constants

__author__ = 'Liao Zhenyu'


class WindowDetail(object):
    def __init__(self, index, number):
        self.index = index
        self.startSecond = index * constants.STEP_LENGTH
        self.startMin = WindowDetail.format_time(self.startSecond)[0]
        self.startSec =  WindowDetail.format_time(self.startSecond)[1]
        self.endSecond = self.startSecond + constants.WINDOW_SIZE
        self.endMin = WindowDetail.format_time(self.endSecond)[0]
        self.endSec =  WindowDetail.format_time(self.endSecond)[1]
        self.value = number
        self.rank = 0

    @staticmethod
    def format_time(seconds):
        min = seconds / 60
        sec = seconds % 60
        return min,sec



# 读取数据文件
def get_data_source_file(file_path):
    with codecs.open(file_path, "rb", "utf-8") as input_file:
        line = input_file.readline()
    window_datas = line.split(",")
    return window_datas


# 排序，并获取rank值
def sort_and_rank(window_query_data):
    sorted_data = sorted(window_query_data, key=lambda window_detail: window_detail.value)
    rank = 1
    for data in sorted_data:
        data.rank = rank
        rank += 1
    return sorted(sorted_data, key=lambda window_detail: window_detail.index)

# 处理查询字符串，获取查询起始和结束的窗口index
def get_window_index(query):
    query_param = query.split(",")
    query_start = query_param[0].split(":")
    query_end = query_param[1].split(":")
    query_start_min = query_start[0]
    query_start_sec = query_start[1]
    query_end_min = query_end[0]
    query_end_sec = query_end[1]
    query_start_seconds = query_start_min * 60 + query_start_sec
    query_end_seconds = query_end_min * 60 + query_end_sec
    query_start_index = query_start_seconds / constants.STEP_LENGTH
    query_end_index = query_end_seconds / constants.STEP_LENGTH
    return query_start_index, query_end_index

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    window_datas = get_data_source_file(constants.STATISTIC_LOG)
    window_index = 0
    window_query_data = list()
    for window_data in window_datas:
        window = WindowDetail(window_index, window_data)
        window_query_data.append(window)
        window_index += 1
    window_query_data = sort_and_rank(window_query_data)
    query = input("Please input the start time and end time: \n")
    while query != "0":
        start_index, end_index = get_window_index(query)
        min_rank = len(window_query_data)
        for index in range(start_index, end_index+1):
            if window_query_data[index].rank < min_rank:
                min_rank = window_query_data[index].rank
        print min_rank
        query = input("Please input the start time and end time: \n")
