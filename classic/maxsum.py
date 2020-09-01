import sys


class Node:
    def __init__(self, val, left, right):
        self.left = left
        self.right = right
        self.val = val


def tree_max_sum(tree):
    global_max_v = sys.maxint * -1

    def max_sum(root):
        global global_max_v
        if root is None:
            return 0

        left = max_sum(root.left)
        right = max_sum(root.right)
        max_v = max(left, right)
        max_v = max(max_v, 0) + root.val
        global_max_v = max(max_v, global_max_v)

    max_sum(tree)
    return global_max_v


def max_sum(arr):
    # sum[i] = max(sum[i-1] + arr[i], arr[i])
    # res = max(sum)
    s = 0
    max_s = sys.maxint * -1
    for item in arr:
        s = max(s, 0) + item
        max_s = max(s, max_s)
    return max_s


def max_sum_subset(arr):
    if not arr:
        return None
    n = len(arr)
    dp = [0] * n
    dp[0] = arr[0]
    if n == 1:
        return dp[0]
    dp[1] = max(arr[0], arr[1])
    if n == 2:
        return dp[1]
    for i in range(2, n):
        dp[i] = max(arr[i], dp[i - 1], dp[i - 2] + arr[i])
    return dp[-1]


def max_multi(arr):
    # max_v[i] = max(max_v[i-1] * arr[i], min_v[i-1], arr[i])
    # min_v[i] = min(max_v[i-1] * arr[i], min_v[i-1], arr[i])
    max_v = 1
    min_v = 1

    max_res = sys.maxint * -1
    for item in arr:
        max_tmp = max_v
        max_v = max(max_v * item, min_v * item, item)
        min_v = min(max_tmp * item, min_v * item, item)
        max_res = max(max_v, max_res)
    return max_res


print(max_sum_subset([10, 6, 3, 8]))
