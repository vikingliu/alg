#coding=utf-8

# s(vi) = (1-d) + d * sum(1/|out(vj)| * s(vj)
# d = 0.85  s(vx) = 1

import numpy as np

d = 0.85
def cal_pr(m, pr, epoch=100):
    for i in range(epoch):
        pr = 1 - d + d * m.dot(pr)
        print(pr)
    return pr

if __name__ == '__main__':
    m = np.array([[0,1,1],[0,0,0],[0,0,0]])
    pr = np.array([1,1,1])
    cal_pr(m, pr)