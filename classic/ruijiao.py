# coding=utf-8
import math
import random


def simulation(N):
    obtuse, acute, right = 0, 0, 0
    for _ in range(N):
        theta = [random.random() * 2 * math.pi, random.random() * 2 * math.pi, random.random() * 2 * math.pi]
        theta.sort()
        theta_1, theta_2, theta_3 = theta
        side = [chord(theta_2 - theta_1), chord(theta_3 - theta_2), chord(2 * math.pi + theta_1 - theta_3)]
        side.sort()
        side_1, side_2, side_3 = side
        judgeFlag = judge(side_1, side_2, side_3)
        if judgeFlag == -1:
            acute += 1
        if judgeFlag == 1:
            obtuse += 1
        if judgeFlag == 0:
            right += 1
    return acute / N, obtuse / N, right / N


def chord(theta):
    if theta > math.pi:
        theta = 2 * math.pi - theta
    return 2 * math.sin(theta / 2)


def judge(s1, s2, s3):
    if s1 ** 2 + s2 ** 2 > s3 ** 2:
        return -1
    elif s1 ** 2 + s2 ** 2 < s3 ** 2:
        return 1
    else:
        return 0


acute, obtuse, right = simulation(1000000)
print('acute:\t{0}\nobtuse:\t{1}\nright:\t{2}\n'.format(acute, obtuse, right))
