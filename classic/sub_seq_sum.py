# encoding=utf-8


def get_sum(A):
    if len(A) == 1:
        return A[0]
    elif len(A) == 2:
        return max(A[0], A[1])

    path = [0] * len(A)
    path[0] = 0
    dp_2 = A[0]
    if A[0] > A[1]:
        path[1] = -1
        dp_1 = A[0]
    else:
        path[1] = 0
        dp_1 = A[1]
    for i in range(2, len(A)):
        if dp_2 + A[i] > A[i] and dp_2 + A[i] > dp_1:
            path[i] = -2
            dp_i = dp_2 + A[i]
        elif dp_1 > A[i] and dp_1 > dp_2 + A[i]:
            path[i] = -1
            dp_i = dp_1
        else:
            path[i] = 0
            dp_i = A[i]
        dp_2 = dp_1
        dp_1 = dp_i

    while True:
        if path[i] == 0:
            print(A[i])
            break
        elif path[i] == -1:
            i += -1
        elif path[i] == -2:
            print(A[i], end=' ')
            i += -2
    return dp_1


def get_sum_1(A):
    dp = [[0] * 2 for _ in range(len(A))]
    dp[0][0] = -sys.maxsize
    dp[0][1] = A[0]
    for i in range(1, len(A)):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1])
        dp[i][1] = max(dp[i - 1][0] + A[i], A[i])
    return max(dp[-1][0], dp[-1][1])


print(get_sum([-3, -2, 1, 3, 6, -2, -4]))
