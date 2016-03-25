#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Liao Zhenyu'


def word_frequency_sim(userFeature1, userFeature2):
    sumset = set()
    total = 0
    common = 0
    for key,value in userFeature1:
        if key not in sumset:
            sumset.add(key)
        total += value
    for key,value in userFeature2:
        if key in sumset:
            common += value+userFeature1[key]
        total += value
    return common * 1.0 / total
