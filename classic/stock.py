def get_max_value(nums):
    s = 0
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            s += nums[i] - nums[i - 1]
    return s


print(get_max_value([1, 3, 2, 5, 9]))
