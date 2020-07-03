# coding=utf-8
import math
import sys
from heap import Heap, Node


# 一般kd树要求数据维度在20维以内。
# 通常原则是，如果维度是k, 数据点数是N， 需要满足N >> 2k
class KdNode:
    def __init__(self, point, left, right):
        self.point = point
        self.left = left
        self.right = right

    def __str__(self):
        return '%s' % self.point


class KdTree(object):
    def __init__(self, data):
        self.root = self.build_tree(data)

    def search(self, point):
        return self._search(point, self.root)

    def search_k(self, point, k):
        k_node_heap = Heap(k)
        self._search_k(point, self.root, k_node_heap)
        return k_node_heap

    def search_range(self, point, r):
        rst = []
        self._search_range(point, self.root, rst, r)
        return rst

    def build_tree(self, data, deep=0):
        if not data:
            return None
        n = len(data[0])
        v = deep % n
        data = sorted(data, key=lambda x: x[v])
        mid = len(data) / 2
        point = data[mid]
        left_data = data[0: mid]
        right_data = data[mid + 1:]
        left = self.build_tree(left_data, deep + 1)
        right = self.build_tree(right_data, deep + 1)
        node = KdNode(point, left, right)
        return node

    def _search(self, point, kd_tree, deep=0):
        if kd_tree is None:
            return None, sys.maxsize
        n = len(kd_tree.point)
        v = deep % n
        if point[v] < kd_tree.point[v]:
            k_cur_node, min_dist = self._search(point, kd_tree.left, deep + 1)
            other_node = kd_tree.right
        else:
            k_cur_node, min_dist = self._search(point, kd_tree.right, deep + 1)
            other_node = kd_tree.left

        cur_dist = self.cal_euclidean_dist(point, kd_tree.point)

        if cur_dist < min_dist:
            k_cur_node = kd_tree
            min_dist = cur_dist

        if other_node:
            # cal the distance of other area
            other_dist = abs(point[v] - kd_tree.point[v])
            if other_dist < min_dist:
                other_node, other_dist = self._search(point, other_node, deep + 1)
                if other_node:
                    if other_dist < min_dist:
                        k_cur_node = other_node
                        min_dist = other_dist

        return k_cur_node, min_dist

    def _search_k(self, point, kd_tree, k_node_heap, deep=0):
        if kd_tree is None:
            return None
        n = len(kd_tree.point)
        v = deep % n
        if point[v] < kd_tree.point[v]:
            self._search_k(point, kd_tree.left, k_node_heap, deep + 1)
            other_node = kd_tree.right
        else:
            self._search_k(point, kd_tree.right, k_node_heap, deep + 1)
            other_node = kd_tree.left

        cur_dist = self.cal_euclidean_dist(point, kd_tree.point)

        if not k_node_heap.is_full() or k_node_heap.head().value > cur_dist:
            k_node_heap.add(Node(cur_dist, kd_tree))

        if other_node:
            # cal the distance of other area
            other_dist = abs(point[v] - kd_tree.point[v])
            min_dist = k_node_heap.head().value
            if other_dist < min_dist or not k_node_heap.is_full():
                self._search_k(point, other_node, k_node_heap, deep + 1)

    def _search_range(self, point, kd_tree, rst, r, deep=0):
        if kd_tree is None:
            return None
        n = len(kd_tree.point)
        v = deep % n
        if point[v] < kd_tree.point[v]:
            self._search_range(point, kd_tree.left, rst, r, deep + 1)
            other_node = kd_tree.right
        else:
            self._search_range(point, kd_tree.right, rst, r, deep + 1)
            other_node = kd_tree.left

        cur_dist = self.cal_euclidean_dist(point, kd_tree.point)

        if cur_dist <= r:
            rst.append((cur_dist, kd_tree))

        if other_node:
            # cal the distance of other area
            other_dist = abs(point[v] - kd_tree.point[v])
            if other_dist <= r:
                self._search_range(point, other_node, rst, r, deep + 1)

    def cal_euclidean_dist(self, vec1, vec2):
        if vec1 and vec2 and len(vec1) == len(vec2):
            sum = 0
            for i in range(len(vec1)):
                sum += math.pow(vec1[i] - vec2[i], 2)
            return math.sqrt(sum)
        return 0
