# coding=utf-8
'''
Given an expression in the form 2^i * 3^j * 5^k * 7^l where i,j,k,l >=0 are integers.
write a program to generate numbers from that equation in sorted order efficiently.
For example numbers from that expression will be in the order 1,2,3,4,5,6,7,8,9,10,12.....and so on..
'''
import math
import time


def generate(cnt):
    s = time.time()
    res = []
    for i in range(1, cnt + 1):
        find = True
        x = i
        while x > 1 and find:
            find = False
            if x % 2 == 0:
                x = x // 2
                find = True

            if x % 3 == 0:
                x = x // 3
                find = True

            if x % 5 == 0:
                x = x // 5
                find = True

            if x % 7 == 0:
                x = x // 7
                find = True
        if x == 1:
            res.append(i)
    print(time.time() - s)
    print(len(res), res)


def generate_fast(cnt):
    s = time.time()
    res = []
    l = int(math.log(cnt, 7))
    for v in range(l + 1):
        v_7 = 7 ** v
        k = int(math.log(cnt // v_7, 5))
        for z in range(k + 1):
            k_5 = v_7 * 5 ** z
            j = int(math.log(cnt // k_5, 3))
            for y in range(j + 1):
                j_3 = k_5 * 3 ** y
                i = int(math.log(cnt // j_3, 2))
                for x in range(i + 1):
                    i_2 = j_3 * 2 ** x
                    res.append(i_2)
    res = sorted(res)
    print(time.time() - s)
    print(len(res), res)


generate(20000)
generate_fast(20000)
