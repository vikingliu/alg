import numpy as np


def kmeans(ds, k):
    """k-means聚类算法

    k       - 指定分簇数量
    ds      - ndarray(m, n)，m个样本的数据集，每个样本n个属性值
    """

    m, n = ds.shape  # m：样本数量，n：每个样本的属性值个数
    result = np.empty(m, dtype=np.int)  # m个样本的聚类结果
    # cores = np.empty((k, n))  # k个质心
    cores = ds[np.random.choice(np.arange(m), k, replace=False)]  # 从m个数据样本中不重复地随机选择k个样本作为质心

    while True:  # 迭代计算
        d = np.square(np.repeat(ds, k, axis=0).reshape(m, k, n) - cores)
        distance = np.sqrt(np.sum(d, axis=2))  # ndarray(m, k)，每个样本距离k个质心的距离，共有m行
        index_min = np.argmin(distance, axis=1)  # 每个样本距离最近的质心索引序号

        if (index_min == result).all():  # 如果样本聚类没有改变
            return result, cores  # 则返回聚类结果和质心数据

        result[:] = index_min  # 重新分类
        for i in range(k):  # 遍历质心集
            items = ds[result == i]  # 找出对应当前质心的子样本集
            cores[i] = np.mean(items, axis=0)  # 以子样本集的均值作为当前质心的位置


# 欧氏距离计算
def distEclud(x, y):
    return np.sqrt(np.sum((x - y) ** 2))  # 计算欧氏距离


# 为给定数据集构建一个包含K个随机质心的集合
def randCent(dataSet, k):
    m, n = dataSet.shape
    centroids = np.zeros((k, n))
    used_index = set()
    for i in range(k):
        while True:
            index = int(np.random.uniform(0, m))
            if index not in used_index:
                break
        used_index.add(index)
        centroids[i, :] = dataSet[index, :]
    return centroids


# k均值聚类
def kmeans(dataSet, k):
    m = np.shape(dataSet)[0]  # 行的数目
    # 第一列存样本属于哪一簇
    # 第二列存样本的到簇的中心点的误差
    clusterAssment = np.mat(np.zeros((m, 2)))
    clusterChange = True

    # 第1步 初始化centroids
    centroids = randCent(dataSet, k)
    while clusterChange:
        clusterChange = False

        # 遍历所有的样本（行数）
        for i in range(m):
            minDist = 100000.0
            minIndex = -1

            # 遍历所有的质心
            # 第2步 找出最近的质心
            for j in range(k):
                # 计算该样本到质心的欧式距离
                distance = distEclud(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    minIndex = j
            # 第 3 步：更新每一行样本所属的簇
            if clusterAssment[i, 0] != minIndex:
                clusterChange = True
                clusterAssment[i, :] = minIndex, minDist ** 2
        # 第 4 步：更新质心
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == j)[0]]  # 获取簇类所有的点
            centroids[j, :] = np.mean(pointsInCluster, axis=0)  # 对矩阵的行求均值

    return clusterAssment.A[:, 0], centroids
