def permutation(data, start=0):
    """

    :param data: sorted list
    :param start:
    :return:
    """
    if start == len(data):
        print data

    for i in range(start, len(data)):
        if i > start and data[i] == data[i - 1]:
            continue
        data[i], data[start] = data[start], data[i]
        permutation(data, start + 1)
        data[i], data[start] = data[start], data[i]

