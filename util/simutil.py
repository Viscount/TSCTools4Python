#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math


__author__ = 'Liao Zhenyu'


def word_frequency_jaccard_sim(userFeature1, userFeature2):
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


def word_frequency_cos_sim(userFeature1, userFeature2):
    commonset = set()
    for key in userFeature1.keys():
        if key in userFeature2.keys():
            commonset.add(key)
    dot = 0.0
    for key in commonset:
        dot += userFeature1[key] * userFeature2[key]
    return dot/norm(userFeature1)/norm(userFeature2)


def norm(userFeature):
    sqrsum = 0.0
    for key, value in userFeature.items():
        sqrsum += value * value
    return math.sqrt(sqrsum)


def tf_idf_cos_sim(userFeature1, userFeature2):
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


if __name__ == "__main__":
    userFeature1 = {"token1": 1, "token2": 2}
    userFeature2 = {"token1": 2, "token3": 1}
    print norm(userFeature1)
    print word_frequency_cos_sim(userFeature1, userFeature2)
