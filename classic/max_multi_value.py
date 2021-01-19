max_v = 0
max_seq = []


def get_sub(nums, s):
    res = []

    def dfs(nums, i, s, path, v, rest):
        global max_v, max_seq
        if v == s:
            x = 1
            for j in path:
                x *= j
            if max_v < x:
                max_v = x
                max_seq = path.copy()
            res.append(path.copy())
            return
        if i == len(nums) or v > s or v + rest < s:
            return
        rest -= nums[i]
        path.append(nums[i])
        dfs(nums, i + 1, s, path, v + nums[i], rest)
        path.pop()
        dfs(nums, i + 1, s, path, v, rest)

    rest = sum(nums)
    dfs(nums, 0, s, [], 0, rest)
    print(max_v, max_seq)
    return res


N = 10
print(get_sub(range(1, N), N))
