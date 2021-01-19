# coding=utf-8

import random

s = 2 * 3.14


def get_ruijiao(n=10000):
    for i in range(n):
        p1 = random.random() % s
        p2 = random.random() % s
        p3 = random.random() % s
        p = [p1, p2, p3]
        p = sorted(p)
