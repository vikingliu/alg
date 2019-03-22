# coding=utf-8
import math
import sys

import decision_tree
from tree import Node


def simple_pruning(T, a, cost_func=decision_tree.H):
    """

    :param T: Tree
    :param a: a >= 0
    :param cost_func: H(D), Gini(D), square_error(D)
    :return:
    """
    c_ta = cost_func(T.sample) * len(T.sample)
    if not T.children:
        return c_ta

    c_tb = a * (len(T.children) - 1)
    for child in T.children.values():
        c_tb += simple_pruning(child, a)

    if c_ta <= c_tb:
        # prunning
        T.children = {}
        T.val = decision_tree.max_cnt(T.sample)
        return c_ta
    return c_tb


def rep(T, test):
    if not test:
        return 0
    if not T.children:
        error_cls = [item[-1] for item in test if item[-1] != T.val]
        return len(error_cls)
    error = 0

    if '#other' in T.children.keys() and len(T.children) == 2:
        di = {key: [] for key in T.children.keys()}

        for item in test:
            key = item[T.feature]
            if item[T.feature] not in di.keys():
                key = '#other'
            di[key].append(test)
    else:
        di = decision_tree.split(test, T.feature)
    for key, child in T.children.items():
        sub_test = di.get(key, [])
        error += rep(child, sub_test)
    cls = decision_tree.max_cnt(test)
    error_cls = [item[-1] for item in test if item[-1] != cls]
    error_pruning = len(error_cls)

    if error_pruning < error:
        T.children = {}
        T.val = cls
        return error_pruning
    return error


def pep(T):
    n = len(T.sample)
    e_leaf = len([item[-1] for item in T.sample if item[-1] != T.val]) + 0.5
    if not T.children:
        return e_leaf
    e_subtree = 0
    for child in T.children.values():
        e_subtree += pep(child)
    e = e_subtree / n
    se_subtree = math.sqrt(n * e * (1 - e))
    if e_leaf <= e_subtree - se_subtree:
        T.children = {}
        T.val = decision_tree.max_cnt(T.sample)
        return e_leaf
    return e_subtree


def mep(T):
    pass


def ccp(T, test, cost_func=decision_tree.Gini):
    gts = []
    _cal_pruning_a(T, cost_func, gts)
    # remove the root
    gts = gts[:-1]
    T.gt = None
    Tn = [T]
    gts.sort()
    for i, a in enumerate(gts):
        Tk = _pruning_a(Tn[i], a)
        Tn.append(Tk)
    best_T = None
    min_error = sys.maxint
    for model in Tn:
        error = decision_tree.predict_classify_error(model, test)
        if error < min_error:
            min_error = error
            best_T = model
    return best_T


def _pruning_a(T, a):
    # copy node
    node = Node(val=T.val, feature=T.feature, sample=T.sample, gt=T.gt)
    if T.gt == a:
        # pruning
        node.val = decision_tree.max_cnt(T.sample)
        node.feature = None
        return node
    children = {}
    if T.children:
        for key, child in T.children.items():
            children[key] = _pruning_a(child, a)
    if children:
        node.children = children
    return node


def _cal_pruning_a(T, cost_func=decision_tree.Gini, gts=[]):
    c_r = cost_func(T.sample) * len(T.sample)
    if not T.children:
        return c_r
    c_R = 0
    for child in T.children.values():
        c_R += _cal_pruning_a(child, cost_func, gts)
    gt = (c_r - c_R) / (len(T.children) - 1)
    T.gt = gt
    gts.append(gt)
    return c_R


def ebp(T, test):
    pass


def cvp(T):
    pass
