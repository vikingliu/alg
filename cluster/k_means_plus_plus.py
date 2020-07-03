# coding=utf-8

import numpy as np
import sys


# 加载数据
def load_data_set(file_name):
    data = np.loadtxt(file_name, delimiter='\t')
    return data


# 欧氏距离计算
def distEclud(x, y):
    return np.sqrt(np.sum((x - y) ** 2))  # 计算欧氏距离


# 为给定数据集构建一个包含K个随机质心的集合
def randCent(data):
    m, n = data.shape
    centroids = np.zeros((1, n))
    index = int(np.random.uniform(0, m))
    centroids[0, :] = data[index, :]
    return centroids


# k均值聚类
def kmeans(data, k):
    m = np.shape(data)[0]  # 行的数目
    # 第一列存样本属于哪一簇
    # 第二列存样本的到簇的中心点的误差
    clusterAssment = np.mat(np.zeros((m, 2), dtype=float))
    clusterChange = True

    # 第1步 初始化centroids
    centroids = randCent(data)
    while clusterChange and len(centroids) <= k:
        clusterChange = False
        # 遍历所有的样本（行数）
        max_dist = 0
        max_index = -1
        for i in range(m):
            min_dist = sys.maxsize
            min_index = -1

            # 遍历所有的质心
            # 第2步 找出最近的质心
            for j in range(len(centroids)):
                # 计算该样本到质心的欧式距离
                distance = distEclud(centroids[j, :], data[i, :])
                if distance < min_dist:
                    min_dist = distance
                    min_index = j
            # 第 3 步：更新每一行样本所属的簇
            if clusterAssment[i, 0] != min_index:
                clusterChange = True
            clusterAssment[i, :] = min_index, min_dist ** 2

            # 找到分裂点，离簇最远的点
            if min_dist > max_dist:
                max_dist = min_dist
                max_index = i

        # 第 4 步：更新质心
        for j in range(len(centroids)):
            pointsInCluster = data[np.nonzero(clusterAssment[:, 0].A == j)[0]]  # 获取簇类所有的点
            centroids[j, :] = np.mean(pointsInCluster, axis=0)  # 对矩阵的行求均值

        # 第 5 步： 距离最大的点分裂成一个新的簇
        if len(centroids) < k:
            centroids = np.insert(centroids, len(centroids), values=data[max_index, :], axis=0)
            clusterChange = True

    return clusterAssment, centroids


if __name__ == "__main__":
    data = np.array([
        [1, 1], [2, 1], [2, 2], [1, 2],
        [7, 8], [7, 7], [8, 8], [8, 7],
        [1, 8], [2, 8], [1, 9], [2, 9]
    ], dtype=float)

    print kmeans(data, 3)
