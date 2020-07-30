# coding=utf-8
import numpy as np
import re
from collections import defaultdict


# --- CONSTANTS ----------------------------------------------------------------+


class Word2Vec(object):
    def __init__(self):
        self.n = settings['n']
        self.eta = settings['learning_rate']
        self.epochs = settings['epochs']
        self.window = settings['window_size']
        if settings['model'] == 'skip_gram':
            self.loss_func = self.skip_gram
        else:
            self.loss_func = self.cbow
        self.w1 = None
        self.w2 = None

    # GENERATE TRAINING DATA
    def generate_training_data(self, settings, corpus):

        # GENERATE WORD COUNTS
        word_counts = defaultdict(int)
        for row in corpus:
            for word in row:
                word_counts[word] += 1

        self.v_count = len(word_counts.keys())

        # GENERATE LOOKUP DICTIONARIES
        self.words_list = sorted(list(word_counts.keys()), reverse=False)
        self.word_index = dict((word, i) for i, word in enumerate(self.words_list))
        self.index_word = dict((i, word) for i, word in enumerate(self.words_list))

        training_data = []
        # CYCLE THROUGH EACH SENTENCE IN CORPUS
        for sentence in corpus:
            sent_len = len(sentence)

            # CYCLE THROUGH EACH WORD IN SENTENCE
            for i, word in enumerate(sentence):

                # w_target  = sentence[i]
                w_target = self.word2onehot(sentence[i])

                # CYCLE THROUGH CONTEXT WINDOW
                w_context = []
                for j in range(i - self.window, i + self.window + 1):
                    if j != i and j <= sent_len - 1 and j >= 0:
                        w_context.append(self.word2onehot(sentence[j]))
                training_data.append([w_target, w_context])
        return np.array(training_data)

    # SOFTMAX ACTIVATION FUNCTION
    def softmax(self, x):
        # e_x = np.exp(x - np.max(x))
        # return e_x / e_x.sum(axis=0)
        orig_shape = x.shape
        if len(x.shape) > 1:
            x = x - np.max(x, axis=1, keepdims=True)
            exp_x = np.exp(x)
            x = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        else:
            x = x - np.max(x, axis=0)
            exp_x = np.exp(x)
            x = exp_x / np.sum(exp_x, axis=0)
        assert x.shape == orig_shape
        return x

    # CONVERT WORD TO ONE HOT ENCODING
    def word2onehot(self, word):
        word_vec = [0 for i in range(0, self.v_count)]
        word_index = self.word_index[word]
        word_vec[word_index] = 1
        return word_vec

    # FORWARD PASS
    def forward_pass(self, x):
        h = np.dot(self.w1.T, x)
        u = np.dot(self.w2.T, h)
        y_c = self.softmax(u)
        return y_c, h, u

    # BACKPROPAGATION
    def backprop(self, e, h, x):
        """

        :param e:  v * 1
        :param h:  n * 1
        :param x:  input vector one hot
        :return:
        """
        # 向量外积 np.outer(h, e) = h.T * e
        # delta_w2: n * v
        delta_w2 = np.outer(h, e)
        # delta_w1: v * n
        delta_w1 = np.outer(x, np.dot(self.w2, e.T))

        # UPDATE WEIGHTS
        #
        self.w1 = self.w1 - (self.eta * delta_w1)
        self.w2 = self.w2 - (self.eta * delta_w2)
        pass

    # FORWARD PASS
    def forward_pass_multi(self, inputs):
        c = len(inputs)
        h = np.zeros([self.n, ])
        for x in inputs:
            h += np.dot(self.w1.T, x)
        h = h / c
        u = np.dot(self.w2.T, h)
        y_c = self.softmax(u)
        return y_c, h, u

    def backprop_multi(self, e, h, inputs):
        """

        :param e:  v * 1
        :param h:  n * 1
        :param x:  input vector one hot
        :return:
        """
        # 向量外积 np.outer(h, e) = h.T * e
        # delta_w2: n * v
        delta_w2 = np.outer(h, e)
        # delta_w1: 1 * n
        c = len(inputs)
        delta_w1 = np.dot(self.w2, e.T) / c

        # UPDATE WEIGHTS
        for x in inputs:
            self.w1[x.index(1)] -= self.eta * delta_w1

        self.w2 = self.w2 - (self.eta * delta_w2)

    # TRAIN W2V model
    def train(self, training_data):
        # INITIALIZE WEIGHT MATRICES
        self.w1 = np.random.uniform(-0.8, 0.8, (self.v_count, self.n))  # embedding matrix
        self.w2 = np.random.uniform(-0.8, 0.8, (self.n, self.v_count))  # context matrix

        # CYCLE THROUGH EACH EPOCH
        for i in range(0, self.epochs):

            self.loss = 0

            # CYCLE THROUGH EACH TRAINING SAMPLE
            for w_t, w_c in training_data:
                self.loss += self.loss_func(w_t, w_c)

            print 'EPOCH:', i, 'LOSS:', self.loss
        pass

    def softmax_loss(self, w_t, w_c):
        # FORWARD PASS
        y_pred, h, u = self.forward_pass_multi(w_t)

        # CALCULATE ERROR
        # softmax 损失  y* - 1
        EI = np.sum([np.subtract(y_pred, word) for word in w_c], axis=0)

        # BACKPROPAGATION
        self.backprop_multi(EI, h, w_t)

        # CALCULATE LOSS
        C = len(w_c)
        loss = -np.sum([u[word.index(1)] for word in w_c]) + C * np.log(np.sum(np.exp(u)))
        # self.loss += -2*np.log(len(w_c)) -np.sum([u[word.index(1)] for word in w_c]) + (len(w_c) * np.log(np.sum(np.exp(u))))
        return loss

    def skip_gram(self, w_t, w_c):
        return self.softmax_loss([w_t], w_c)

    def cbow(self, w_t, w_c):
        return self.softmax(w_c, [w_t])

    # input a word, returns a vector (if available)
    def word_vec(self, word):
        w_index = self.word_index[word]
        v_w = self.w1[w_index]
        return v_w

    # input a vector, returns nearest word(s)
    def vec_sim(self, vec, top_n):

        # CYCLE THROUGH VOCAB
        word_sim = {}
        for i in range(self.v_count):
            v_w2 = self.w1[i]
            theta_num = np.dot(vec, v_w2)
            theta_den = np.linalg.norm(vec) * np.linalg.norm(v_w2)
            theta = theta_num / theta_den

            word = self.index_word[i]
            word_sim[word] = theta

        words_sorted = sorted(word_sim.items(), key=lambda (word, sim): sim, reverse=True)

        for word, sim in words_sorted[:top_n]:
            print word, sim

        return words_sorted[:top_n]

    # input word, returns top [n] most similar words
    def word_sim(self, word, top_n):
        index = self.word_index[word]
        vec = self.w1[index]
        return self.vec_sim(vec, top_n)


# --- EXAMPLE RUN --------------------------------------------------------------+

settings = {}
settings['n'] = 5  # dimension of word embeddings
settings['window_size'] = 2  # context window +/- center word
settings['min_count'] = 0  # minimum word count
settings['epochs'] = 5000  # number of training epochs
settings['neg_samp'] = 10  # number of negative words to use during training
settings['learning_rate'] = 0.01  # learning rate
settings['model'] = 'skip_gram'
np.random.seed(0)  # set the seed for reproducibility

corpus = [['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']]

# INITIALIZE W2V MODEL
w2v = Word2Vec()

# generate training data
training_data = w2v.generate_training_data(settings, corpus)

# train word2vec model
w2v.train(training_data)
