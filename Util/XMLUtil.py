#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Entity.Danmaku import *
import os


class XMLUtil(object):

    @staticmethod
    def read_xml(file_path):
        tree = ET.ElementTree(file=file_path)
        danmaku_list = []
        for element in tree.iterfind(".//d"):
            attr = element.get("p")
            content = element.text
            danmaku = Danmaku(attr, content)
            danmaku_list.append(danmaku)
        return danmaku_list


if __name__ == "__main__":
    os.chdir("D:\\Develop\\workspace\\TSCTools4Python")
    danmaku_list = XMLUtil.read_xml(os.path.join(".", "data", "movie", "2065063.xml"))
    print(danmaku_list[0].content)



