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


def max_sum(data):
    s = 0
    max_s = sys.maxint * -1
    for item in data:
        if s > 0:
            s += item
        else:
            s = item
        max_s = max(s, max_s)
    return max_s


def max_sum_subset(data):
    if not data:
        return None
    n = len(data)
    dp = [0] * n
    dp[0] = data[0]
    if n == 1:
        return dp[0]
    dp[1] = max(data[0], data[1])
    if n == 2:
        return dp[1]
    for i in range(2, len(data)):
        dp[i] = max(data[i], dp[i - 1], dp[i - 2] + data[i])
    return dp[-1]


print max_sum_subset([10, 6, 3, 8])
