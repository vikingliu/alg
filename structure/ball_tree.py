# coding=utf-8
import math


def cal_euclidean_dist(vec1, vec2):
    if vec1 and vec2 and len(vec1) == len(vec2):
        sum = 0
        for i in range(len(vec1)):
            sum += math.pow(vec1[i] - vec2[i], 2)
        return sum
    return 0


def get_circle(data):
    pass


class BallTree(object):
    def __init__(self, data):
        pass
