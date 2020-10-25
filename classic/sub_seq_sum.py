import sys


def get_sum(A):
    dp = [0] * len(A)
    dp[0] = A[0]
    dp[1] = max(A[0], A[1])
    for i in range(2, len(A)):
        dp[i] = max(dp[i - 2] + A[i], A[i], dp[i - 1])
    return dp[-1]


def get_sum_1(A):
    dp = [[0] * 2 for i in range(len(A))]
    dp[0][0] = -sys.maxsize
    dp[0][1] = A[0]
    for i in range(1, len(A)):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1])
        dp[i][1] = max(dp[i - 1][0] + A[i], A[i])
    return max(dp[-1][0], dp[-1][1])


print(get_sum_1([-3,-2,-1]))
