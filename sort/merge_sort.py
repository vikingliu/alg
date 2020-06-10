def merge_sort(data, start, end):
    if start >= end:
        return
    mid = start + (end - start) / 2
    merge_sort(data, start, mid)
    merge_sort(data, mid + 1, end)
    merge(data, start, mid, mid + 1, end)


def merge(data, start1, end1, start2, end2):
    data_tmp = []
    start = start1
    end = end2
    while start1 <= end1 and start2 <= end2:
        if data[start1] < data[start2]:
            data_tmp.append(data[start1])
            start1 += 1
        else:
            data_tmp.append(data[start2])
            start2 += 1
    while start1 <= end1:
        data_tmp.append(data[start1])
        start1 += 1
    while start2 <= end2:
        data_tmp.append(data[start2])
        start2 += 1
    n = start
    while start <= end:
        data[start] = data_tmp[start - n]
        start += 1

