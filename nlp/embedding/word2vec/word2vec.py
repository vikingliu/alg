# -*- coding: utf-8 -*-

import math

from huffman import *
from counter import *




def normalize_l2(value):
    value /= np.sqrt(np.sum(value ** 2, axis=1, keepdims=True))
    return value


# Softmax function, optimized such that larger inputs are still feasible
# softmax(x + c) = softmax(x)
def softmax(x):
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


def is_stop_word(word):
    if len(word) == 0:
        return True
    return False


class Word2Vec:
    def __init__(self, vec_len=15000, learn_rate=0.025, win_len=5, loss_func=None):
        self.cutted_text_list = None
        self.vec_len = vec_len
        self.learn_rate = learn_rate
        self.win_len = win_len
        self.word_dict = None
        self.word_freq = None
        self.freq_list = None
        self.huffman = None
        self.w2 = None
        self.loss_func = self.hiearchical_softmax_loss  # default loss function
        if loss_func == 'softmax_loss':
            self.loss_func = self.softmax_loss
        elif loss_func == 'negative_sampling_loss':
            self.loss_func = self.negative_sampling_loss

    def build_word_dict(self, word_freq):
        # word_dict = {word: {word, freq, possibility, init_vector, huffman_code}, }
        word_dict = {}
        freq_list = [x[1] for x in word_freq]
        sum_count = sum(freq_list) * 1.0
        for i, item in enumerate(word_freq):
            temp_dict = dict(
                word=item[0],
                freq=item[1],
                possibility=item[1] / sum_count,
                vector=np.random.random([1, self.vec_len]),
                Huffman=None,
                theta_vec=np.random.random([1, self.vec_len]),
                one_hot_index=i
            )
            word_dict[item[0]] = temp_dict
        self.word_dict = word_dict
        self.word_freq = word_freq
        self.freq_list = np.array(freq_list) / sum_count

    def train(self, word_list, model='cbow', limit=100, ignore=0):
        # build word_dict and huffman tree
        if self.word_dict is None:
            counter = WordCounter(word_list)
            self.build_word_dict(counter.count_res.larger_than(ignore))
            self.cutted_text_list = counter.word_list
        if self.huffman is None:
            self.huffman = HuffmanTree(self.word_dict, vec_len=self.vec_len)
        # get method
        if model == 'cbow':
            method = self.CBOW
        else:
            method = self.SkipGram
        # train word vector
        before = (self.win_len - 1) >> 1
        after = self.win_len - 1 - before
        # total = len(self.cutted_text_list)
        count = 0
        for epoch in range(limit):
            for line in self.cutted_text_list:
                line_len = len(line)
                for i in range(line_len):
                    word = line[i]
                    if is_stop_word(word):
                        continue
                    context = line[max(0, i - before):i] + line[i + 1:min(line_len, i + after + 1)]
                    method(word, context)
                count += 1

    def CBOW(self, word, context_words):
        if not word in self.word_dict:
            return
        # get sum of all context words' vector
        gram_vector_sum = np.zeros([1, self.vec_len])
        for i in range(len(context_words))[::-1]:
            context_gram = context_words[i]  # a word from context
            if context_gram in self.word_dict:
                gram_vector_sum += self.word_dict[context_gram]['vector']
            else:
                context_words.pop(i)
        if len(context_words) == 0:
            return
        # gram_vector_sum 求个均值
        error = self.loss_func(word, gram_vector_sum)
        # modify word vector
        for context_word in context_words:
            self.word_dict[context_word]['vector'] += error
            self.word_dict[context_word]['vector'] = normalize_l2(self.word_dict[context_word]['vector'])

    def SkipGram(self, word, context_words):
        if not word in self.word_dict:
            return

        for i in range(len(context_words))[::-1]:
            if not context_words[i] in self.word_dict:
                context_words.pop(i)
        if len(context_words) == 0:
            return
        word_vector = self.word_dict[word]['vector']
        for context_word in context_words:
            error = self.loss_func(context_word, word_vector)
            word_vector += error
            # L2 正则
            self.word_dict[word]['vector'] = normalize_l2(word_vector)

    def hiearchical_softmax_loss(self, word, input_vector):
        node = self.huffman.root
        word_code = self.word_dict[word]['code']
        error = np.zeros([1, self.vec_len])
        for level in range(len(word_code)):
            branch = word_code[level]
            p = sigmoid(input_vector.dot(node.value.T))
            grad = self.learn_rate * (1 - int(branch) - p)
            error += grad * node.value
            node.value += grad * input_vector
            # L2正则
            node.value = normalize_l2(node.value)
            if branch == '0':
                node = node.right
            else:
                node = node.left
        return error

    def negative_sampling(self, word, k):
        neg = []
        for _ in range(k):
            while True:
                index = np.argmax(np.random.multinomial(1, self.freq_list))
                new_word = self.word_freq[index]
                if new_word[0] != word:
                    sample = self.word_dict[new_word[0]]
                    neg.append(sample)
                else:
                    break
        return neg

    # word2vec 源码的方法
    def skip_gramp_neg(self, word, context_words):
        if not word in self.word_dict:
            return
        for i in range(len(context_words))[::-1]:
            if not context_words[i] in self.word_dict:
                context_words.pop(i)
        if len(context_words) == 0:
            return
        for context_word in context_words:
            context_word_vector = self.word_dict[context_word]['vector']
            error = self.loss_func(word, context_word_vector)
            context_word_vector += error
            # L2 正则
            self.word_dict[context_word]['vector'] = normalize_l2(context_word_vector)

    def negative_sampling_loss(self, word, input_vector, k=10):
        neg = self.negative_sampling(word, k)
        w = self.word_dict[word]
        error = np.zeros([1, self.vec_len])
        for u in [w] + neg:
            theta = u['theta_vec']
            p = sigmoid(input_vector.dot(theta.T))
            lw_u = 0
            if u['word'] == w['word']:
                lw_u = 1
            grad = self.learn_rate * (lw_u - p)
            error += grad * theta
            theta += grad * input_vector
            # L2正则
            u['theta_vec'] = normalize_l2(theta)
        return error

    def softmax_loss(self, word, input_vector):

        if self.w2 is None:
            self.w2 = np.random.uniform(-0.8, 0.8, (self.vec_len, len(self.word_dict)))  # context matrix

        u = input_vector.dot(self.w2)
        y_c = softmax(u)
        index = self.word_dict[word]['one_hot_index']

        # 反向传播 softmax
        y_c[:, index] -= 1
        e = y_c

        delta_w2 = np.outer(input_vector, e)
        delta_w1 = np.dot(self.w2, e.T)

        # UPDATE WEIGHTS
        error = -self.learn_rate * delta_w1.T
        self.w2 -= self.learn_rate * delta_w2

        return error

    def sim_word(self, word1, word2):
        vec1 = self.word_dict[word1]['vector']
        vec2 = self.word_dict[word2]['vector']
        return self.sim_vec(vec1, vec2)

    def sim_vec(self, vec1, vec2):
        theta_num = np.dot(vec1, vec2)
        theta_den = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        theta = theta_num / theta_den
        return theta

    def __getitem__(self, word):
        if not word in self.word_dict:
            return None
        return self.word_dict[word]['vector']


if __name__ == '__main__':
    data = [
        'Merge multiple sorted inputs into a single sorted output',
        'The API below differs from textbook heap algorithms in two aspects'
    ]
    wv = Word2Vec(vec_len=50, loss_func='negative_sampling_loss')
    wv.train(data, model='cbow')
    print(wv['into'])
