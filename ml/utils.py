import math
from collections import defaultdict


def cal_px_py_pxy(data):
    """
    stats from data, cal p(x), p(y), p(x|y)
    :param data: [x1, x2, x3....,y]
    :return: p(x), p(y), p(x|y)
    """
    x_n = range(len(data[0]) - 1)
    py = defaultdict(int)
    pxy = [defaultdict(int) for i in x_n]
    px = [defaultdict(int) for i in x_n]
    for row in data:
        y = row[-1]
        py[y] += 1
        for i, x in enumerate(row[0:-1]):
            pxy[i][(x, y)] += 1
            px[i][x] += 1

    for y, n in py.items():
        for i, item in enumerate(px):
            for x in item.keys():
                pxy[i][(x, y)] /= n * 1.0
        py[y] /= len(data) * 1.0

    for i, item in enumerate(px):
        for x in item.keys():
            px[i][x] /= len(data) * 1.0

    return px, py, pxy


def sample_w(data, w=None):
    if not w:
        return data
    if not data:
        return None
    if len(data) != len(w):
        return data

    min_w = min(w)
    new_data = []
    for i, row in enumerate(data):
        n = int(math.ceil(w[i] * 1.0 / min_w))
        for j in range(n):
            new_data.append(row[:])
    return new_data
