# coding=utf-8


def pow(n, m):
    if m == 0:
        return 1
    if m == 1:
        return n
    r = pow(n, m >> 1)
    r *= r
    if m % 2 == 1:
        r *= n
    return r


def pow_y(n, y):
    pass


def pow_x(n, m):
    x = int(m)
    y = m - x
    pow(n, x) * pow_y(n, y)


def pow_all(n, m):
    if m < 0:
        return 1 / pow_x(n, m * -1)
    return pow_x(n, m)
