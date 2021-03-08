# coding=utf-8


def dfs(left, right, pre):
    if left == 0 and left == right:
        print(pre)

    if left > 0:
        dfs(left - 1, right, pre + '(')
    if right > left:
        dfs(left, right - 1, pre + ')')


def dfs_1(left, right, b_left, b_right, pre):
    if left == 0 and left == right and b_left == 0 and b_left == b_right:
        print(pre)

    if left == right:
        if b_left > 0:
            dfs_1(left, right, b_left - 1, b_right, pre + '[')
        if b_right > b_left and pre[-1] != '[':
            dfs_1(left, right, b_left, b_right - 1, pre + ']')
    if left > 0:
        dfs_1(left - 1, right, b_left, b_right, pre + '(')
    if right > left:
        dfs_1(left, right - 1, b_left, b_right, pre + ')')


def print_n_pair(n):
    dp = [''] * (n + 1)
    dp[0] = ['']
    # dp[i] = dp[0]dp[i-1] + dp[1]dp[i-2] + .... dp[i-1]dp[0]
    for i in range(1, n + 1):
        dp[i] = []
        for j in range(0, i):
            left = dp[j]
            right = dp[i - j - 1]
            for l in left:
                for r in right:
                    dp[i].append('(' + l + ')' + r)
    return dp[-1]





# print(print_n_pair(3))

# dfs_1(3, 3, 1, 1, '')
print(print_n_pair_1([1, 2, 3]))
