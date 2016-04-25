#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import codecs
import datetime
import logging
import math
import os
import re
from decimal import Decimal, getcontext

from gensim import corpora

from Entity.Danmaku import Danmaku
from db.model.barrage import Barrage
from util.fileutil import FileUtil

__author__ = 'Liao Zhenyu'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def getDanmakuListFromXmlFile(file_path):
    tree = ET.ElementTree(file=file_path)
    danmakuList = []
    for element in tree.iterfind(".//d"):
        attr = element.get("p")
        content = element.text
        danmaku = Danmaku(attr, content)
        danmakuList.append(danmaku)
    return sorted(danmakuList, key=lambda danmaku: danmaku.videoSecond)


def getDanmakuListFromTxtFile(file_path):
    dankamu_list = []
    with codecs.open(file_path, "rb", "utf-8") as input_file:
        for line in input_file:
            split_info = line.strip().split(u"\t")
            if len(split_info) < 9:
                continue
            param_str = u",".join(split_info[0: len(split_info) - 1])
            print param_str
            danmaku = Danmaku(param_str, split_info[len(split_info) - 1])
            dankamu_list.append(danmaku)
    return sorted(dankamu_list, key=lambda danmaku: danmaku.videoSecond)


# 解析出bilibili直播的弹幕数据。
def getDanmakuListFromLiveTextFile(file_path):
    with codecs.open(file_path, "rb", "utf-8") as input_file:
        (folder, file_name) = os.path.split(file_path)
        barrage_start_datetime_str = file_name.split(".")[0] + " 12:00:00"  # 每场围棋比赛是当天12点开始的。
        barrage_start_datetime = datetime.datetime.strptime(barrage_start_datetime_str, "%Y-%m-%d %H:%M:%S")
        sender_name_list = []
        danmaku_list = []
        for line in input_file:
            split_info = line.strip().split("\t")
            if len(split_info) < 3:
                continue
            datetime_str = split_info[0]
            sender_name = split_info[1]
            content = split_info[2]
            barrage_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            if barrage_datetime < barrage_start_datetime:
                continue  # 比赛还未开始的弹幕略去
            barrage_timestamp = str((barrage_datetime - barrage_start_datetime).total_seconds())
            sender_name_list.append([sender_name])
            # 构建适配参数
            param_str = barrage_timestamp + ",,,,,," + sender_name + ","
            danmaku = Danmaku(param_str, content)
            danmaku_list.append(danmaku)
        # 为每一个用户的名称对应一个唯一的数字表示
        dictionary = corpora.Dictionary(sender_name_list)
        dictionary.save("live_sender_name.dict")
        # 在将danmaku_list中的danmaku用户名称替换为刚刚生成的对应数字表示
        for danmaku in danmaku_list:
            danmaku.senderId = str(dictionary.token2id[danmaku.senderId])
        return danmaku_list


# 对xml弹幕数据进行排序，将排序好的弹幕数据写入代码文件的当前目录下。
def gen_sorted_danmaku_file_from_xml(file_path):
    barrage_list = __parse_barrage_xml_file(file_path)
    barrage_list = sort_barrages(barrage_list)  # 将弹幕按照降序排序。
    file_name = str(__get_barrage_xml_file_cid(file_path)) + "-sorted.txt"
    with codecs.open(file_name, "wb", "utf-8") as output_file:
        for barrage in barrage_list:
            barrage_str = __format_dankamu_play_timestamp(barrage.play_timestamp) + u"\t" + barrage.play_timestamp\
                          + u"\t" + barrage.type + u"\t" + barrage.font_size + u"\t" + barrage.font_color + u"\t"\
                          + barrage.unix_timestamp + u"\t" + barrage.pool + u"\t" + barrage.sender_id + u"\t"\
                          + barrage.row_id + u"\t" + barrage.content + u"\n"
            output_file.write(barrage_str)
    return barrage_list


# 格式化原弹幕数据中的playtimestamp为xxminutexxs的格式
def __format_dankamu_play_timestamp(timestamp):
    timestamp = float(timestamp)
    minutes = int(math.floor(timestamp / 60))
    seconds = int(math.floor(timestamp % 60))
    format_str = str(minutes) + u" minute " + str(seconds) + u" s"
    return format_str


def __sort_barrages_by_play_timestamp(barrage):
    # 由于play_timestamp字符串时间戳的小树位置不定，所以用Decial将字符串转化为数字
    # 将 decimal 的精度设置为30
    getcontext().prec = 30
    return Decimal(barrage.play_timestamp)


# order_flag：True 按照play_timestamp升序排列
# order_flag：False 按照play_timestamp降序排列
def sort_barrages(barrages, order_flag=False):
    barrages = sorted(barrages, key=__sort_barrages_by_play_timestamp, reverse=order_flag)
    return barrages


# 文件名称必须是以 cid.xml命名的，否则无法读取弹幕信息。
def __get_barrage_xml_file_cid(xml_file_path):
    (base_path, xml_file_name) = os.path.split(xml_file_path)
    cid = xml_file_name.split(".")[0]
    return cid


# 解析出xml文件中的弹幕信息，文件名称必须是以 cid.xml命名的，否则无法读取弹幕信息。
def __parse_barrage_xml_file(xml_file_path):
    # 获取xml文件中的全部内容。
    with codecs.open(xml_file_path, "rb", "utf-8") as input_file:
        content = []
        for line in input_file:
            content.append(line)
    content = u"\n".join(content)
    # 弹幕出现的播放时间，弹幕类型，字体大小，字体颜色，弹幕出现的unix时间戳，弹幕池，弹幕创建者id，弹幕id
    pattern = re.compile(r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>', re.S)
    barrages = re.findall(pattern, content)
    if len(barrages) <= 0:
        return None
    barrage_list = []
    for barrage_tuple in barrages:
        barrage = Barrage(play_timestamp=barrage_tuple[0], type=barrage_tuple[1], font_size=barrage_tuple[2],
                          font_color=barrage_tuple[3], unix_timestamp=barrage_tuple[4], pool=barrage_tuple[5],
                          sender_id=barrage_tuple[6], row_id=barrage_tuple[7], content=barrage_tuple[8])
        barrage_list.append(barrage)
    return barrage_list


if __name__ == "__main__":
    # 测试代码，测试从xml文件中读取的数据。
    # danmakuList = getDanmakuListFromTxtFile(FILE_PATH)
    # for danmaku in danmakuList:
    #     print danmaku.videoSecond, u"\t", danmaku.content

    # 将xml文件的弹幕数据读取出来，排序后写入当前的文件夹下。
    # gen_sorted_danmaku_file_from_xml(os.path.join(FileUtil.get_project_root_path(), "data", "movie", "2065063.xml"))

    # 从弹幕的live数据中读取信息。
    danmaku_list = getDanmakuListFromLiveTextFile(
        os.path.join(FileUtil.get_project_root_path(), "data", "AlphaGo", "bilibili",
                     "2016-03-09.txt"))
    for danmaku in danmaku_list:
        print str(danmaku.videoSecond), u"\t", danmaku.senderId, u"\t", danmaku.content, u"\n"
