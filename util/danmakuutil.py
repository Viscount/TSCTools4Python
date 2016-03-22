#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Entity import Danmaku

__author__ = 'Liao Zhenyu'


def extract_users(danmaku_list):
    user_list = set()
    for danmaku in danmaku_list:
        user_list.add(danmaku.senderId)
    return user_list
