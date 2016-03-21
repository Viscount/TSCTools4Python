#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import codecs
import re

from db.dao.barragedao import BarrageDao
from db.dao.videodao import VideoDao
from spider import BarrageSpider
from util.consoleutil import ConsoleUtil
from util.datetimeutil import DateTimeUtil
from util.fileutil import FileUtil

"""
抓取bilibili站点的视频信息（标题，分类）以及视频对应的弹幕信息。
"""

__author__ = "htwxujian@gmail.com"


class BilibiliSpider(BarrageSpider):
    def __init__(self):
        # 确保父类被正确初始化了
        # http://stackoverflow.com/questions/21063228/typeerror-in-python-single-inheritance-with-super-attribute
        super(BilibiliSpider, self).__init__()

    # 获得视频的标题信息
    def get_video_title(self, html_content):
        pattern = re.compile(r'<div\sclass="v-title"><h1.*?>(.*?)</h1></div>', re.S)
        match = re.search(pattern, html_content)
        if match is None:
            return None
        title = match.group(1)
        return title

    # 获得视频的标签信息。
    def get_video_tags(self, html_content):
        pattern = re.compile(r'<span\stypeof="v:Breadcrumb"><a\shref=.*?\srel="v:url"\sproperty="v:title">(.*?)' +
                             '</a></span>', re.S)
        match = re.findall(pattern, html_content)
        if match is None:
            return None
        tags = u"\t".join(match)
        return tags

    # 获得跟视频弹幕对应的cid信息。
    def get_video_cid(self, html_content):
        pattern = re.compile(r'.*?<script.*>EmbedPlayer\(\'player\',.*?"cid=(\d*)&.*?</script>', re.S)
        match = re.search(pattern, html_content)
        if match is None:
            return u"-1"
        cid = match.group(1).strip()
        return cid

    # 获得视频的id信息。
    def get_video_aid(self, video_url):
        pattern = re.compile(r'http://.*?/.*?/av(.*?)/.*?', re.S)
        match = re.search(pattern, video_url)
        if match is None:
            return None
        mid = match.group(1).strip()
        return unicode(mid)

    # 构建弹幕的xml链接地址。
    def barrage_xml_url(self, cid):
        if cid is None:
            return None
        xml_url = "http://comment.bilibili.tv/" + cid + ".xml"
        print xml_url
        return xml_url

    # 获得弹幕xml链接地址上的全部弹幕信息。
    def get_row_video_barrage(self, barrage_xml_url):
        # 获取弹幕网页的源代码
        barrage_html = self.get_html_content(barrage_xml_url)
        # 弹幕出现的播放时间，弹幕类型，字体大小，字体颜色，弹幕出现的unix时间戳，弹幕池，弹幕创建者id，弹幕id
        pattern = re.compile(r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>', re.S)
        barrages = re.findall(pattern, barrage_html)
        # 返回全部的弹幕信息
        return barrages

    # 获得更新的弹幕列表。
    def get_refresh_video_barrage(self, cid, row_barrages):
        barrage_file_path = FileUtil.get_barrage_file_path(cid)
        # 检查该cid的弹幕文件是否存在，如果不存在，那么此时的row_barrages数据将全部写入文件中，
        # 如果存在，那么就只要找到更新的弹幕记录。
        barrage_count = 0
        if FileUtil.is_file_exists(barrage_file_path):
            last_barrage_index = -1  # 记录文件中最后一条弹幕在row_barrages中的下标。
            barrage_count = FileUtil.get_file_line_count(barrage_file_path)
            last_n_barrages = FileUtil.get_file_last_n_line_content(barrage_file_path, 5)
            ConsoleUtil.print_console_info(u"当前文件的最后n条弹幕：\n" + u"\n".join(last_n_barrages))
            for index in xrange(len(row_barrages) - 1, -1, -1):
                if self.__is_same_barrage(last_n_barrages, row_barrages[index]):
                    # 获得存储在弹幕文件中的最后一条弹幕，在更新弹幕序列中的位置。
                    last_barrage_index = index
                    break
            # 当前弹幕数据没有更新
            if last_barrage_index == (len(row_barrages) - 1):
                row_barrages = []
                ConsoleUtil.print_console_info(unicode(DateTimeUtil.get_cur_timestamp("%Y-%m-%d %H:%M:%S")) +
                                               u"\t" + u"弹幕数据没有更新。")
            # 此时部分的弹幕数据需要更新
            elif last_barrage_index >= 0:
                ConsoleUtil.print_console_info(unicode(DateTimeUtil.get_cur_timestamp("%Y-%m-%d %H:%M:%S")) +
                                               u"\t" + u"有弹幕数据更新：" +
                                               u"\t" + str(len(row_barrages) - last_barrage_index - 1))
                row_barrages = row_barrages[last_barrage_index + 1: len(row_barrages)]
            # 弹幕全文都要更新
            elif last_barrage_index == -1:
                ConsoleUtil.print_console_info(unicode(DateTimeUtil.get_cur_timestamp("%Y-%m-%d %H:%M:%S")) + u"\t" +
                                               u"有弹幕数据更新：" + u"\t" + str(len(row_barrages)))
        barrage_count += len(row_barrages)
        ConsoleUtil.print_console_info(unicode(DateTimeUtil.get_cur_timestamp("%Y-%m-%d %H:%M:%S")) +
                                       u" 当前弹幕总条数：" + unicode(barrage_count) + u"\n\n")
        return row_barrages

    # 将弹幕信息写入文件中。
    def save_barrages_to_local(self, cid, row_barrages):
        if len(row_barrages) > 0:
            barrage_file_path = FileUtil.get_barrage_file_path(cid)
            with codecs.open(barrage_file_path, "ab", "utf-8") as output_file:
                for barrage in row_barrages:
                    if barrage is not None:
                        output_file.write(u"\t".join(barrage) + u"\n")

    # 判断 row_barrages 中的某一条弹幕记录 与 本地文件中最后n条弹幕的某一条是否相同。
    def __is_same_barrage(self, last_n_barrages, barrage):
        # barrage 格式：(row_id, play_timestamp, ... , content)
        # last_n_barrages 格式：[last_barrage, last_barrage, ...]
        for last_barrage in last_n_barrages:
            # last_barrage 格式: (row_id\tplay_timestamp\t...\tcontent)
            last_barrage = last_barrage.split(u"\t")
            if len(last_barrage) != len(barrage):
                ConsoleUtil.print_console_info(u"Error，弹幕格式有误，无法两条弹幕是否相同。")
                continue
            is_same = True
            for index in xrange(0, len(last_barrage)):
                if last_barrage[index] != barrage[index]:
                    is_same = False
                    break
            if is_same:
                return True
        return False

    # 抓取网页的视频以及弹幕信息。
    def start(self, video_url):
        # 视频网页的html源码信息。
        video_html_content = self.get_html_content(video_url)
        # 获得视频的相关信息
        mid = self.get_video_aid(video_url)
        cid = self.get_video_cid(video_html_content)
        tags = self.get_video_tags(video_html_content)
        title = self.get_video_title(video_html_content)
        # 将视频信息存储入数据库中
        VideoDao.add_video(cid, title, tags, mid, unicode(video_url))
        # 获取弹幕信息。
        barrages = self.get_row_video_barrage(self.barrage_xml_url(cid))
        # 获取更新的弹幕信息。
        barrages = self.get_refresh_video_barrage(cid, barrages)
        # 将更新后的弹幕信息写入数据库。
        BarrageDao.add_barrages(barrages, cid)
        # 将更新后的弹幕信息写入本地文件。
        self.save_barrages_to_local(cid, barrages)


if __name__ == "__main__":
    bSpider = BilibiliSpider()
    # video_url = "http://www.bilibili.com/video/av4128614/?tg"  # 为毛直接爬这个网页会爬到主页的内容，刚刚明明不会的。
    # video_url = "http://www.bilibili.com/video/av4119682/"
    video_url = "http://www.bilibili.com/video/av4130482/"
    bSpider.start(video_url)