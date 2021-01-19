# coding=utf-8

import collections


def get_pairs(nums, s):
    '''

    :param nums:
    :param s:
    :return:
    '''
    pre = set()
    pair = []
    for n in nums:
        diff = s - n
        if diff in pre:
            pair.append((diff, n))
        if n not in pre:
            pre.add(n)
    return pair


def get_pairs_dup(nums, s):
    '''
     计算所有和为s的pair， nums 有重复的数据，每个数只能用一次
    :param nums:
    :param s: target sum
    :return: all pairs
    '''
    pre = collections.defaultdict(int)
    pair = []
    for n in nums:
        diff = s - n
        if pre[diff] > 0:
            pair.append((diff, n))
            pre[diff] -= 1
        pre[n] += 1
    return pair


nums = [1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 0, -1, 7]

print(get_pairs_dup(nums, 6))
