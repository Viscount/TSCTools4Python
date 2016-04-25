#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

__author__ = 'Liao Zhenyu'

DATASOURCE = "xml"
FILE_PATH = os.path.join("..", "data", "movie", "2065063.xml")
WINDOW_SIZE = 30
STEP_LENGTH = 10
USERID = []
DUMP_PATH = os.path.join("..", "data", "matrix")
USER_DICT_PATH = os.path.join("..", "WordSegment", "user_dict.txt")
PARSE_LOG = os.path.join("..", "data", "parseLog.txt")
STATISTIC_LOG = os.path.join("..", "data", "numOfTsc.txt")
DANMAKU_DICT = os.path.join("..", "data", "damakuWord.dict")
CORPUS_PATH = os.path.join("..", "data", "danmaku.mm")
TFIDF_MODLE = os.path.join("..", "data", "tf-idf.model")

