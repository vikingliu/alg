import heapq


def tow_d(arr):
    if not arr:
        return 0
    n = len(arr)
    if n < 3:
        return 0
    left = 0
    right = n - 1
    area = 0
    while left <= right:
        left_max = arr[left]
        right_max = arr[right]
        if left_max < right_max:
            left += 1
            while left <= right and left_max > arr[left]:
                area += left_max - arr[left]
                left += 1
        else:
            right -= 1
            while left <= right and right_max > arr[right]:
                area += right_max - arr[right]
                right -= 1
    return area


def three_d(heightMap):
    if not heightMap:
        return 0
    m = len(heightMap)
    n = len(heightMap[0])

    if m < 3 or n < 3:
        return 0
    edges = []
    # visit = [[0]*n for i in xrange(m)]
    for i in xrange(m):
        heapq.heappush(edges, (heightMap[i][0], i, 0))
        heapq.heappush(edges, (heightMap[i][n - 1], i, n - 1))
        heightMap[i][0] = -1
        heightMap[i][n - 1] = -1
    for j in xrange(1, n - 1):
        heapq.heappush(edges, (heightMap[0][j], 0, j))
        heapq.heappush(edges, (heightMap[m - 1][j], m - 1, j))
        heightMap[0][j] = -1
        heightMap[m - 1][j] = -1

    visit_num = len(edges)
    if visit_num == n * m:
        return 0
    v = 0
    while edges:
        min_edge = heapq.heappop(edges)
        wall_min_v, i, j = min_edge
        start_point = [(i, j)]
        while start_point:
            i, j = start_point.pop()
            index = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
            for i, j in index:
                if 0 <= i < m and 0 <= j < n and heightMap[i][j] != -1:
                    if heightMap[i][j] <= wall_min_v:
                        v += wall_min_v - heightMap[i][j]
                        start_point.append((i, j))
                    else:
                        heapq.heappush(edges, (heightMap[i][j], i, j))
                    heightMap[i][j] = -1
                    visit_num += 1
        if visit_num == n * m:
            break
    return v


print(tow_d([4, 2, 1, 2, 3]))
