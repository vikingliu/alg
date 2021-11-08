# coding=utf-8

def matrix_conv(matrix):
    matrix_rows = []
    matrix_cols = []
    for i in range(len(matrix)):
        row = {}
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                row[(i, j)] = matrix[i][j]
        matrix_rows.append(row)
    return matrix_rows


def matrix_multi(matrix1, matrix2):
    matrix_rows = []

    for row1 in matrix1:
        new_row = {}
        new_v = 0
        for i, val1 in row1.items():
            for col in range(len(matrix2)):
                for j, val2 in matrix2[col].items():
                    pass

            if (j, i) in matrix2[j]:
                new_v += matrix2[j][(j, i)] * val
                new_row[(i, j)] = new_v
        matrix_rows.append(new_row)
    return matrix_rows


matrix1 = [
    [1, 2, 0],
    [0, 0, 1],
    [2, 0, 0]
]
a = matrix_conv(matrix1)
print(a)
matrix2 = [
    [0, 2, 0],
    [0, 0, 1],
    [0, 0, 0]
]

b = matrix_conv(matrix2)
print(b)

print(matrix_multi(a, b))
