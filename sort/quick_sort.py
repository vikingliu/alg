# coding=utf-8


def partition(data, start, end):
    index = data[start]
    while start < end:
        while start < end and data[end] >= index:
            end -= 1
        if start < end:
            data[start] = data[end]
            start += 1
        while start < end and data[start] < index:
            start += 1
        if start < end:
            data[end] = data[start]
            end -= 1
    data[start] = index
    return start


def partition_1(a, start, end):
    index = start
    start += 1
    while start < end:
        while start < end and a[end] > a[index]:
            end -= 1
        while start < end and a[start] < a[index]:
            start += 1
        a[start], a[end] = a[end], a[start]

    if a[start] > a[index]:
        start -= 1
    a[start], a[index] = a[index], a[start]
    return start


def partition_2(a, start, end):
    v = a[start]
    index = start - 1
    for i in range(start, end + 1):
        if a[i] < v:
            index += 1
            a[i], a[index] = a[index], a[i]
    return index + 1


def quick_sort(data, start, end, func=partition):
    if start >= end:
        return

    p = func(data, start, end)
    quick_sort(data, start, p - 1)
    quick_sort(data, p + 1, end)


num = [5, 1, 9, 2, 4]
quick_sort(num, 0, len(num) - 1, partition_2)
print(num)
