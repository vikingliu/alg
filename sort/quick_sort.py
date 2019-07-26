def quick_sort(data, start, end):
    if start >= end:
        return

    p = partition(data, start, end)
    quick_sort(data, start, p - 1)
    quick_sort(data, p + 1, end)


def partition(data, start, end):
    tmp = data[start]

    while start < end:
        while start < end and data[end] > tmp:
            end -= 1
        if data[end] < tmp:
            data[start] = data[end]
            start += 1
        while start < end and data[start] < tmp:
            start += 1
        if data[start] > tmp:
            data[end] = data[start]
            end -= 1
    data[start] = tmp
    return start


d = [3, 4, 1, -2, 7, 9]
quick_sort(d, 0, len(d) - 1)
print d
