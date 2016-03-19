#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from db.dbutil import DBUtil

"""
对movie数据库表进行存取操作
"""

__author__ = "htwxujian@gmail.com"


class MovieDao(object):
    # 初始化数据库的相关信息。
    DBUtil.init_db()

    @staticmethod
    def add_movie(movie):
        session = DBUtil.open_session()
        session.add(movie)
        session.commit()
        DBUtil.close_session(session)
