#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from db.dao.videodao import VideoDao
from db.dbutil import DBUtil
from db.model import Barrage

"""
对movie数据库表进行存取操作
"""

__author__ = "htwxujian@gmail.com"


class BarrageDao(object):
    # 初始化数据库的相关信息。
    DBUtil.init_db()

    """
    barrages: [(,,,,,,,), (,,,,,,,).....]
    cid: barrage对应的cid信息
    """

    @staticmethod
    def add_barrages(barrages, cid):
        video = VideoDao.get_video_by_cid(cid)
        if video is None:
            return False
        session = DBUtil.open_session()
        try:
            for barrage in barrages:
                b = Barrage(row_id=barrage[7], play_timestamp=barrage[0], type=barrage[1], font_size=barrage[2],
                            font_color=barrage[3], unix_timestamp=barrage[4], pool=barrage[5], sender_id=barrage[6],
                            content=barrage[8])
                b.video = video
                session.add(b)
            session.commit()
            return True
        except Exception as e:
            print e
            session.rollback()
            return False
        finally:
            DBUtil.close_session(session)
