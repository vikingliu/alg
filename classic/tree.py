# coding=utf-8

class Node:
    def __init__(self, val, left=None, right=None):
        self.left = left
        self.right = right
        self.val = val


def tree_sum(root, sum=0):
    if root is None:
        return sum
    sum = sum * 10 + root.val
    if root.left is None and root.right is None:
        return sum
    return tree_sum(root.left, sum) + tree_sum(root.right, sum)


def max_depth_path(root, height=0, path='#'):
    if root is None:
        return 0, path
    height += 1
    path = '%s->%s' % (path, root.val)
    if root.left is None and root.right is None:
        return height, path
    left_height, left_path = max_depth_path(root.left, height, path)
    right_height, right_path = max_depth_path(root.right, height, path)
    if left_height > right_height:
        return left_height, left_path
    else:
        return right_height, right_path


def is_same(root1, root2):
    if root1 is None and root2 is None:
        return True
    if root1 is not None and root2 is not None:
        return is_same(root1.left, root2.right) and is_same(root1.right, root2.left)
    return False


def cal_height(root):
    if root is None:
        return 0
    root.left_height = cal_height(root.left) + 1
    root.right_height = cal_height(root.right) + 1
    return max(root.left_height, root.right_height)


def is_in(rootA, rootB):
    cal_height(rootA)
    cal_height(rootB)

    def _is_in(_rootA, _rootB):
        if _rootA is None and _rootB is None:
            return True
        if _rootA is not None and _rootB is not None:
            if _rootA.left_height < _rootB.left_height or _rootA.right_height < _rootB.right_height:
                return False

        rst = __is_in(_rootA, _rootB)
        if rst:
            return rst
        return _is_in(_rootA.left, _rootB) or _is_in(_rootA.right, _rootB)

    return _is_in(rootA, rootB)


def __is_in(rootA, rootB):
    if rootA is None and rootB is None:
        return True
    if rootA is not None and rootB is not None:
        if rootA.left_height < rootB.left_height or rootA.right_height < rootB.right_height:
            return False
        return __is_in(rootA.left, rootB.left) and __is_in(rootA.right, rootB.right)
    if rootA is None:
        return False
    return True


root = Node(1, Node(3, Node(1)), Node(2, None, Node(2)))
# print(get_sum(root))
# print(max_depth_path(root))
print(is_same(root.left, root.right))
