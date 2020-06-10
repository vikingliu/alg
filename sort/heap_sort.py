def heap_sort(data):
    if data is None or len(data) == 0:
        return
    n = len(data)
    for i in range(n / 2 - 1, -1, -1):
        build(data, i, n)
    for i in range(n):
        last = n - i - 1
        data[0], data[last] = data[last], data[0]
        build(data, 0, last)


def build(data, i, n):
    left = i * 2 + 1
    right = left + 1
    max_i = i
    if left < n and data[left] > data[max_i]:
        max_i = left
    if right < n and data[right] > data[max_i]:
        max_i = right

    if max_i != i:
        data[max_i], data[i] = data[i], data[max_i]
        build(data, max_i, n)

