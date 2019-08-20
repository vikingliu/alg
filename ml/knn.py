# coding=utf-8
import math
from heap import Heap, Node


class Tree:
    def __init__(self, dot, left, right):
        self.dot = dot
        self.left = left
        self.right = right

    def __str__(self):
        return '%s' % self.dot


def build_kd_tree(data, j=0):
    if not data:
        return None
    k = len(data[0])
    l = j % k + 1
    data = sorted(data, key=lambda x: x[l - 1])
    mid = len(data) / 2
    cur = data[mid]
    left_data = data[0: mid]
    right_data = data[mid + 1:]
    left = build_kd_tree(left_data, j + 1)
    right = build_kd_tree(right_data, j + 1)
    node = Tree(cur, left, right)
    return node


def search(x, kd_tree, j=0):
    if kd_tree is None:
        return None
    k = len(kd_tree.dot)
    l = j % k + 1
    if x[l - 1] < kd_tree.dot[l - 1]:
        k_cur_node = search(x, kd_tree.left, j + 1)
        other_node = kd_tree.right
    else:
        k_cur_node = search(x, kd_tree.right, j + 1)
        other_node = kd_tree.left
    if k_cur_node is None:
        return kd_tree
    cur_distance = calEuclideanDistance(x, kd_tree.dot)
    min_distance = calEuclideanDistance(x, k_cur_node.dot)

    if cur_distance < min_distance:
        k_cur_node = kd_tree
        min_distance = cur_distance

    if other_node:
        # cal the distance of other area
        other_distance = abs(x[l - 1] - kd_tree.dot[l - 1])
        if other_distance < min_distance:
            other_node = search(x, other_node, j + 1)
            if other_node:
                other_distance = calEuclideanDistance(x, other_node.dot)
                if other_distance < min_distance:
                    k_cur_node = other_node

    return k_cur_node


def search_k(x, kd_tree, k_node_heap, j=0):
    if kd_tree is None:
        return None
    k = len(kd_tree.dot)
    l = j % k + 1
    if x[l - 1] < kd_tree.dot[l - 1]:
        search_k(x, kd_tree.left, k_node_heap, j + 1)
        other_node = kd_tree.right
    else:
        search_k(x, kd_tree.right, k_node_heap, j + 1)
        other_node = kd_tree.left

    cur_distance = calEuclideanDistance(x, kd_tree.dot)

    if not k_node_heap.is_full() or k_node_heap.head().value > cur_distance:
        k_node_heap.add(Node(cur_distance, kd_tree))

    if other_node:
        # cal the distance of other area
        other_distance = abs(x[l - 1] - kd_tree.dot[l - 1])
        min_distance = k_node_heap.head().value
        if other_distance < min_distance or not k_node_heap.is_full():
            search_k(x, other_node, k_node_heap, j + 1)


def calEuclideanDistance(vec1, vec2):
    if vec1 and vec2 and len(vec1) == len(vec2):
        sum = 0
        for i in range(len(vec1)):
            sum += math.pow(vec1[i] - vec2[i], 2)
        return math.sqrt(sum)
    return 0


if __name__ == '__main__':
    data = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
    kd_tree = build_kd_tree(data)
    x = [6, 2]
    print search(x, kd_tree)
    k_node_heap = Heap(4)
    search_k(x, kd_tree, k_node_heap)
    print k_node_heap
