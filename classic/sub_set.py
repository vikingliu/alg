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
    for i in range(int(math.pow(2, n))):
        b = bin(i)[2:]
        sub = []
        for j, c in enumerate(b):
            if c == '1':
                sub.append(a[len(b) - j - 1])
        res.append(sub)
    return res


print sub_set_1([1, 2, 3])
