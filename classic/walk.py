# coding=utf-8


def walk(N, m, p, k, path=[]):
    """
    多少种走法
    :param N:
    :param m: start
    :param p: end position
    :param k: k-step
    :param path: from m to p steps
    :return:    
    """

    step = len(path)
    if step > k or m > N or m < 1:
        return 0
    if m == p and k == step:
        print(path)
        return 1
    return walk(N, m + 1, p, k, path + [1]) + walk(N, m - 1, p, k, path + [-1])


if __name__ == '__main__':
    print(walk(5, 2, 4, 4))
