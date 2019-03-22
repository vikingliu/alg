# coding=utf-8

import random
import sys

import decision_tree
from ml import ML

"""
random tree
1. total N samples, bootstrap N
2. each node, random m features from M, sometimes m=sqrt(M) for category or m=1/3 M for regression
3. build decision tree
"""


class RandomForest(ML):
    def __init__(self):
        ML.__init__(self, 'Random Forest')
        pass


def bootstrap(D):
    train_d = []
    test_d = []
    train_i = []
    n = len(D)
    for i in range(n):
        r = random.randint(0, sys.maxint) % n
        train_d.append(D[r])
        train_i.append(r)

    train_i = set(train_i)
    for i in range(n):
        if i not in train_i:
            test_d.append(D[i])
    return train_d, test_d


def train(D, features=[]):
    forest = []
    for i in range(len(D)):
        train_d, test_d = bootstrap(D)
        tree = decision_tree.cart(train_d, features, rf=True)
        forest.append(tree)
    return forest


def predict_classify(forest, test):
    predict_cls = []
    for tree in forest:
        cls = decision_tree.classify(tree, test)
        predict_cls.append(cls)
    return decision_tree.max_cnt(predict_cls)


def predict_regression(forest, test):
    predict_reg = []
    for tree in forest:
        reg = decision_tree.regression(tree, test)
        predict_reg.append(reg)
    return 1.0 * sum(predict_reg) / len(predict_reg)


if __name__ == '__main__':
    D = range(100000)
    train(D)
