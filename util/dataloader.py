#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Entity.Danmaku import Danmaku
from util.constants import FILE_PATH
import re
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


if __name__ == "__main__":
    # 测试代码，测试从xml文件中读取的数据。
    danmakuList = getDanmakuListFromTxtFile(FILE_PATH)
    for danmaku in danmakuList:
        print danmaku.videoSecond, u"\t", danmaku.content
