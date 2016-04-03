#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import consoleutil as console
import WordSegment

__author__ = 'Liao Zhenyu'


def extract_users(danmaku_list):
    user_list = set()
    for danmaku in danmaku_list:
        user_list.add(danmaku.senderId)
    return user_list


def merge_word_dict(old_word_dict, new_word_dict):
    result_dict = dict()
    for key, value in old_word_dict.items():
        result_dict[key] = value
    for key, value in new_word_dict.items():
        if key in result_dict:
            count = result_dict[key]
            count += value
            result_dict[key] = value
        else:
            result_dict[key] = value
    return result_dict


def extract_user_feature(danmaku_list):
    user_feature = dict()
    for danmaku in danmaku_list:
        if danmaku.content is None:
            continue
        console.ConsoleUtil.print_console_info("start parsing sentence "+danmaku.content)
        word_list = WordSegment.wordSegment(danmaku.content)
        if len(word_list) == 0:
            continue
        word_dict = dict()
        for word in word_list:
            if word.content in word_dict:
                count = word_dict[word.content]
                count += 1
                word_dict[word.content] = count
            else:
                word_dict[word.content] = 1
        user_id = danmaku.senderId
        if user_id in user_feature:
            old_dict = user_feature[user_id]
            user_feature[user_id] = merge_word_dict(old_dict, word_dict)
        else:
            user_feature[user_id] = word_dict
    return user_feature
