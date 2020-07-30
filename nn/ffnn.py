# coding=utf-8

import numpy as np


def ffnn(X, W_B_s, f):
    """

    :param X: input
    :param W_B_s: [(W0,b0),(W1,b1), ....(Wl, bl)]
    :param f: 激活函数，sigmod, relu, tanh等
    :return:
    """
    a = X
    for W, b in W_B_s:
        a = f(W.dot(a) + b)
    return a
