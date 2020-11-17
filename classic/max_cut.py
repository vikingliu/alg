# coding=utf-8

# N = a1+a2+a3...+am
# max(a1*a2*a3...*am)
def max_cut_0(N, dp={}):
    if N <= 3:
        return N, [N]
    if N in dp:
        return dp[N]
    max_v = 0
    max_path = []
    for i in range(2, int(N / 2) + 1):
        v1, path1 = max_cut_0(i, dp)
        dp[i] = (v1, path1)
        v2, path2 = max_cut_0(N - i, dp)
        dp[N - i] = (v2, path2)
        if max_v < v1 * v2:
            max_v = v1 * v2
            max_path = path1 + path2
    return max_v, max_path


def max_cut(N):
    v = N % 3
    e = int(N / 3)
    if v == 2:
        return 2 * (3 ** e), [2] + ([3] * e)
    if v == 1:
        return 2 * 2 * (3 ** (e - 1)), [2, 2] + ([3] * (e - 1))
    if v == 0:
        return 3 ** e, [3] * e


def max_cut_no_dup(N):
    seq = set()
    res = 1
    cur_sum = 0
    n = 2
    while cur_sum < N:
        if cur_sum + n > N:
            n = N - cur_sum
            for m in seq:
                if n + m not in seq:
                    n += m
                    seq.remove(m)
                    cur_sum -= m
                    res //= m
                    break
        seq.add(n)
        cur_sum += n
        res *= n
        n += 1

    return res, list(seq)


n = 25
print(max_cut(n))
print(max_cut_0(n))
print(max_cut_no_dup(n))
