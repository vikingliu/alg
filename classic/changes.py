# coding=utf-8


def combination(n, change=[], start=0, path=[]):
    """
       f(n,start) = Σ f(n - ci, i)   i = [start, len(change)]

    :param N:
    :param change: sorted change
    :param start: default is 0
    :param path:
    :return:
    """
    if n == 0:
        print(path)
        return

    for i in range(start, len(change)):
        item = change[i]
        if n >= item:
            combination(n - item, change, i, path + [item])


def get_combination_num(n, change=[], start=0):
    """

    :param n:
    :param change:
    :param start:
    :return:
    """
    if n == 0:
        return 1
    cnt = 0
    for i in xrange(start, len(change)):
        item = change[i]
        if n >= item:
            cnt += get_combination_num(n - item, change, i)
        else:
            break
    return cnt


def coin_change(amount, coins):
    """
    dp[i] = dp[i] + dp[i-c]
    :param amount:
    :param coins:
    :return:
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for i in range(c, amount + 1):
            dp[i] += dp[i - c]
    print(dp)
    return dp[amount]


print(coin_change(9, [1, 2, 5, 10]))
# print get_combination_num(9, [1, 2, 5, 10])
# combination(9, [1, 2, 5, 10])
