# coding=utf-8
import numpy as np


# gd
# gt = ▽J(θ)
# mt = φ(g1,g2,...gt)
# vt = ψ(g1,g2,...gt)

# θt+1 = θt - mt/sqrt(vt + ε)
# ε 为平滑项，防止分母为零，通常取 1e-8


# vanilla SGD
# mt = η * gt
# vt = I**2
# ε = 0
# θt+1 = θt - mt
# SGD 的缺点在于收敛速度慢，可能在鞍点处震荡
# 学习率η的选择也比较困难


def sgd(gt, eta, theta):
    mt = eta * gt
    theta = theta - mt
    return theta


# momentum

# mt = γ*mt-1 + η*gt
# θt+1 = θt - mt
# γ 通常取 0.9 左右
# 引入动量加速收敛

def sgd_m(gt, eta, theta_t, mt, gama=0.9):
    mt = gama * mt + eta * gt
    theta = theta_t - mt
    return theta, mt


# NAG: Nesterov Accelerated Gradient
# gt = ▽J(θ - γ*mt-1)
# mt = γ*mt-1 + η*gt
# θt+1 = θt - mt

def sgd_nag(gt, eta, theta, mt=0, gama=0.9):
    """

    :param gt:  ▽J(θ - γ*mt-1)
    :param eta: η
    :param theta: θt
    :param mt: mt-1
    :param gama: γ
    :return: theta, mt
    """
    mt = gama * mt + eta * gt
    theta = theta - mt
    return theta, mt


def sgd_nag_(gt, eta, theta, mt=0, gama=0.9):
    mt = gama * mt + eta * gt
    mt_ = gama * mt + eta * gt
    theta = theta - mt_
    return theta


# Adagrad
# mt = η*gt
# vt = diag(Σg1**2, Σg2**2, ... Σgt**2)
# θt+1 = θt - mt/sqrt(vt + ε)

def sgd_adagrad(diag_gt, gt, eta, theta, eps=1e-8):
    """

    :param diag_gt:  d*d的对角矩阵， gt一个d维向量

           每次计算完gt，更新diag_gt
           for i,v in enumerate(np.sqrt(gt)):
               diag_gt[i,i] = v
    :param gt: 梯度，d维度 向量
    :param eta: η 学习率
    :param theta: θt
    :param eps: ε
    :return: θt+1
    """
    mt = eta * gt
    vt = diag_gt
    theta = theta - mt / np.sqrt(vt + eps)
    return theta


# RMSprop
# mt = η*gt
# vt = γvt-1 + (1 - γ) diag(gt**2)
# θt+1 = θt - mt/sqrt(vt + ε)

def sgd_RMSprop(diag_gt, gt, eta, theta, vt=0, eps=1e-8, gama=0.9):
    mt = eta * gt
    vt = gama * vt + (1 - gama) * diag_gt
    theta = theta - mt / np.sqrt(vt + eps)
    return theta, vt


# Adam
# mt = η(β1*mt-1 + (1-β1)gt)
# vt = β2*vt-1 + (1 - β2)diag(gt**2)
# m0 = 0, v0 = 0
# mt' = mt / (1 - β1**t)
# vt' = vt / (1 - β2**t)
# θt+1 = θt - mt'/(sqrt(vt') + ε)

def sgd_adam(diag_gt, gt, theta, t=1, mt=0, vt=0, eta=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
    """

    :param diag_gt:
    :param gt:
    :param theta:
    :param t:
    :param mt:
    :param vt:
    :param eta: η = η / sqrt(t)
    :param beta1:
    :param beta2:
    :param eps:
    :return:
    """
    mt = eta * (beta1 * mt + (1 - beta1) * gt)
    vt = beta2 * vt + (1 - beta2) * diag_gt
    mt_ = mt / (1 - beta1 ** t)
    vt_ = vt / (1 - beta2 ** t)
    theta = theta - mt_ / np.sqrt(vt_ + eps)
    return theta, mt, vt


# NAdam
# NAG' + Adam
# --------
# NAG'
# gt = ▽J(θ)
# mt = γ*mt-1 + η*gt
# mt' = γ*mt + η*gt
# θt+1 = θt - mt'
# ---------
# mt = η(β1*mt-1 + (1-β1)gt)
# vt = β2*vt-1 + (1 - β2)diag(gt**2)
# m0 = 0, v0 = 0
# mt' = η(mt / (1 - β1**t+1) + (1 - β1)gt/(1 - β1**t))
# vt' = vt / (1 - β2**t)
# θt+1 = θt - mt'/(sqrt(vt') + ε)

def sgd_nadam(diag_gt, gt, theta, t=1, mt=0, vt=0, eta=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
    mt = eta * (beta1 * mt + (1 - beta1) * gt)
    vt = beta2 * vt + (1 - beta2) * diag_gt
    mt_ = eta * (mt / (1 - beta1 ** (t + 1)) + (1 - beta1) * gt / (1 - beta1 ** t))
    vt_ = vt / (1 - beta2 ** t)
    theta = theta - mt_ / np.sqrt(vt_ + eps)
    return theta, mt, vt
