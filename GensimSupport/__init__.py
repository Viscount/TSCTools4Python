#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gensim import corpora, models
from util import constants

__author__ = 'Liao Zhenyu'


def get_corpus(parse_dict):
    texts = []
    for key, value in parse_dict.items():
        words = []
        if value is None:
            continue
        for word in value:
            words.append(word.content)
        texts.append(words)
    dictionary = corpora.Dictionary(texts)
    dictionary.save(constants.DANMAKU_DICT)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(constants.CORPUS_PATH, corpus)
    tfidf = models.TfidfModel(corpus)
    tfidf.save(constants.TFIDF_MODLE)
    return
