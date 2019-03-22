# coding=utf-8
import math
import sys

from decision_tree import CartCls
from ml import ML


class AdaBoost(ML):
    def __init__(self, g, max_m=10, min_e=0.01):
        self.m = max_m
        self.g = g
        self.min_e = min_e
        self.model = None

    def train(self, data):
        n = len(data)
        dm = [1.0 / n] * n
        fs = []
        pre_em = sys.maxint
        for i in range(self.m):
            em, alpha, gm, dm = self._train_g(data, dm, g)
            if em < self.min_e or pre_em - em < 0.01:
                break
            print em, alpha, dm
            fs.append((alpha, gm))
            g.model = None
            pre_em = em
        self.model = fs
        return fs

    def predict(self, test):
        if not self.model:
            return None
        rst = []
        for f in self.model:
            self.g.model = f[1]
            cls = f[0] * self.g.predict(test)
            rst.append(cls)
        return sum(rst)

    def _train_g(self, data, dm, g):
        gm = g.train(data, dm)
        em = g.error
        am = 0.5 * math.log((1 - em) / em)
        n = len(data)
        zm = sum([dm[i] * math.exp(-1 * am * data[i][-1] * g.predict(data[i])) for i in range(n)])
        dm_1 = [0] * n
        for i in range(n):
            dm_1[i] = dm[i] * math.exp(-1 * am * data[i][-1] * g.predict(data[i]))
            dm_1[i] /= zm
        return em, am, gm, dm_1

    def error(self, data, dm, g):
        e = 0
        for i, row in enumerate(data):
            y = g.predict(row)
            if y != row[-1]:
                e += dm[i]
        return e


class WeakCls(ML):
    def __init__(self):
        ML.__init__(self, 'weak')
        self.model = None
        self.error = 0

    def train(self, data, w=None):
        return self.min_split_error(data, w)

    def predict(self, test):
        for feature, split_v, val in self.model:
            if test[feature] <= split_v:
                return val
        return val

    def cal_error(self, data, c, w=None):
        e = 0
        for i, row in enumerate(data):
            if row[-1] != c:
                e += w[i]
        return e

    def sort_dw(self, data, feature, w=None):
        if not w:
            w = [1] * len(data)
        d_w = zip(data, w)
        d_w = sorted(d_w, key=lambda x: x[0][feature])
        data = []
        w = []
        for row in d_w:
            data.append(row[0])
            w.append(row[1])
        return data, w

    def min_split_error(self, data, w=None):
        for feature in range(len(data[0]) - 1):
            data, w = self.sort_dw(data, feature, w)
            split_v = self._split_v(data)
            n = len(data)
            min_error = sys.maxint
            split_data = None
            for s in split_v:
                r1 = data[0:s]
                r2 = data[s:n]
                if not r1 or not r2:
                    continue

                w1 = w[0:s]
                w2 = w[s:n]
                error1 = self.cal_error(r1, 1, w1) + self.cal_error(r2, -1, w2)
                error2 = self.cal_error(r1, -1, w1) + self.cal_error(r2, 1, w2)
                if error1 < error2:
                    c1 = 1
                    c2 = -1
                else:
                    c1 = -1
                    c2 = 1
                error = min(error1, error2)
                if error < min_error:
                    min_error = error
                    split_data = [(feature, data[s - 1][0], c1), (feature, data[s - 1][0], c2)]
        self.model = split_data
        self.error = min_error
        return self.model

    def _split_v(self, data):
        pre = None
        split_v = []
        for i, row in enumerate(data):
            if pre is None:
                pre = row
                continue
            if row[-1] == pre[-1]:
                continue

            split_v.append(i)
            pre = row
        return split_v


if __name__ == '__main__':
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
    features = ['身体', '业务', '潜力']

    # data = [
    #     [0, 1],
    #     [1, 1],
    #     [2, 1],
    #     [3, -1],
    #     [4, -1],
    #     [5, -1],
    #     [6, 1],
    #     [7, 1],
    #     [8, 1],
    #     [9, -1],
    # ]
    # features = ['x']
    # g = WeakCls()
    g = CartCls(features, max_depth=1)
    ada = AdaBoost(g)
    ada.train(data)
    print ada.predict([1, 1, 1])
