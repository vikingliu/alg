# coding=utf-8
'''
Given an expression in the form 2^i * 3^j * 5^k * 7^l where i,j,k,l >=0 are integers.
write a program to generate numbers from that equation in sorted order efficiently.
For example numbers from that expression will be in the order 1,2,3,4,5,6,7,8,9,10,12.....and so on..
'''
import math


def generate(cnt):
    n = 0
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
            print(i)
            n += 1
    print(n, n * math.log(n))


def generate_1(cnt):
    i = 0
    j = 0
    k = 0
    l = 0
    n = 0
    while n < cnt:
        v = (2 ** i) * (3 ** j) * (5 ** k) * (7 ** l)
        print(v)

        n += 1


def get_param(i, j, k, l):
    '''
      2 -> 3
      3 -> 2*2
      2*2 -> 5
      5 -> 2*3
      2*3 -> 7
      7 -> 2*2*2
      2*2*2 -> 3*3
      3*3 -> 2*5
      2*5 -> 2*2*3
      2*2*3 -> 3*5
      3*5 -> 2*2*2*2

      2*   2*2*2 -> 2*   3*3
      2*   3*3 -> 2*  2*5
      2*2*5 -> 3*7

    :param i:
    :param j:
    :param k:
    :param l:
    :return:
    '''


# generate(2000)
