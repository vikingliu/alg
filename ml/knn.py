# coding=utf-8
import sys

sys.path.append('..')
from structure.kd_tree import KdTree

if __name__ == '__main__':
    data = [[2, 3, 5], [5, 4, 6], [9, 6, 8], [4, 7, 0], [8, 1, 3], [7, 2, 5]]
    kd_tree = KdTree(data)
    point = [6, 2, 1]
    node, dist = kd_tree.search(point)
    print node, dist
    k_node_heap = kd_tree.search_k(point, 4)
    print k_node_heap

    rst = kd_tree.search_range(point, 4.2)
    for node, dist in rst:
        print node, dist, ';',
