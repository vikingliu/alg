def quick_sort(data, start, end):
    if start >= end:
        return

    p = partition(data, start, end)
    quick_sort(data, start, p - 1)
    quick_sort(data, p + 1, end)

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


d = [3, 4, 1, -2, 7, 9]
quick_sort(d, 0, len(d) - 1)
print d
