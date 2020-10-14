def get_sub(nums, s):
    res = []

    def dfs(nums, i, s, path, v):
        if v == s:
            res.append(path.copy())
            return
        if i == len(nums) or v > s:
            return

        path.append(nums[i])
        dfs(nums, i + 1, s, path, v + nums[i])
        path.pop()
        dfs(nums, i + 1, s, path, v)

    dfs(nums, 0, s, [], 0)
    return res


print(get_sub([1, 2, 3, 4, -1, 5], 10))
