# -*- coding:utf-8 -*-
import numpy as np
import random


class Document(object):
    def __init__(self):
        self.words = []
        self.length = 0


class DocStats(object):

    def __init__(self):
        self.docs_count = 0
        self.words_count = 0
        self.docs = []
        self.word2id = {}


class LDAModel(object):

    def __init__(self, K, alpha, beta, iter_times, top_words_num=5):
        # 模型参数
        # 聚类个数K
        self.K = K
        # 超参数α（alpha）
        self.beta = beta
        # β(beta)
        self.alpha = alpha
        # 迭代次数iter_times
        self.iter_times = iter_times
        # 每个类特征词个数top_words_num
        self.top_words_num = top_words_num

    def init_params(self, docs):
        self.preprocessing(docs)
        # nw,词word在主题topic上的分布
        self.nw = np.zeros((self.data.words_count, self.K), dtype="int")
        # nwsum,每各topic的词的总数
        self.nwsum = np.zeros(self.K, dtype="int")
        # nd,每个doc中各个topic的词的总数
        self.nd = np.zeros((self.data.docs_count, self.K), dtype="int")
        # ndsum,每各doc中词的总数
        self.ndsum = np.zeros(self.data.docs_count, dtype="int")

        # M*doc.size()，文档中词的主题分布
        self.Z = np.array(
            [[0 for _ in xrange(self.data.docs[x].length)] for x in xrange(self.data.docs_count)])

        # 随机先分配类型
        for x in xrange(len(self.Z)):
            self.ndsum[x] = self.data.docs[x].length
            for y in xrange(self.data.docs[x].length):
                topic = random.randint(0, self.K - 1)
                self.Z[x][y] = topic
                self.nw[self.data.docs[x].words[y]][topic] += 1
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1
        self.theta = np.zeros((self.data.docs_count, self.K))
        self.phi = np.zeros((self.K, self.data.words_count))
        # self.theta = np.array([[0.0 for y in xrange(self.K)] for x in xrange(self.dpre.docs_count)])
        # self.phi = np.array([[0.0 for y in xrange(self.dpre.words_count)] for x in xrange(self.K)])

        self.Vbeta = self.data.words_count * self.beta
        self.Kalpha = self.K * self.alpha

    def preprocessing(self, docs):
        data = DocStats()
        items_idx = 0
        for tmp in docs:
            # 生成一个文档对象
            doc = Document()
            for item in tmp:
                if data.word2id.has_key(item):
                    doc.words.append(data.word2id[item])
                else:
                    data.word2id[item] = items_idx
                    doc.words.append(items_idx)
                    items_idx += 1
            doc.length = len(tmp)
            data.docs.append(doc)
        data.docs_count = len(data.docs)
        data.words_count = len(data.word2id)
        self.data = data

    def sampling(self, i, j):
        topic = self.Z[i][j]
        word = self.data.docs[i].words[j]
        self.nw[word][topic] -= 1
        self.nd[i][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[i] -= 1

        # p = θmk * φkt
        # θmk
        theta_mk = (self.nd[i] + self.alpha) / (self.ndsum[i] + self.Kalpha)
        # φkt
        phi_kt = (self.nw[word] + self.beta) / (self.nwsum + self.Vbeta)
        p = theta_mk * phi_kt

        for k in xrange(1, self.K):
            p[k] += p[k - 1]

        u = random.uniform(0, p[self.K - 1])
        for topic in xrange(self.K):
            if p[topic] > u:
                break

        self.Z[i][j] = topic
        self.nw[word][topic] += 1
        self.nwsum[topic] += 1
        self.nd[i][topic] += 1
        self.ndsum[i] += 1

        return topic

    def fit(self, docs):
        self.init_params(docs)
        for _ in xrange(self.iter_times):
            for doc in xrange(self.data.docs_count):
                for word in xrange(self.data.docs[doc].length):
                    self.sampling(doc, word)
        self._theta()
        self._phi()

    def _theta(self):
        for i in xrange(self.data.docs_count):
            self.theta[i] = (self.nd[i] + self.alpha) / (self.ndsum[i] + self.Kalpha)

    def _phi(self):
        for k in xrange(self.K):
            self.phi[k] = (self.nw.T[k] + self.beta) / (self.nwsum[k] + self.Vbeta)

    def predict(self, doc):
        doc = [self.data.word2id[word] for word in doc if word in self.data.word2id]
        for _ in xrange(self.iter_times):
            for word in xrange(len(doc)):
                self.sampling(doc, word)


if __name__ == '__main__':
    doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
    doc2 = "My father spends a lot of time driving my sister around to dance practice."
    doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
    doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
    doc5 = "Health experts say that Sugar is not good for your lifestyle."
    # 整合文档数据
    docs = [doc1, doc2, doc3, doc4]
    docs = [doc.split(' ') for doc in docs]
    lda = LDAModel(4, 0.01, 0.01, 100)
    lda.fit(docs)
    lda.predict(doc5)
    # print lda.theta
    # print lda.phi
