# coding=utf-8

from numpy import *

from ml import ML
from collections import defaultdict


def loadDataSet(fileName):  # 构建数据库和标记库
    dataMat = [];
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))  # 只有一列
    return dataMat, labelMat


class SVM(ML):
    def __init__(self, C, toter, maxIter, kernel='linear'):
        ML.__init__(self, 'svm')
        self.kernel = kernel
        self.En = []
        self.C = C
        self.toter = toter
        self.maxIter = maxIter
        self.b = 0
        self.alphas = None
        self.kij = {}

    def train(self, data, w=None):
        self.smo(data)

    def predict(self, test):
        pass

    def Kij(self, data, i, j):
        return None

    def get_Ei(self, data, i):
        return None

    @staticmethod
    def selectJrand(i, m):  # 生成一个随机数
        j = i
        while j == i:
            j = int(random.uniform(0, m))  # 生成一个[0, m]的随机数，int转换为整数。注意，需要import random
        return j

    @staticmethod
    def clipAlpha(aj, H, L):  # 阈值函数
        if aj > H:
            aj = H
        if aj < L:
            aj = L
        return aj

    def smo(self, data_x, data_y, C, toler, maxIter):
        data = mat(data_x)
        y = mat(data_y).T
        b = 0
        m, n = shape(data)
        alphas = mat(zeros((m, 1)))
        iter = 0
        while iter < maxIter:  # 迭代次数
            alphaPairsChanged = 0
            for i in range(m):  # 在数据集上遍历每一个alpha
                # /*
                #  * 把违背KKT条件的ai作为第一个
                #  * 满足KKT条件的情况是：
                #  * yi*f(i) >= 1 and alpha == 0 (正确分类)
                #  * yi*f(i) == 1 and 0<alpha < C (在边界上的支持向量)
                #  * yi*f(i) <= 1 and alpha == C (在边界之间)
                #  *
                #  * ri = y[i] * Ei = y[i] * f(i) - y[i]^2 = y[i]*f(i) - 1>= 0
                #  * 如果ri < 0 并且alpha < C 则违反了KKT条件
                #  * 因为原本ri < 0 应该对应的是alpha = C
                #  * 同理，ri > 0并且alpha > 0则违反了KKT条件
                #  * 因为原本ri > 0对应的应该是alpha =0
                #  * f(i) = sum(alpha[j]*y[j]*Kji) + b
                #  */
                fxi = float(multiply(alphas, y).T * (data * data[i, :].T)) + b
                Ei = fxi - float(y[i])
                ri = y[i] * Ei
                if ((ri < -toler) and (alphas[i] < C)) or ((ri > toler) and (alphas[i] > 0)):
                    # /*
                    # * f(i)*yi=1边界上的点 0 < a[i] < C
                    # * 找MAX|E1 - E2|
                    # */
                    j = self.selectJrand(i, m)  # 从m中选择一个随机数，第2个alpha j
                    fxj = float(multiply(alphas, y).T * data * data[j, :].T) + b
                    Ej = fxj - float(y[j])

                    alphaIold = alphas[i].copy()  # 复制下来，便于比较
                    alphaJold = alphas[j].copy()

                    if y[i] != y[j]:  # 开始计算L和H
                        L = max(0, alphas[j] - alphas[i])
                        H = min(C, C + alphas[j] - alphas[i])
                    else:
                        L = max(0, alphas[j] + alphas[i] - C)
                        H = min(C, alphas[j] + alphas[i])
                    if L == H:
                        print 'L==H'
                        continue

                    # eta是alphas[j]的最优修改量，如果eta为零，退出for当前循环
                    # eta = Kii + Kjj - 2 * Kij
                    eta = 2.0 * data[i, :] * data[j, :].T - \
                          data[i, :] * data[i, :].T - \
                          data[j, :] * data[j, :].T
                    if eta >= 0:
                        print 'eta>=0'
                        continue
                    # alpha[j]new,unc = alpha[j]old + y[j](Ei - Ej)/eta
                    alphas[j] -= y[j] * (Ei - Ej) / eta  # 调整alphas[j]
                    # L <= alpha[j]new <= H
                    alphas[j] = self.clipAlpha(alphas[j], H, L)
                    if abs(alphas[j] - alphaJold) < 0.00001:
                        # 如果alphas[j]没有调整
                        print 'j not moving enough'
                        continue
                    # alpha[i]new = alpha[i]old + y[i]*y[j](alpha[j]old - alpha[j]new)
                    alphas[i] += y[j] * y[i] * (alphaJold - alphas[j])

                    # b1new = bold - Ei - y[i]*Kii*(alpha[i]new - alpha[i]old) - y[j]*Kji*(alpha[j]new - alpha[j]old)
                    b1 = b - Ei - y[i] * (alphas[i] - alphaIold) * \
                                  data[i, :] * data[i, :].T - \
                         y[j] * (alphas[j] - alphaJold) * \
                         data[i, :] * data[j, :].T
                    # b2new = bold - Ej - y[i]*Kij*(alpha[i]new - alpha[i]old) - y[j]*Kjj*(alpha[j]new - alpha[j]old)
                    b2 = b - Ej - y[i] * (alphas[i] - alphaIold) * \
                                  data[i, :] * data[j, :].T - \
                         y[j] * (alphas[j] - alphaJold) * \
                         data[j, :] * data[j, :].T

                    if 0 < alphas[i] < C:
                        b = b1
                    elif 0 < alphas[j] < C:
                        b = b2
                    else:
                        b = (b1 + b2) / 2.0
                    alphaPairsChanged += 1

                    print 'iter: %d i: %d, pairs changed %d' % (iter, i, alphaPairsChanged)
            if alphaPairsChanged == 0:
                iter += 1
            else:
                iter = 0
            print 'iteration number: %d' % iter
        return b, alphas


if __name__ == "__main__":
    dataArr, labelArr = loadDataSet('testSet.txt')
    b, alphas = smoSimple(dataArr, labelArr, 0.6, 0.001, 40)

    print b, alphas
