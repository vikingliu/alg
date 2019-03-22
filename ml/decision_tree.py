# coding=utf-8
import copy
import math
import random
import sys
from collections import defaultdict

from ml import ML
from tree import Node


def H(D, has_w=False):
    """
    计算数据集D的熵,
    :param D: [[x11,x12,x13...x1n,y,w],.... [xm1,xm2,xm3...xmn,y,w]] if has_w is True else there is no w
    :param has_w: row[-1] is the weight
    :return: -sum(pk * log(pk)), k=1,2,3..  = len(set(y))
    """
    index = -2 if has_w else -1

    p = defaultdict(int)
    for i, row in enumerate(D):
        y = row[index]
        if has_w:
            p[y] += row[-1]
        else:
            p[y] += 1
    h = 0
    if has_w:
        N = sum([row[-1] for row in D])
    else:
        N = len(D)
    for y in p.keys():
        p[y] /= N * 1.0
        h += p[y] * math.log(p[y], 2)

    return h * -1


def Gini(D, has_w=False):
    """
    计算gini指数
    :param D: [[x11,x12,x13...x1n,y],.... [xm1,xm2,xm3...xmn,y]]
    :param has_w: row[-1] is the weight
    :return: 1 - sum(pk * pk), k=1,2,3..  = len(set(y))
    """
    index = -2 if has_w else -1
    p = defaultdict(int)
    for i, row in enumerate(D):
        y = row[index]
        if has_w:
            # row[-1] is w
            p[y] += row[-1]
        else:
            p[y] += 1

    sum_pk = 0
    if has_w:
        # sum(w)
        N = sum([row[-1] for row in D])
    else:
        N = len(D)
    for y in p.keys():
        p[y] /= N * 1.0
        sum_pk += p[y] * p[y]

    return 1 - sum_pk


def g(D, A, alg='g', has_w=False):
    """
    计算信息增益或者增益率
    :param D: [[x11,x12,x13...x1n,y],.... [xm1,xm2,xm3...xmn,y]]
    :param A: split feature A index
    :param alg: alg in ['g', 'gr']
    :param has_w: row[-1] is the weight
    :return: (g or gr, split Di)
    """

    Di = split(D, A)
    HDA = 0
    HAD = 0
    if has_w:
        N = sum([row[-1] for row in D])
    else:
        N = len(D)
    for i, di in Di.items():
        if has_w:
            diw = sum([row[-1] for row in di])
        else:
            diw = len(di)
        p = 1.0 * diw / N
        HDA += p * H(di, has_w)
        HAD += p
    if alg == 'gr':
        return (H(D, has_w) - HDA) / HAD, Di
    else:
        return H(D, has_w) - HDA, Di


def gr(D, A, has_w=False):
    return g(D, A, 'gr', has_w=has_w)


def min_Gini(D, A, has_w=False):
    """
     计算特征 A所有属性的Gini, 返回最小的Gini和划分
    :param D: [[x11,x12,x13...x1n,y],.... [xm1,xm2,xm3...xmn,y]]
    :param A: split feature A index
    :return: min Gini for all feature A's values
    """
    Di = split(D, A)
    min_gDA = sys.maxint
    split_D = {}

    if has_w:
        len_d = sum([row[-1] for row in D])
    else:
        len_d = len(D)

    for i, D1 in Di.items():

        D2 = []
        for j in Di.keys():
            if j != i:
                D2.extend(Di[j])
        if has_w:
            len_d1 = sum([row[-1] for row in D1])
            len_d2 = sum([row[-1] for row in D2])
        else:
            len_d1 = len(D1)
            len_d2 = len(D2)
        pk = 1.0 * len_d1 / len_d

        gDA = pk * Gini(D1, has_w) + 1.0 * len_d2 / len_d * Gini(D2, has_w)
        if gDA < min_gDA:
            min_gDA = gDA
            split_D = {i: D1}
            if D2:
                split_D['#other'] = D2

    return min_gDA, split_D


def square_error(D, has_w=None):
    if has_w:
        w = [row[-1] for row in D]
        index = -2
    else:
        w = [1] * len(D)
        index = -1
    c = sum([row[index] * w[i] for i, row in enumerate(D)]) * 1.0 / len(D)
    s = sum([math.pow((row[index] * w[i] - c), 2) for r, row in enumerate(D)])
    return s


def min_square_error(D, A, has_w=False):
    D = sorted(D, key=lambda x: x[A])
    n = len(D)
    min_error = sys.maxint
    split_D = {}
    for s in range(1, n):
        R1 = D[0:s]
        R2 = D[s:n]
        error = square_error(R1, has_w) + square_error(R2, has_w)
        if error < min_error:
            min_error = error
            split_D = {'<=%s' % D[s - 1][0]: R1, '>%s' % D[s - 1][0]: R2}
    return min_error, split_D


def split(D, A):
    Di = defaultdict(list)
    for i, item in enumerate(D):
        Di[item[A]].append(item)
    return Di


def max_cnt(D, has_w=False):
    stats = defaultdict(int)
    index = -2 if has_w else -1
    for y in D:
        val = 1
        if type(y) is list:
            if has_w:
                val = y[-1]
            y = y[index]
        stats[y] += val
    stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    return stats[0][0]


def rand(f_set, m):
    n = len(f_set)
    m_features = []
    while len(m_features) < m:
        i = random.randint(0, n * 1000) % n
        if i not in m_features:
            m_features.append(i)
    m_features = [f_set[i] for i in m_features]
    return m_features


def same_row(D, has_w=False):
    x_len = 2 if has_w else 1
    for i in range(1, len(D)):
        for j in range(len(D[0]) - x_len):
            if D[i - 1][j] != D[i][j]:
                return False
    return True


def predict_classify_error(model, test, add_test=False):
    error = 0
    for row in test:
        pre = classify(model, row, add_test)
        if pre != data[-1]:
            error += 1
    return error


def predict_regression(model, test, add_test=False):
    error = 0
    for row in test:
        pre = regression(model, row, add_test)
        error += math.pow(abs(pre - data[-1]), 2)
    return error / len(test)


def empty_sample(T):
    if not T.children:
        return
    T.sample = []
    for child in T.children.values():
        empty_sample(child)


def classify(tree, test, add_test=False):
    if add_test:
        tree.sample.append(test)
    if tree.children:
        val = test[tree.feature]
        sub_tree = tree.children.get(val, None)
        sub_tree = sub_tree if sub_tree else tree.children['#other']
        return classify(sub_tree, test)
    else:
        return tree.val


def regression(tree, test, add_test=False):
    if add_test:
        tree.sample.append(test)
    if tree.children:
        val = test[tree.feature]
        for split_point, sub_tree in tree.children.items():
            if '<=' in split_point and val <= float(split_point.replace('<=', '')):
                break
        return classify(sub_tree, test)
    else:
        return tree.val


class DT(ML):
    split_func = {
        'id3': g,
        'c45': gr,
        'cart': min_Gini,
        'cart_r': min_square_error
    }

    def __init__(self, alg, features, max_depth=sys.maxint, min_sample=1, min_e=0.01, rf=False):
        ML.__init__(self, alg)
        self.alg = alg
        self.features = features
        self.max_depth = max_depth
        self.min_sample = min_sample
        self.min_e = min_e
        self.rf = rf
        self.model = None
        self.error = 0
        # self.split_A = []
        self.best_split_func = self.split_func[self.alg]

    def train(self, data, w=None):
        self.error = 0
        has_w = False
        if w:
            D = copy.deepcopy(data)
            for i, row in enumerate(D):
                row.append(w[i])
            has_w = True
            data = D
        self.model = self._train(data, has_w=has_w)
        # self.split_A.append(self.model.feature)
        return self.model

    def predict(self, test):
        if self.alg == 'cart_r':
            return regression(self.model, test)
        return classify(self.model, test)

    def _train(self, D, has_split_A=[], depth=1, has_w=False):
        split_feature = None
        Di = None
        rst = []
        index = -2 if has_w else -1
        d = [row[index] for row in D]
        if len(set(d)) != 1 and depth <= self.max_depth and len(d) > self.min_sample and not same_row(D, has_w):
            f_set = range(len(D[0]) + index)
            if self.rf:
                m = int(math.sqrt(len(f_set)))
                f_set = rand(f_set, m)
            for A in f_set:
                if A in has_split_A:
                    continue
                gDA, gDi = self.best_split_func(D, A, has_w)
                rst.append((gDA, gDi, A))

            if self.alg in ['id3', 'c45'] and rst:
                gDA, Di, split_feature = max(rst)
                if gDA < self.min_e:
                    split_feature = None

            elif self.alg in ['cart', 'cart_r'] and rst:
                gDA, Di, split_feature = min(rst)

        if split_feature is None:
            if self.alg in ['cart_r']:
                val = sum(d) * 1.0 / len(d)
            else:
                val = max_cnt(D, has_w)
                self.error += sum([row[-1] if has_w else 1 for row in D if row[index] != val])

            return Node(val, sample=D)

        children = {}
        for v, di in Di.items():
            child = self._train(di, has_split_A + [split_feature], depth + 1, has_w)
            if child:
                children[v] = child

        return Node(self.features[split_feature], split_feature, children, D)


class ID3(DT):
    def __init__(self, features, max_depth=sys.maxint, min_sample=1, e=0.01, rf=False):
        DT.__init__(self, 'id3', features, max_depth, min_sample, e, rf)


class C45(DT):
    def __init__(self, features, max_depth=sys.maxint, min_sample=1, e=0.01, rf=False):
        DT.__init__(self, 'c45', features, max_depth, min_sample, e, rf)


class CartCls(DT):
    def __init__(self, features, max_depth=sys.maxint, min_sample=1, rf=False):
        DT.__init__(self, 'cart', features, max_depth, min_sample, rf=rf)


class CartReg(DT):
    def __init__(self, features, max_depth=sys.maxint, min_sample=1, rf=False):
        DT.__init__(self, 'cart_r', features, max_depth, min_sample, rf=rf)


if __name__ == '__main__':
    data = [
        [u'青年', u'否', u'否', u'一般', u'否'],
        [u'青年', u'否', u'否', u'好', u'否'],
        [u'青年', u'是', u'否', u'好', u'是'],
        [u'青年', u'是', u'是', u'一般', u'是'],
        [u'青年', u'否', u'否', u'一般', u'否'],
        [u'中年', u'否', u'否', u'一般', u'否'],
        [u'中年', u'否', u'否', u'好', u'否'],
        [u'中年', u'是', u'是', u'好', u'是'],
        [u'中年', u'否', u'是', u'非常好', u'是'],
        [u'中年', u'否', u'是', u'非常好', u'是'],
        [u'老年', u'否', u'是', u'非常好', u'是'],
        [u'老年', u'否', u'是', u'好', u'是'],
        [u'老年', u'是', u'否', u'好', u'是'],
        [u'老年', u'是', u'否', u'非常好', u'是'],
        [u'老年', u'否', u'否', u'一般', u'否'],
    ]
    data1 = [[1, 4.5], [2, 4.75], [3, 4.91], [4, 5.34], [5, 5.80], [6, 7.05], [7, 7.90], [8, 8.23], [9, 8.70],
             [10, 9.00]]
    f = [u'年龄', u'有工作', u'有自己的房子', u'信贷情况']
    f1 = ['x']
    data = [
        [0, 1, 3, -1],
        [0, 3, 1, -1],
        [1, 2, 2, -1],
        [1, 1, 3, -1],
        [1, 2, 3, -1],
        [0, 1, 2, -1],
        [1, 1, 2, 1],
        [1, 1, 1, 1],
        [1, 3, 1, -1],
        [0, 2, 1, -1]
    ]
    f = [u'身体', u'业务', u'潜力']
    # classifier = ID3(f)
    # classifier = C45(f)
    classifier = CartCls(f, rf=True)
    w = [1.0] * len(data)
    # classifier = CartReg(f, rf=True)

    model = classifier.train(data, w)
    # print classify(model, [u'老年', u'否', u'是', u'非常好'])
    # print classifier.predict([5.5])

    model.show()
