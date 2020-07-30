# coding=utf-8
import numpy as np

e = 1e-10


# L2正则化
def normalize_l2(x):
    x = x / np.sqrt(np.sum(x ** 2 + e, axis=1, keepdims=True))
    return x


# sigmoid: y = 1/(1 + exp(-x))
# σ(x) = 1/(1+exp(-x)
# σ'(x) = σ(x)(1-σ(x))
# [logσ(x)]' = 1 - σ(x)
# [log(1-σ(x))]' = -σ(x)
# 最大使然损失
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# tanh: y = (exp(x) - exp(-x))/(exp(x) + exp(-x))
def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))


# relu: y = max(0, x)
def relu(x):
    return np.maximum(0, x)


# softmax(zi) = exp(zi) / Σ exp(zj)
# 交叉熵损失 C = -Σyi * lnai,  ai = softmax(zi), yi in [0, 1] 分类结果
# 求导 i = j, ∂ai/∂zi = ai(1 - ai), i ≠ j  ai(zj)' = -aiaj
# ∂C/∂zi = -yi + ai * Σyj
# 对于分类问题，yi中只有一个1，其它全部0，C(zi)' = ai - 1
def softmax(x):
    orig_shape = x.shape
    if len(x.shape) > 1:
        x = x - np.max(x, axis=1, keepdims=True)
        exp_x = np.exp(x)
        x = exp_x / np.sum(exp_x, axis=1, keepdims=True)
    else:
        x = x - np.max(x, axis=0)
        exp_x = np.exp(x)
        x = exp_x / np.sum(exp_x, axis=0)
    assert x.shape == orig_shape
    return x


def batch_norm():
    pass


def layer_norm():
    pass
