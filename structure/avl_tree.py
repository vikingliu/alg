# coding=utf-8
class TreeNode:
    def __init__(self, val, left=None, right=None, height=1):
        self.val = val
        self.left = left
        self.right = right
        self.height = height

    def __repr__(self, label='root', level=0):
        ret = "\t" * level + repr(label) + ':' + repr(self.val) + "," + repr(self.height) + "\n"
        if self.left:
            ret += self.left.__repr__('left', level + 1)
        if self.right:
            ret += self.right.__repr__('right', level + 1)
        return ret


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance_factor(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def is_bst(self):
        vals = []
        self.__in_order(self.root, vals)
        for i in range(1, len(vals)):
            if vals[i - 1] > vals[i]:
                return False
        return True

    def in_order(self, vals=[]):
        return self.__in_order(self.root, vals)

    def __in_order(self, node, vals):
        if node is not None:
            self.__in_order(node.left, vals)
            vals.append(node.val)
            self.__in_order(node.right, vals)

    def is_balanced(self):
        return self.__is_balanced(self.root)

    def __is_balanced(self, node):
        if node is None:
            return True
        balance = self.get_balance_factor(node)
        if abs(balance) > 1:
            return False
        return self.__is_balanced(node.left) and self.__is_balanced(node.right)

    def add(self, val):
        node = self.__add(self.root, val)
        if self.root is None:
            self.root = node

    def __add(self, node, val):
        if node is None:
            return TreeNode(val)

        if node.val > val:
            node.left = self.__add(node.left, val)
        elif node.val < val:
            node.right = self.__add(node.right, val)
        else:
            node.val = val
        return self.__rotate(node)

    def delete(self, val):
        return self.__delete(self.root, val)

    def __delete(self, node, val):
        if node is None:
            return None

        rest = node
        if node.val > val:
            node.left = self.__delete(node.left, val)
        elif node.val < val:
            node.right = self.__delete(node.right, val)
        else:
            # find val
            if node.left is None:
                rest = node.right
                node.right = None
            elif node.right is None:
                rest = node.left
                node.left = None
            else:
                min_node = self.__find_min_node(node.right)
                if node == self.root:
                    self.root = min_node

                min_node.right = self.__delete(node.right, min_node.val)
                min_node.left = node.left
                rest = min_node
                node.left = None
                node.right = None
        return self.__rotate(rest)

    def update(self, old_val, new_val):
        self.__delete(self.root, old_val)
        self.__add(self.root, new_val)

    def find(self, val):
        cur = self.root
        while cur:
            if cur.val > val:
                cur = cur.left
            elif cur.val < val:
                cur = cur.right
            else:
                break
        return cur

    def __find_min_node(self, node):
        if node is None or node.left is None:
            return node
        return self.find_next(node.left)

    # 对节点进行向右旋转操作，返回旋转后的根节点x
    #      y                   x
    #     / \                 /  \
    #    x  T4  向右旋转(y)   z     y
    #   / \    ---------->  / \   / \
    #  z  T3              T1  T2 T3 T4
    # / \
    # T1 T2
    def right_rotate(self, y):
        x = y.left
        T3 = x.right
        x.right = y
        y.left = T3
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        if y == self.root:
            self.root = x
        return x

    # 对节点进行向左旋转操作，返回旋转后的根节点x
    #   y                 x
    #  / \               /  \
    # T1  x  向左旋转(y) y    z
    #    / \ -------> / \   / \
    #   T2  z        T1 T2 T3 T4
    #      / \
    #     T3 T4
    def left_rotate(self, y):
        x = y.right
        T2 = x.left
        x.left = y
        y.right = T2
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        if y == self.root:
            self.root = x
        return x

    def __rotate(self, node):
        if node:
            node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
            balance = self.get_balance_factor(node)
            # LL
            if balance > 1 and self.get_balance_factor(node.left) >= 0:
                return self.right_rotate(node)
            # RR
            if balance < -1 and self.get_balance_factor(node.right) <= 0:
                return self.left_rotate(node)
            # LR
            if balance > 1 and self.get_balance_factor(node.left) < 0:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            # RL
            if balance < -1 and self.get_balance_factor(node.right) > 0:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
        return node


if __name__ == '__main__':
    tree = AVLTree()
    arr = [60, 50, 40, 30, 20, 10]
    # 依次添加进avl树
    for i in arr:
        tree.add(i)
    # 中序遍历
    tree.in_order()
    # 是否是BST
    print("is BST:", tree.is_bst())
    # 是否平衡
    print("is Balanced:", tree.is_balanced())
    # 添加节点45
    tree.add(45)
    # 是否还是BST
    print("is BST:", tree.is_bst())
    # 是否还是平衡的
    print("is Balanced:", tree.is_balanced())
    # 查找节点50
    print(tree.find(50))
    # 删除节点后
    tree.delete(40);
    # 是否还是BST
    print("is BST:", tree.is_bst())
    # 是否还是平衡的
    print("is Balanced:", tree.is_balanced())
    tree.update(45, 51)
    # 是否还是BST
    print("is BST:", tree.is_bst())
    # 是否还是平衡的
    print("is Balanced:", tree.is_balanced())

    print(tree.root)
