# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal


def phi(data, mu_k, cov_k):
    """
    第 k 个模型的高斯分布密度函数
    每 i 行表示第 i 个样本在各模型中的出现概率
    :param data:
    :param mu_k:
    :param cov_k:
    :return:
    """
    norm = multivariate_normal(mean=mu_k, cov=cov_k)
    # norm = np.random.multivariate_normal(mean=mu_k, cov=cov_k)
    return norm.pdf(data)


def em_e(data, mu, cov, alpha):
    """
    E 步：计算每个模型对样本的响应度
    :param data: 为样本矩阵，每个样本一行，只有一个特征时为列向量
    :param mu: 为均值多维数组，每行表示一个样本各个特征的均值
    :param cov: 为协方差矩阵的数组
    :param alpha:  为模型响应度数组
    :return:
    """
    # 样本数
    N = data.shape[0]
    # 模型数
    K = alpha.shape[0]

    # 为避免使用单个高斯模型或样本，导致返回结果的类型不一致
    # 因此要求样本数和模型个数必须大于1
    assert N > 1, "There must be more than one sample!"
    assert K > 1, "There must be more than one gaussian model!"

    # 响应度矩阵，行对应样本，列对应响应度
    gamma = np.mat(np.zeros((N, K)))

    # 计算各模型中所有样本出现的概率，行对应样本，列对应模型
    prob = np.zeros((N, K))
    for k in range(K):
        prob[:, k] = phi(data, mu[k], cov[k])
    prob = np.mat(prob)

    # 计算每个模型对每个样本的响应度
    for k in range(K):
        gamma[:, k] = alpha[k] * prob[:, k]
    for i in range(N):
        gamma[i, :] /= np.sum(gamma[i, :])
    return gamma


# M 步：迭代模型参数
# Y 为样本矩阵，gamma 为响应度矩阵
def em_m(data, gamma):
    # 样本数和特征数
    N, D = data.shape
    # 模型数
    K = gamma.shape[1]

    # 初始化参数值
    mu = np.zeros((K, D))
    cov = []
    alpha = np.zeros(K)

    # 更新每个模型的参数
    for k in range(K):
        # 第 k 个模型对所有样本的响应度之和
        # sum(rik)
        Nk = np.sum(gamma[:, k])
        # 更新 mu
        # 对每个特征求均值
        for d in range(D):
            mu[k, d] = np.sum(np.multiply(gamma[:, k], data[:, d])) / Nk
        # 更新 cov
        cov_k = np.mat(np.zeros((D, D)))
        for i in range(N):
            cov_k += gamma[i, k] * (data[i] - mu[k]).T * (data[i] - mu[k]) / Nk
        cov.append(cov_k)
        # 更新 alpha
        alpha[k] = Nk / N
    cov = np.array(cov)
    return mu, cov, alpha


def norm(data):
    """
    数据预处理,将所有数据都缩放到 0 和 1 之间
    :param data:
    :return:
    """
    for i in range(data.shape[1]):
        max_ = data[:, i].max()
        min_ = data[:, i].min()
        data[:, i] = (data[:, i] - min_) / (max_ - min_)
    return data


def init_params(feature, k):
    """
    初始化模型参数
    :param shape: shape 是表示样本规模的二元组，(样本数, 特征数)
    :param K: 表示模型个数
    :return:

    """
    mu = np.random.rand(k, feature)
    cov = np.array([np.eye(feature)] * k)
    alpha = np.array([1.0 / k] * k)
    return mu, cov, alpha


def gmm_em(data, k, epoch):
    """
    高斯混合模型 EM 算法
    :param data: 给定样本矩阵 data，计算模型参数
    :param k: 为模型个数
    :param epoch: 为迭代次数
    :return: 每个样本的模型
    """
    data = norm(data)
    mu, cov, alpha = init_params(data.shape[1], k)
    for i in range(epoch):
        # 求当前模型参数下，各模型对样本的响应度矩阵
        gamma = em_e(data, mu, cov, alpha)
        mu, cov, alpha = em_m(data, gamma)

    # 对每个样本，求响应度最大的模型下标，作为其类别标识
    return gamma.argmax(axis=1).flatten().tolist()[0]


if __name__ == '__main__':

    # 载入数据
    data = np.loadtxt("../data/gmm.data")
    mat_data = np.mat(data)

    # 模型个数，即聚类的类别个数
    k = 3

    # 根据 GMM 模型，对样本数据进行聚类，一个模型对应一个类别
    categories = gmm_em(mat_data, k, 100)
    cls = {}
    # 将每个样本放入对应类别的列表中
    for i in range(len(categories)):
        if categories[i] not in cls:
            cls[categories[i]] = []
        cls[categories[i]].append(data[i])
    # 绘制聚类结果
    colors = ['rs', 'bo', 'go']
    for k, v in cls.items():
        v = np.array(v)
        plt.plot(v[:, 0], v[:, 1], colors[k], label="class%s" % (k + 1))

    plt.legend(loc="best")
    plt.title("GMM Clustering By EM Algorithm")
    plt.show()
