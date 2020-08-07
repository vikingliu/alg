# coding=utf-8

e = 1e-15


def sqrt(n):
    left = 0
    right = n
    cnt = 0
    while True:
        mid = (left + right) / 2.0
        x = mid ** 2
        delta = abs(n - x)
        if delta < e:
            break
        if x > n:
            right = mid
        elif x == n:
            break
        else:
            left = mid
        cnt += 1
    return mid


def newton_sqrt(n):
    """
    f(x) = x^2 - n
    f'(x) = 2x
    xn+1 = xn - f(xn)/f'(xn)
         = xn - (xn^2 - n)/2xn
         = (xn + n/xn)/2

    :param n:
    :return:
    """
    r = n
    cnt = 0
    while abs(r ** 2 - n) > e:
        r = (r + n / r) / 2.0
        cnt += 1
    return r


print newton_sqrt(2)
