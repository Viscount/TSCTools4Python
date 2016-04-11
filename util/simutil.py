#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math


__author__ = 'Liao Zhenyu'


def word_frequency_sim(userFeature1, userFeature2):
    sumset = set()
    total = 0
    common = 0
    for (key, value) in userFeature1.items():
        if key not in sumset:
            sumset.add(key)
        total += value
    for (key, value) in userFeature2.items():
        if key in sumset:
            common += (value + userFeature1[key])
        total += value
    return common * 1.0 / total


def norm(userFeature):
    sqrsum = 0.0
    for key, value in userFeature.items():
        sqrsum += value * value
    return math.sqrt(sqrsum)


def tf_idf_sim(userFeature1, userFeature2):
    userFeatureDict1 = dict()
    userFeatureDict2 = dict()
    for (token, weight) in userFeature1:
        userFeatureDict1[token] = weight
    for (token, weight) in userFeature2:
        userFeatureDict2[token] = weight
    commonset = set()
    for key in userFeatureDict2.keys():
        if key in userFeatureDict1.keys():
            commonset.add(key)
    dot = 0.0
    for key in commonset:
        dot += userFeatureDict1[key] * userFeatureDict2[key]
    return dot/norm(userFeatureDict1)/norm(userFeatureDict2)
