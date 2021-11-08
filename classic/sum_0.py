# coding=utf-8


def get_comp(nums, i, pre, pre_sum, res):
    if i == len(nums):
        if pre and sum(pre) == 0:
            res.append(pre.copy())
        return
    if -nums_sum[i] <= pre_sum <= nums_sum[i]:
        get_comp(nums, i + 1, pre + [nums[i]], pre_sum + nums[i], res)
        get_comp(nums, i + 1, pre + [-nums[i]], pre_sum - nums[i], res)
        get_comp(nums, i + 1, pre, pre_sum, res)


res = []
nums = [-2, 3, 2, 1, 4, 2]
n = len(nums)
nums_sum = [0] * len(nums)
s = 0

for i in range(n - 1, -1, -1):
    s += abs(nums[i])
    nums_sum[i] = s
print(nums_sum)

get_comp(nums, 0, [], 0, res)
print(res)
