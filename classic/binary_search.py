# coding=utf-8

def bin_search(nums, v):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == v:
            return mid
        elif nums[mid] > v:
            right = mid - 1
        elif nums[mid] < v:
            left = mid + 1

    return -1


def move_bin_search(nums, v):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == v:
            return mid
        elif nums[left] < nums[right]:
            if nums[mid] > v:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[left] > nums[mid]:
            if nums[mid] > v or nums[left] <= v:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < v or nums[left] > v:
                right = mid - 1
            else:
                left = mid + 1
    return -1


def move_bin_search_1(nums, v):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == v:
            return mid
        elif nums[left] < nums[right] and nums[mid] > v:
            right = mid - 1
        elif nums[left] > nums[mid] and (nums[mid] > v or nums[left] <= v):
            right = mid - 1
        elif nums[left] < nums[mid] and (nums[mid] < v or nums[left] > v):
            right = mid - 1
        else:
            left = mid + 1
    return -1


nums = range(0, 10, 2)
for n in nums:
    pos = bin_search(nums, n)
    print(pos, n, nums[pos])

print('--------------')
nums = [10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6, 7]
for n in nums:
    pos = move_bin_search(nums, n)
    print(pos, n, nums[pos])
