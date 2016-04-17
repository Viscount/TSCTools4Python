#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import constants
from gensim import corpora, models


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
            result_dict[key] = count
        else:
            result_dict[key] = value
    return result_dict


def extract_word_frequency(danmaku_list, parse_dict):
    user_feature = dict()
    for danmaku in danmaku_list:
        if danmaku.content is None:
            continue
        word_list = parse_dict[danmaku.rowId]
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


def extract_tf_idf(danmaku_list, parse_dict):
    user_feature = extract_word_frequency(danmaku_list, parse_dict)
    dictionary = corpora.Dictionary.load(constants.DANMAKU_DICT)
    tfidf = models.TfidfModel.load(constants.TFIDF_MODLE)
    new_user_feature = dict()
    for key, value in user_feature.items():
        word_count_list = []
        for word, count in value.items():
            word_token = dictionary.token2id[word]
            word_count_list.append((word_token, count))
        new_user_feature[key] = tfidf[word_count_list]
    return new_user_feature


def extract_lda(danmaku_list, parse_dict):
    user_feature = extract_tf_idf(danmaku_list, parse_dict)
    lda_model = models.LdaModel.load(constants.LDA_MODLE)
    new_user_feature = dict()
    for key, value in user_feature.items():
        topics = lda_model.get_document_topics(value)
        new_user_feature[key] = topics
    return new_user_feature


def extract_user_feature(danmaku_list, parse_dict, extract_mode):
    if extract_mode == 'Word-Frequency':
        user_feature = extract_word_frequency(danmaku_list, parse_dict)
    elif extract_mode == 'TF-IDF':
        user_feature = extract_tf_idf(danmaku_list, parse_dict)
    elif extract_mode == "LDA":
        user_feature = extract_lda(danmaku_list, parse_dict)
    return user_feature
