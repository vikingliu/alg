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


def is_in(rootA, rootB):
    pass


root = Node(1, Node(3, Node(1)), Node(2, None, Node(2)))
# print(get_sum(root))
# print(max_depth_path(root))
print(is_same(root.left, root.right))
