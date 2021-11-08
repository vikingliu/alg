# coding=utf-8

def max_seq(nums):
    dp = [0] * len(nums)
    dp[0] = [nums[0]]
    for i in range(1, len(nums)):
        dp[i] = [nums[i]]
        for j in range(i):
            if nums[i] > dp[j][-1] and len(dp[j]) + 1 > len(dp[i]):
                dp[i] = dp[j] + [nums[i]]
    return dp


nums = [13, 9, 2, 5, 3, 6, 101, 18, 19]
print(max_seq(nums))
