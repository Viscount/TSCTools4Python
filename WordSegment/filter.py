# !/usr/bin/env python
# -*- coding: UTF-8 -*-

from Entity import Word
import library
import re

__author__ = 'Liao Zhenyu'


def check_flag(flag):
    if flag[0] in library.ACCEPTABLE_FLAG:
        return True
    else:
        return False


def check_cont(content):
    for item in library.REPALCE_SET:
        pattern = re.compile(item)
        if re.match(pattern,content) is not None:
            new_content = library.REPLACE_DICT[item]
            return new_content
        else:
            return content
