#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Entity.Danmaku import Danmaku
from util.constants import FILE_PATH

__author__ = 'Liao Zhenyu'


def getDanmakuListFromFile(file_path):
    tree = ET.ElementTree(file=file_path)
    danmakuList = []
    for element in tree.iterfind(".//d"):
        attr = element.get("p")
        content = element.text
        danmaku = Danmaku(attr, content)
        danmakuList.append(danmaku)
    return sorted(danmakuList, key=lambda danmaku: danmaku.videoSecond)

if __name__ == "__main__":
    # 测试代码，测试从xml文件中读取的数据。
    danmakuList = getDanmakuListFromFile(FILE_PATH)
    for danmaku in danmakuList:
        print danmaku.videoSecond, u"\t", danmaku.content
