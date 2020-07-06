# coding=utf-8
import math
import numpy as np

eps = 1e-7


class Node(object):
    def __init__(self, center, radius, left=None, right=None, points=None):
        self.center = center
        self.radius = radius
        self.points = points
        self.left = left
        self.right = right


class BallTree(object):
    def __init__(self, data, leaf=10):
        if type(data) is list:
            data = np.array(data)
        self.leaf = leaf
        self.center, self.radius = self.__build(data)

    def __get_circle(self, data):
        n = len(data)
        radius = 0
        center = data[0, :]
        for i in range(1, n):
            pi = data[i]
            if not incircle(center, radius, pi):
                center = pi[:]
                radius = 0
                for j in range(i):
                    pj = data[j]
                    if not incircle(center, radius, pj):
                        center = (pi + pj) / 2.0
                        radius = dis(center, pi)
                        for k in range(j):
                            pk = data[k]
                            if not incircle(center, radius, pk):
                                center = get_circle(pi, pj, pk)
                                radius = dis(center, pi)
        return center, radius

    def __build(self, data):
        center, radius = self.__get_circle(data)
        node = Node(center, radius)
        if len(data) > self.leaf:
            # split

            pass
        else:
            node.points = data
        return node


def dis(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


def incircle(center, radius, x):
    if dis(center, x) < radius:
        return True
    return False


def get_circle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    a = x1 - x2
    b = y1 - y2
    c = x1 - x3
    d = y1 - y3

    theta = b * c - a * d
    if math.fabs(theta) < eps:
        dis12 = dis(p1, p2)
        dis23 = dis(p2, p3)
        dis13 = dis(p1, p3)
        max_dis = dis12
        center = (p1 + p2) / 2.0
        if max_dis > dis23:
            max_dis = dis23
            center = (p2 + p3) / 2.0
        if max_dis > dis13:
            center = (p1 + p3) / 2.0

        return center
    # a1 = ((x1 * x1 - x2 * x2) + (y1 * y1 - y2 * y2)) / 2.0
    a1 = np.sum(p1 ** 2 - p2 ** 2) / 2.0
    # a2 = ((x1 * x1 - x3 * x3) + (y1 * y1 - y3 * y3)) / 2.0
    a2 = np.sum(p1 ** 2 - p3 * 2) / 2.0
    x0 = (b * a2 - d * a1) / theta
    y0 = (c * a1 - a * a2) / theta
    return np.array([x0, y0])


if __name__ == '__main__':
    d = [[0, 0], [0, 4], [2, 2], [4, 4], [5, 5]]
    balltree = BallTree(d)
    print balltree.center, balltree.radius
