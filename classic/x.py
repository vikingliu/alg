import copy
import numpy as np


def split_n_into_k_parts(n, k):
    x = n // k
    num = 1
    i = 0
    seq = []
    while i < k:
        if i < n - x * k:
            num *= (x + 1)
            seq.append(x + 1)
        else:
            num *= x
            seq.append(x)
        i += 1
    return num, seq


def split_n(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    start = np.max([1, n // 5])
    end = n // 2
    max_num = 1
    i = start
    max_seq = []
    while i <= end:
        s, seq = split_n_into_k_parts(n, i)
        if s > max_num:
            max_num = s
            max_seq = seq
        i += 1
    return max_num, max_seq


print(split_n(20))
