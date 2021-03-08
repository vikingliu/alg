# coding=utf-8

'''
珂珂喜欢吃香蕉。这里有 N 堆香蕉，第 i 堆中有 piles[i] 根香蕉。警卫已经离开了，将在 H 小时后回来。
珂珂可以决定她吃香蕉的速度 K （单位：根/小时）。每个小时，她将会选择一堆香蕉，从中吃掉 K 根。如果这堆香蕉少于 K 根，她将吃掉这堆的所有香蕉，然后这一小时内不会再吃更多的香蕉。
珂珂喜欢慢慢吃，但仍然想在警卫回来前吃掉所有的香蕉。
返回她可以在 H 小时内吃掉所有香蕉的最小速度 K（K 为整数）
N=5

piles=[3,4,5,7,9]

H=7
'''
import math


def min_speed(piles, H):
    n = len(piles)
    rest = H - n
    start = n - rest - 1
    while start < n:
        min_v = piles[start]
        start += 1
        h = start
        for x in range(start, n):
            h += math.ceil(piles[x] / min_v)
            if h > H:
                break
        if h == H:
            return min_v

    return math.ceil(piles[-1] / (rest + 1))


piles = [3, 4, 5, 7, 25]
print(min_speed(piles, 7))
