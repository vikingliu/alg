# coding=utf-8
import math

from utils import cal_px_py_pxy


def pw(x, y, fn, wn, Y):
    z = 0
    n = len(fn)
    ele = math.exp(sum([wn[i] * fn[i](x, y) for i in range(n)]))
    for y in Y:
        z += math.exp(sum([wn[i] * fn[i](x, y) for i in range(n)]))
    return ele / z


def ep(fi, pxy):
    """
    Ep'(f) = sum(p'(x,y) f(x,y))
    :param f:
    :param x:
    :param y:
    :return:
    """
    rst = 0
    for px in pxy:
        for key, p in px.items():
            rst += p * fi(*key)
    return rst


def epw(fi, px, pxy, fn, wn, Y):
    """
    Epw(f) = sum(p'(x) pw(y|x) f(x,y))
    pw(y|x) = exp(sum(wi*fi(x,y))) / sum(exp(sum(wi*fi(x,y))))
    :param f:
    :param x:
    :param y:
    :return:
    """
    rst = 0
    for i, p_xy in enumerate(pxy):
        for key, p in p_xy.items():
            rst += px[i][key[0]] * pw(key[0], key[1], fn, wn, Y) * fi(*key)
    print rst, wn
    return rst


def cal_a(fn, pxy):
    max_c = 0
    for px in pxy:
        for key, p in px.items():
            c = sum([fi(*key) for fi in fn])
            max_c = max(max_c, c)
    return max_c


def gis(data, fn, wn, a=1, e=0.01):
    px, py, pxy = cal_px_py_pxy(data)
    if a == 1:
        a = cal_a(fn, pxy)
    ep_fn = [ep(fi, pxy) for fi in fn]
    Y = set([row[-1] for row in data])
    gis_train(fn, wn, ep_fn, px, pxy, Y, a, e)


def gis_train(fn, wn, ep_fn, px, pxy, Y, a, e):
    max_e = 0
    for i in range(len(fn)):
        delta = math.log(ep_fn[i] / epw(fn[i], px, pxy, fn, wn, Y))
        wn[i] += a * delta
        if delta > max_e:
            max_e = delta
    if max_e > e:
        gis_train(fn, wn, ep_fn, px, pxy, Y, a, e)


def iis(fn, wn, pxy, pw):
    pass


def f0(x, y, p_xy):
    if type(x) == int and x > 2:
        return 1
    elif x == 'M':
        return 1
    return 0


def f1(x, y, p_xy):
    if type(x) == int and x < 2:
        return 1
    elif x == 'S':
        return 1
    return 0


if __name__ == '__main__':
    n = 2
    wn = [1] * n
    data = [[1, 'S', -1], [1, 'M', -1], [1, 'M', 1], [1, 'S', 1], [1, 'S', -1],
            [2, 'S', -1], [2, 'M', -1], [2, 'M', 1], [2, 'L', 1], [2, 'L', 1],
            [3, 'L', 1], [3, 'M', 1], [3, 'M', 1], [3, 'L', 1], [3, 'L', -1]]

    gis(data, [f0, f1], wn)
    print wn
