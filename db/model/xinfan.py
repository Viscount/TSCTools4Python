#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
新番信息的实体类
"""

__author__ = "htwxujian@gmail.com"


class XinFan:

    def __init__(self, cover, is_finish, newest_ep_index, pub_time, season_id, title, total_count, url, week):
        self.cover = cover  # 新番的封面图片
        self.is_finish = is_finish  # 新番是否完结，1表示正在连载，2表示已完结
        self.newest_ep_index = newest_ep_index  # 当前新番连载的最新集数
        self.pub_time = pub_time  # 可能是最新集数的发布时间
        self.season_id = season_id  # 新番的id信息
        self.title = title  # 新番的名称
        self.total_count = total_count  # 这个暂时不知道意义
        self.url = url  # 进入新番列表的连接
        self.week = week  # 这个暂时不知道意义
        self.tags = None  # 这个番剧的tag，以\t字符串分割