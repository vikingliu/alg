# coding = utf-8

from itertools import combinations
from collections import defaultdict
import numpy as np

logs = [
    [1, 'A', 5],
    [1, 'B', 3],
    [1, 'C', 2.5],

    [2, 'A', 2],
    [2, 'B', 2.5],
    [2, 'C', 5],
    [2, 'D', 2],

    [3, 'A', 2],
    [3, 'D', 4],
    [3, 'E', 4.5],
    [3, 'G', 5],

    [4, 'A', 5],
    [4, 'C', 3],
    [4, 'D', 4.5],
    [4, 'F', 4],

    [5, 'A', 4],
    [5, 'B', 3],
    [5, 'C', 2],
    [5, 'D', 4],
    [5, 'E', 3.5],
    [5, 'F', 4],
]


def get_matrix(logs):
    items = set()
    users = defaultdict(dict)
    for line in logs:
        user, item, score = line
        items.add(item)
        users[user][item] = score
    items = sorted(items)
    scores = [[0] * len(users) for _ in range(len(items))]
    co_occurrence = defaultdict(int)
    for j, value in enumerate(users.items()):
        for i, item in enumerate(items):
            if item in value[1]:
                scores[i][j] = value[1][item]
        sub_items = value[1].keys()
        for item in value[1].keys():
            co_occurrence[(item, item)] += 1
        for item1, item2 in combinations(sub_items, 2):
            co_occurrence[(item1, item2)] += 1
            co_occurrence[(item2, item1)] += 1

    A = [[0] * len(items) for _ in range(len(items))]

    for i, item1 in enumerate(items):
        for j, item2 in enumerate(items):
            A[i][j] = co_occurrence[(item1, item2)]

    return np.array(A), np.array(scores)


A, scores = get_matrix(logs)
print(A.dot(scores))
