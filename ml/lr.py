# coding=utf-8

import math

import numpy as np


def g(wx):
    return 1 / (1 + math.exp(-1 * wx))


def gradient_descent(x, y, w, a, max_iteration=10):
    for i in range(max_iteration):
        A = np.dot(x, w)
        gA = [g(ai) for ai in A]
        w -= a * x.T * (gA - y)
    return w


if __name__ == '__main__':
    pass
