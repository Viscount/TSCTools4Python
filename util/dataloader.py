#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Entity.Danmaku import Danmaku
from util.constants import FILE_PATH
from db.dao.bilibili_xml_parser import BilibiliXmlParser
from decimal import Decimal, getcontext
import codecs

__author__ = 'Liao Zhenyu'


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


# 对xml数据进行排序。
def gen_sorted_danmaku_file_from_xml(file_path):
    barrage_list = BilibiliXmlParser.parse_xml(file_path)
    barrage_list = sort_barrages(barrage_list)  # 将弹幕按照降序排序。
    file_name = str(BilibiliXmlParser.get_cid(file_path)) + "-sorted.txt"
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
    minutes = timestamp / 60
    seconds = timestamp % 60
    format_str = str(minutes) + u"minute" + str(seconds) + u"s";
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


if __name__ == "__main__":
    # 测试代码，测试从xml文件中读取的数据。
    # danmakuList = getDanmakuListFromTxtFile(FILE_PATH)
    # for danmaku in danmakuList:
    #     print danmaku.videoSecond, u"\t", danmaku.content
    gen_sorted_danmaku_file_from_xml(FILE_PATH)
