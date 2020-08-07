# coding=utf-8
import sys

sys.path.append('..')
from utils import nn_utils


# RNN

# Elam Network
# ht = σh(Wh * xt + Uh * ht-1 + bh)
# yt = σy(Wy * ht + by)

# Jordan Network
# ht = σh(Wh * x + Uh * yt-1 + bh)
# yt = σy(Wy * ht + by)

# xt: input vector
# ht: hidden layer vector
# yt: output vector

def elam_rnn(xt, Wh, Wy, ht_1, bh, by):
    ht = nn_utils.relu(Wh * (xt, ht_1) + bh)
    yt = nn_utils.relu(Wy * ht + by)
    return ht, yt


def jordan_rnn(xt, Wh, Wy, yt_1, bh, by):
    ht = nn_utils.relu(Wh * (xt, yt_1) + bh)
    yt = nn_utils.relu(Wy * ht + by)
    return ht, yt


# LSTM

# ft = σ(Wf * [ht-1, xt] + bf) 遗忘门
# it = σ(Wi * [ht-1, xt] + bi) 输入们
# ot = σ(Wo * [ht-1, xt] + bo) 输出们
# ct = ft * ct-1 + it * tanh(Wc[ht-1, xt] + bc)  细胞状态
# ht = ot * tanh(ct) 隐层


def lstm(xt, ct_1, ht_1, Wf, bf, Wi, bi, Wo, bo, Wc, bc):
    ft = nn_utils.sigmoid(Wf * (ht_1, xt) + bf)
    it = nn_utils.sigmoid(Wi * (ht_1, xt) + bi)
    ot = nn_utils.sigmoid(Wo * (ht_1, xt) + bo)
    ct = ft * ct_1 + it * nn_utils.tanh(Wc * [ht_1, xt] + bc)
    ht = ot * nn_utils.tanh(ct)
    return ct, ht


# GRU
# zt = σ(Wz * [ht-1, xt])
# rt = σ(Wr * [ht-1, xt])
# ht' = tanh(Wh * [rt * ht-1, xt])
# ht = (1-zt) * ht-1 + zt * ht'

# 比lstm 参数

def gru(xt, ht_1, Wz, Wr, Wh):
    zt = nn_utils.sigmoid(Wz * (ht_1, xt))
    rt = nn_utils.sigmoid(Wr * (ht_1, xt))
    ht_ = nn_utils.tanh(Wh * (rt * ht_1, xt))
    ht = (1 - zt) * ht_1 + zt * ht_
    return ht


# sru

# xt' = W * xt
# ft = σ(Wf * xt + bf)
# rt = σ(Wr * xt + br)
# ct = ft * ct-1 + (1 - ft) * xt'
# ht = rt * g(ct) + (1 - rt) * xt

#  xt_, ft, rt 可以并行，不依赖上一个状态

def sru(xt, ct_1, W, Wf, bf, Wr, br, g):
    xt_ = W * xt
    ft = nn_utils.sigmoid(Wf * xt + bf)
    rt = nn_utils.sigmoid(Wr * xt + br)
    ct = ft * ct_1 + (1 - ft) * xt_
    ht = rt * g(ct) + (1 - rt) * xt_
    return ct, ht
