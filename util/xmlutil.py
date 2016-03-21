#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Entity.Danmaku import Danmaku


def getDanmakuListFromFile(file_path):
    tree = ET.ElementTree(file=file_path)
    danmakuList = []
    for element in tree.iterfind(".//d"):
        attr = element.get("p")
        content = element.text
        danmaku = Danmaku(attr, content)
        danmakuList.append(danmaku)
    return danmakuList


