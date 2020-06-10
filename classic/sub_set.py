import math
import time


def cost(func):
    def cal(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        end = time.time()
        print end - start
        return res

    return cal


def sub_set(a, start=0):
    if a is None or start == len(a):
        return []
    res = []
    v = a[start]
    sub = sub_set(a, start + 1)
    res.append([v])
    for item in sub:
        new_item = list(item)
        new_item.append(v)
        res.append(item)
        res.append(new_item)
    return res


@cost
def sub_set_0(a):
    return sub_set(a)


@cost
def sub_set_1(a):
    n = len(a)
    res = []
    for i in range(2**n):
        b = bin(i)[2:]
        sub = []
        for j, c in enumerate(b):
            if c == '1':
                sub.append(a[len(b) - j - 1])
        res.append(sub)
    return res

@cost
def sub_set_2(a):
    rst = []
    def dfs(a, i , r=[]):
        if i == len(a):
            rst.append(list(r))
            return
        r.append(a[i])
        dfs(a, i+1, r)
        r.pop()
        dfs(a, i+1, r)
    dfs(a, 0)
    return rst
@cost
def sub_set_3(a):
    rst = [[]]
    for item in a:
        temp = []
        for cur in rst:
            temp.append(cur + [item])
        rst += temp
    return rst

#print sub_set_2(range(10))
print sub_set_3(range(3))
