# coding=utf-8

from utils import cal_px_py_pxy


def train(data):
    return cal_px_py_pxy(data)


def predict(x, py, pxy):
    """
    p(y|x) = max(p(y) * II p(x\y)))
    :param x: input
    :param py:  p(y) stats from sample
    :param pxy: p(x|y) stats from sample
    :return: predict y
    """
    max_p = 0
    predict_y = 0
    for y, p in py.items():
        for i, v in enumerate(x):
            p *= pxy[i][(v, y)]
        if p > max_p:
            max_p = p
            predict_y = y
    return predict_y


if __name__ == '__main__':
    data = [[1, 'S', -1], [1, 'M', -1], [1, 'M', 1], [1, 'S', 1], [1, 'S', -1],
            [2, 'S', -1], [2, 'M', -1], [2, 'M', 1], [2, 'L', 1], [2, 'L', 1],
            [3, 'L', 1], [3, 'M', 1], [3, 'M', 1], [3, 'L', 1], [3, 'L', -1]]
    px, py, pxy = train(data)
    x = [2, 'S']
    print predict(x, py, pxy)
