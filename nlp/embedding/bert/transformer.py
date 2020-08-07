# coding=utf-8

import attention
from utils import nn_utils


# transform: multi-encoders and multi-decoder

# encoder: self-attention -> feed forward
# decoder: self-attention -> encoder-decoder attention -> feed forward


def feed_forward(z, W1, W2):
    h = z.dot(W1)
    u = h.dot(W2)
    z = nn_utils.softmax(u)
    return z


def encoder(x, position, Ws, W_O, W1, W2):
    """

    :param x: input embedding
    :param position: input position embedding
    :param Ws: list of [W_Q, W_K, W_V]
    :param W_O: for multi-headed attention
    :param W1: for feed_forward
    :param W2: for feed_forward
    :return:
    """
    x += position
    z = attention.multi_headed_attenton(x, Ws, W_O)
    z = x + z
    z = nn_utils.normalize_l2(z)
    z_f = feed_forward(z, W1, W2)
    z = z + z_f
    z = nn_utils.normalize_l2(z)
    return z


def decoder(x, memery, position, Ws, W_O, W1, W2):
    # masked multi-headed attention
    x += position
    z = attention.multi_headed_attenton(x, x, x, Ws, W_O)

    # add & norm
    z = x + z
    z = nn_utils.normalize_l2(z)

    # multi-headed attention
    # encode_ws = [W_Q, W_K_enc, W_V_enc]
    z_m = attention.multi_headed_attenton(z, memery, memery, W_O)

    # add & norm
    z = z_m + z
    z = nn_utils.normalize_l2(z)

    # ffnn
    z_f = feed_forward(z, W1, W2)

    # add & norm
    z = z + z_f
    z = nn_utils.normalize_l2(z)

    return z


def linear(x, w, b):
    y = w.dot(x) + b
    return y


def transformer(src, target, n):
    z = src
    for i in range(n):
        z = encoder(z)
    z_enc = z
    z = target
    for i in range(n):
        z = decoder(z)
    z = linear(z)
    z = nn_utils.softmax(z)
    return z
