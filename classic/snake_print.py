# coding=utf-8

def snake(data):
    m, n = len(data), len(data[0])
    total = m * n
    i, j = 0, 0
    cnt = 0
    direction = 'right'
    right, left, down, up = n - 1, 0, m - 1, 1
    while cnt < total:
        print(data[i][j], end=' ')
        if direction == 'right':
            if j == right:
                direction = 'down'
                i += 1
                right -= 1
            else:
                j += 1
        elif direction == 'down':
            if i == down:
                direction = 'left'
                j -= 1
                down -= 1
            else:
                i += 1
            pass
        elif direction == 'left':
            if j == left:
                direction = 'up'
                i -= 1
                left += 1
            else:
                j -= 1
        elif direction == 'up':
            if i == up:
                direction = 'right'
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
