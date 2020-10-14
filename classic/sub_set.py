# coding=utf-8
import time


def cost(func):
    def cal(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        end = time.time()
        print(end - start)
        return res

    return cal


def sub_set(a, start=0):
    if a is None or start == len(a):
        return [[]]
    sub = sub_set(a, start + 1)
    sub += [[a[start]] + s for s in sub]
    return sub


@cost
def sub_set_0(a):
    return sub_set(a)


@cost
def sub_set_1(a):
    """
    二进制 0/1 对应 结合下标
    :param a:
    :return:
    """
    n = len(a)
    res = []
    for i in range(2 ** n):
        b = bin(i)[2:]
        sub = []
        for j, c in enumerate(b):
            if c == '1':
                sub.append(a[len(b) - j - 1])
        res.append(sub)
    return res


@cost
def sub_set_2(a):
    """
    二叉树深度遍历， 二进制 0/1
    :param a:
    :return:
    """
    rst = []

    def dfs(a, i, r=[]):
        if i == len(a):
            rst.append(list(r))
            return
        r.append(a[i])
        dfs(a, i + 1, r)
        r.pop()
        dfs(a, i + 1, r)

    dfs(a, 0)
    return rst


@cost
def sub_set_3(s):
    """
     f(n) = a[n]f(n-1) + f(n-1)
     f(0) = []
    :param s:
    :return:
    """
    rst = [[]]
    for item in s:
        rst += [[item] + sub for sub in rst]
    return rst


def sub_set_4(s):
    """
      f(n) = a[n]f(n-1) + a[n-1]f(n-2) ... + a[1]f(0) + f(0)
      f(0) = []
    :param s:
    :return:
    """
    rst = []

    def dfs(s, start, path=[]):
        rst.append(list(path))
        for i in xrange(start, len(s)):
            dfs(s, i + 1, path + [s[i]])

    dfs(s, 0)
    return rst


# print sub_set_2(range(10))
print(sub_set(range(3)))
