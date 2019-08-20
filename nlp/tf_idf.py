# coding=utf-8
import math


# 词频（Term Frequency, TF） TFw,Di =  count(w) / |Di|, word(w) 在 Document(Di)中的频率
# 逆文档频率（Inverse Document Frequency, IDF） IDFw = log(N/SUM(I(w,Di))
# N为所有的文档总数，I(w,Di)表示文档Di是否包含关键词，若包含则为1，若不包含则为0
# IDFw = log(N/(1+SUM(I(w,Di)))

# TF-IDFw,Di = TFw,Di * IDFw

class TF_IDF(object):
    def __init__(self, docs):
        self.docs = docs
        self.idf = {}

    def get_tf(self, w, doc):
        c = 0
        for word in doc:
            if word == w:
                c += 1
        return c / len(doc)

    def get_idf(self, w, docs):
        if w in self.idf:
            return self.idf[w]
        N = len(docs)
        I = 0
        for doc in docs:
            if w in doc:
                I += 1
        idf_v = math.log(N / (1 + I))
        self.idf[w] = idf_v
        return idf_v

    def get_tf_idf(self, w, doc):
        return self.get_tf(w, doc) * self.get_idf(w, self.docs)
