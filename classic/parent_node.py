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


def find_min_parent(root, p, q):
    if root is None:
        return 0, None
    val = 0
    if root.val == p:
        val = 1
    if root.val == q:
        val = 2
    left_v, left_node = find_min_parent(root.left, p, q)
    if left_v == 3 and left_node:
        return left_v, left_node
    right_v, right_node = find_min_parent(root.right, p, q)
    if right_v == 3 and right_node:
        return right_v, right_node

    if val + left_v == 3 or val + right_v == 3 or left_v + right_v == 3:
        return 3, root
    return max(val, left_v, right_v), None


class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        return 'node val:' + str(self.val)


#       1
#    2    3
#       5   8

root = Node(1, Node(2), Node(3, Node(5), Node(8)))
v, n = find_min_parent(root, 2, 9)
if n:
    print(n)
