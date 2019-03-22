# coding=utf-8

import math
import sys

import decision_tree
from ml import ML


class BoostingTree(ML):
    def __init__(self, classify=True):
        ML.__init__(self, 'BoostingTree')
        self.classify = classify
        self.fm = []

    def train(self, data, e=0.1, max_m=100, w=None):
        lost = sys.maxint
        m = 0
        while lost > e and m < max_m:
            m += 1
            fi = self._train(data)
            if self.classify:
                pass
            else:
                lost = self.regression_fit(fi, data)
            self.fm.append(fi)
            print m, lost

    def predict(self, test):
        rst = []
        for fi in self.fm:
            if test[fi['split_feature']] <= fi['split_f_v']:
                rst.append(fi['split_v'][0])
            else:
                rst.append(fi['split_v'][1])
        if self.classify:
            return decision_tree.max_cnt(rst)
        else:
            return sum(rst)

    def _train(self, data):
        min_split_error = sys.maxint
        split_feature = None
        split_data = None
        for feature in range(len(data[0]) - 1):
            if self.classify:
                min_error, split_D = decision_tree.min_Gini(data, feature)
            else:
                min_error, split_D = decision_tree.min_square_error(data, feature)

            if min_error < min_split_error:
                split_feature = feature
                min_split_error = min_error
                split_data = split_D
        split_v = []
        split_f_v = None
        for key in split_D.keys():
            val = sum([row[-1] for row in split_D[key]]) * 1.0 / len(split_D[key])
            split_D[key] = val
            if '<=' in key:
                split_f_v = float(key.replace('<=', ''))
                split_v.insert(0, val)
            elif '#other' in key:
                split_v.insert(0, val)
            else:
                split_v.append(val)
        return dict(split_feature=split_feature, split_f_v=split_f_v, split_v=split_v, split_D=split_data)

    @staticmethod
    def regression_fit(fm, data):
        lost = 0
        for row in data:
            if row[fm['split_feature']] <= fm['split_f_v']:
                row[-1] -= fm['split_v'][0]
            else:
                row[-1] -= fm['split_v'][1]
            lost += math.pow(row[-1], 2)
        return lost

    @staticmethod
    def classify_fit(fm, data):
        pass


if __name__ == '__main__':
    data = [
        [1, 5.56],
        [2, 5.70],
        [3, 5.91],
        [4, 6.40],
        [5, 6.80],
        [6, 7.05],
        [7, 8.90],
        [8, 8.70],
        [9, 9.00],
        [10, 9.05]
    ]
    featrues = ['x']
    bt = BoostingTree(classify=False)
    bt.train(data, e=0.01)
    print bt.predict([3])
