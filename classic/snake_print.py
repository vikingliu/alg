# coding=utf-8

def snake(data):
    m, n = len(data), len(data[0])
    total = m * n
    i, j = 0, 0
    cnt = 0
    direction = 0  # 0=right, 1=down, 2=left, 3=up
    right, left, down, up = n - 1, 0, m - 1, 1
    while cnt < total:
        print(data[i][j], end=' ')
        if direction == 0:
            if j == right:
                direction = 1
                i += 1
                right -= 1
            else:
                j += 1
        elif direction == 1:
            if i == down:
                direction = 2
                j -= 1
                down -= 1
            else:
                i += 1
            pass
        elif direction == 2:
            if j == left:
                direction = 3
                i -= 1
                left += 1
            else:
                j -= 1
        elif direction == 3:
            if i == up:
                direction = 0
                j += 1
                up += 1
            else:
                i -= 1
        cnt += 1


data = [[1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
        [17, 18, 19, 20]]

snake(data)
