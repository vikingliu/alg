# coding=utf-8
import collections
import random


def get_max_v_index(nums):
    max_v = nums[0]
    max_indexs = [0]
    for i in range(1, len(nums)):
        if nums[i] > max_v:
            max_v = nums[i]
            max_indexs = [i]
        elif nums[i] < max_v:
            continue
        else:
            max_indexs.append(i)
    return max_indexs


indexs = get_max_v_index([6, 4, 3, 2, 6, 6, 3, 6, 5, 6])
stats = collections.defaultdict(int)

for _ in range(10000):
    i = random.choice(indexs)
    stats[i] += 1
print(stats)
