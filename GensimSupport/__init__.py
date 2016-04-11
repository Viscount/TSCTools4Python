#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gensim import corpora
import logging
from util import constants

__author__ = 'Liao Zhenyu'


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_corpus(parse_dict):
    texts = []
    for key, value in parse_dict.items():
        words = []
        for word in value:
            words.append(word.content)
        texts.append(value)
    dictionary = corpora.Dictionary(texts)
    dictionary.save(constants.DANMAKU_DICT)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(constants.CORPUS_PATH, corpus)
    return
