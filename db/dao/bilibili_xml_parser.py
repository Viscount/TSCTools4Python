#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os

"""
对b站的弹幕xml本地文件进行解析。
"""

__author__ = "htwxujian@gmail.com"


class BilibiliXmlParser(object):
    def get_cid(self, xml_file_path):
        (base_path, xml_file_name) = os.path.split(xml_file_path)
        cid = xml_file_name.split(".")[0]
        return cid

    # 解析出xml文件中的弹幕信息，文件名称必须是以 cid.xml命名的，否则无法读取弹幕信息。
    def parse_xml(self, video, xml_file_path):
        pass
