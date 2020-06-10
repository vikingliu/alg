cnt = 0
def permutation(data, start=0):
    """

    :param data: sorted list
    :param start:
    :return:
    """
    global cnt
    if start == len(data):
        print data
        return

    permutation(data, start + 1)
    for i in range(start + 1, len(data)):
        if i > start and data[i] == data[i - 1]:
            continue
        cnt += 1
        data[i], data[start] = data[start], data[i]
        permutation(data, start + 1)
        data[i], data[start] = data[start], data[i]

permutation([1,2,3])
print cnt
