# coding=utf-8

'''
一个m行n列的迷宫，迷宫左上角是入口，右下角是出口，每次只能向下或者向右走一格，问从入口到出口总共有多少种走法


'''


def f(n, m):
    n += 1
    m += 1
    dp = [[1] * m for _ in range(n)]
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[-1][-1]


print(f(3, 3))
