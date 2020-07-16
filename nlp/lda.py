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
        self.id2word = {}


class LDAModel(object):

    def __init__(self, model=None):
        self.model = model
        if model:
            self.K = model.K
            # 超参数α（alpha）
            self.beta = model.beta
            # β(beta)
            self.alpha = model.alpha
            # 迭代次数iter_times
            self.iter_times = model.iter_times
            # 每个类特征词个数top_words_num
            self.top_words_num = model.top_words_num
            self.topic_words = {}

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
        if self.model:
            data.id2word = self.model.data.id2word
            data.word2id = self.model.data.word2id
        for d in docs:
            # 生成一个文档对象
            doc = Document()
            doc_len = 0
            for w in d:
                if data.word2id.has_key(w):
                    doc.words.append(data.word2id[w])
                    doc_len += 1
                elif self.model is None:
                    data.word2id[w] = items_idx
                    data.id2word[items_idx] = w
                    doc.words.append(items_idx)
                    items_idx += 1
                    doc_len += 1
                else:
                    # word not in model
                    pass

            doc.length = doc_len
            data.docs.append(doc)
        data.docs_count = len(data.docs)
        data.words_count = len(data.word2id)
        self.data = data

    def sampling(self, d, w):
        """
                Gibbs Sampling为当前词重新分配主题
                :param d: 文档编号
                :param w: 词在文档中的编号
                """
        topic = self.Z[d][w]
        word = self.data.docs[d].words[w]
        self.nw[word][topic] -= 1
        self.nd[d][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[d] -= 1

        # p = θmk * φkt
        # θmk
        theta_mk = (self.nd[d] + self.alpha) / (self.ndsum[d] + self.Kalpha)
        if self.model:
            phi_kt = (self.model.nw[word] + self.nw[word] + self.beta) / (self.model.nwsum + self.nwsum + self.Vbeta)
        else:
            # φkt
            phi_kt = (self.nw[word] + self.beta) / (self.nwsum + self.Vbeta)
        p = theta_mk * phi_kt

        # 随机更新 topic, 跟新概率大的
        for k in xrange(1, self.K):
            p[k] += p[k - 1]

        u = random.uniform(0, p[self.K - 1])
        for topic in xrange(self.K):
            if p[topic] > u:
                break

        # 按这个更新主题更好理解，这个效果还不错
        # p = np.squeeze(np.asarray(self.p / np.sum(self.p)))
        # topic = np.argmax(np.random.multinomial(1, p))

        self.nw[word][topic] += 1
        self.nwsum[topic] += 1
        self.nd[d][topic] += 1
        self.ndsum[d] += 1

        return topic

    def fit(self, docs, K, alpha, beta, iter_times, top_words_num=5):
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
        self.topic_words = {}
        self._fit(docs)

    def _fit(self, docs):
        self.init_params(docs)
        for _ in xrange(self.iter_times):
            for d in xrange(self.data.docs_count):
                for w in xrange(self.data.docs[d].length):
                    topic = self.sampling(d, w)
                    self.Z[d][w] = topic
        self._theta()
        self._phi()
        self._topic_words()

    def _theta(self):
        for i in xrange(self.data.docs_count):
            self.theta[i] = (self.nd[i] + self.alpha) / (self.ndsum[i] + self.Kalpha)

    def _phi(self):
        for k in xrange(self.K):
            self.phi[k] = (self.nw.T[k] + self.beta) / (self.nwsum[k] + self.Vbeta)

    def predict(self, docs, iter_times=100, repeat_num=3):
        self.iter_times = iter_times
        rst = np.zeros((len(docs), self.K))
        for _ in range(repeat_num):
            self._fit(docs)
            rst += self.theta
        rst /= repeat_num
        rst = [sorted([(k, p) for k, p in enumerate(doc_topic)], key=lambda x: x[1], reverse=True) for doc_topic in rst]
        return rst

    def _topic_words(self):
        self.top_words_num = min(self.top_words_num, self.data.words_count)
        for k in xrange(self.K):
            words = [(self.data.id2word[n], self.phi[k][n]) for n in xrange(self.data.words_count)]
            words.sort(key=lambda i: i[1], reverse=True)
            self.topic_words[k] = words[0:5]

    def get_topic(self, k):
        return self.topic_words[k] if k < self.K else []


if __name__ == '__main__':
    doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
    doc2 = "My father spends a lot of time driving my sister around to dance practice."
    doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
    doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
    doc5 = "Health experts say that Sugar is not good for your lifestyle."
    # 整合文档数据
    docs = [doc1, doc2, doc3, doc4]
    docs = [doc.split(' ') for doc in docs]
    lda = LDAModel()
    lda.fit(docs, 4, 0.01, 0.01, 1000)
    newlda = LDAModel(lda)
    docs = [doc5]
    docs = [doc.split(' ') for doc in docs]
    print newlda.predict(docs)
    # lda.predict(doc5)
    # print lda.theta
    # print lda.phi
