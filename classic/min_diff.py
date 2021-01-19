# coding=utf-8
import sys

min_diff = sys.maxsize


def get_min_diff(nums, i, pre_sum, pre_len, total):
    global min_diff
    if i == len(nums):
        diff = abs(total - pre_sum * 2)
        if pre_len < len(nums) and diff < min_diff:
            min_diff = diff
            print(min_diff, pre_sum, total)
        return

    get_min_diff(nums, i + 1, pre_sum + nums[i], pre_len + 1, total)
    get_min_diff(nums, i + 1, pre_sum, pre_len, total)


nums = [1, 2, 3, 5]
get_min_diff(nums, 0, 0, 0, sum(nums))
print(min_diff)
