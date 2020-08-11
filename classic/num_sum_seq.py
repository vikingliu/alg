# coding=utf-8

import math


def get_num_sum(s):
    n = len(s)
    for i in xrange(n / 2):
        num1 = s[0: i + 1]
        x = int(math.ceil((n + i) / 2.0))
        for j in xrange(i + 1, x):
            num2 = s[i + 1: j + 1]
            nums = get_sequence(num1, num2, s)
            print num1, num2, nums


def get_sequence(num1, num2, s):
    sub_s = num1 + num2
    nums = [int(num1), int(num2)]
    while len(sub_s) < len(s):
        num = nums[-1] + nums[-2]
        nums.append(num)
        sub_s += str(num)
    if sub_s == s:
        return nums
    return []


get_num_sum('199100199')
