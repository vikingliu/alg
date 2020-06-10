def min_parent(root, p0, p1):
    res = None
    def get_min_parent(root, p0, p1):
        global res
        if root is None:
            return False

        f_v = True if p0 == root or p1 == root else False

        f_l_v = get_min_parent(root.left, p0, p1)
        if f_v and f_l_v:
            res = root
            return True

        if res is not None:
            return True

        f_r_v = get_min_parent(root.right, p0, p1)
        if f_v and f_r_v:
            res = root
            return True

        if f_l_v and f_r_v:
            # find min root
            res = root

        return f_v or f_l_v or f_r_v
    get_min_parent(root, p0, p1)
    return res

