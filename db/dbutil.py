#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.model import BASE_MODEL

"""
数据库操作模块
"""

__author__ = "htwxujian@gmail.com"


class DBUtil(object):
    def __init__(self):
        self.conn_string = "mysql+mysqlconnector://root:18817870106@localhost:3306/ptestdb"

    # 构建数据库链接
    def __construct_conn_str(self, db_type, db_driver, db_user_name, db_pass, hostname, port, db_name):
        # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        self.conn_string = db_type + "+" + db_driver + "://" + db_user_name + ":" \
                           + db_pass + "@" + hostname + ":" + str(port) + "/" + db_name

    # 初始化数据库，创建数据库表等。
    def init_db(self):
        engine = create_engine(self.conn_string)
        session = sessionmaker()
        session.configure(bind=engine)
        BASE_MODEL.metadata.create_all(engine)


if __name__ == "__main__":
    db_util = DBUtil()
    db_util.init_db()
