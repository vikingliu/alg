# coding=utf-8

# f(q,d) = SUM(c(w,q)) * (k+1)c(w,d)/(c(w,d)+k(1-b+b |d|/avdl) * log(M/df(w))

# 第一项c(w,q)就是搜索q中词w的词频
# 第三项是词w的逆文档频率，M是所有文本的个数，df(w)是出现词w的文本个数
# 中间的第二项是关键，实质是词w的TF值的变换，c(w,d)是词w在文本d中的词频。
# 首先是一个TF Transformation，目的是防止某个词的词频过大，经过下图中公式的约束，词频的上限为k+1，不会无限制的增长。
# 例如，一个词在文本中的词频无论是50还是100，都说明文本与这个词有关，但相关度不可能是两倍关系。
# b是[0,1]之间的常数，avdl是平均文本长度，d是文本d的长度。
# avdl 平均文档长度
# https://www.zybuluo.com/zhuanxu/note/974675

import math
from six import iteritems
from six.moves import xrange

# BM25 parameters.
PARAM_K1 = 1.5
PARAM_B = 0.75
EPSILON = 0.25


class BM25(object):
    def __init__(self, corpus):
        self.corpus_size = len(corpus)
        self.avgdl = sum(map(lambda x: float(len(x)), corpus)) / self.corpus_size
        self.corpus = corpus
        self.f = []
        self.df = {}
        self.idf = {}
        self.initialize()

    def initialize(self):
        for document in self.corpus:
            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            # word fre in doc
            self.f.append(frequencies)
            for word, freq in iteritems(frequencies):
                if word not in self.df:
                    self.df[word] = 0
                # word fre
                self.df[word] += 1
        for word, freq in iteritems(self.df):
            self.idf[word] = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)

    def get_score(self, document, index, average_idf):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue
            idf = self.idf[word] if self.idf[word] >= 0 else EPSILON * average_idf
            score += (idf * self.f[index][word] * (PARAM_K1 + 1)
                      / (self.f[index][word] + PARAM_K1 * (1 - PARAM_B + PARAM_B * self.corpus_size / self.avgdl)))
        return score

    def get_scores(self, document, average_idf):
        scores = []
        for index in xrange(self.corpus_size):
            score = self.get_score(document, index, average_idf)
            scores.append(score)
        return scores


def get_bm25_weights(corpus):
    bm25 = BM25(corpus)
    average_idf = sum(map(lambda k: float(bm25.idf[k]), bm25.idf.keys())) / len(bm25.idf.keys())
    weights = []
    for doc in corpus:
        scores = bm25.get_scores(doc, average_idf)
        weights.append(scores)

    return weights
