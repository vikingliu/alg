# coding=utf-8


# B-Tree，或者B减树
# 一个 m 阶的B树是(m >= 3)
# 1.每一个节点最多有 m 个子节点
# 2.每一个非叶子节点（除根节点）最少有 ⌈m/2⌉ 个子节点， 孩子节点>=2
# 3.如果根节点不是叶子节点，那么它至少有两个子节点
# 4.有 k 个子节点的非叶子节点拥有 k − 1 个键
# 5.所有的叶子节点都在同一层
class Node(object):
    def __init__(self, key=None, m=2):
        self.keys = []
        if key:
            self.keys.append(key)
        self.children = []
        self.m = m

    def is_leaf(self):
        return len(self.children) == 0

    def has_key(self, key):
        return key in self.keys

    def get_child(self, key):
        # 二分查找
        for i, item in enumerate(self.keys):
            if key <= item:
                child = self.children[i] if self.children else None
                return i, child
        child = self.children[-1] if self.children else None
        return len(self.keys) - 1, child

    def add_key(self, key, child=None):
        index = 0
        for i, item in enumerate(self.keys):
            index = i
            if key <= item:
                break
            index = i + 1
        self.keys.insert(index, key)
        if child:
            self.children.insert(index + 1, child)

        return self.split()

    def remove(self, key, index=-1):
        if self.is_leaf():
            self.keys.remove(key)
        else:
            index = self.keys.index(key) if index < 0 else index
            left = self.children[index]
            right = self.children[index + 1]
            p_key, p_ref = self.merge(left, right)
            if p_key:
                self.keys[index] = p_key
                self.children[index + 1] = p_ref
            else:
                # merge to left = left + right
                self.keys.remove(key)
                self.children.remove(right)
        return index

    def merge(self, left, right):
        if left.is_leaf() and right.is_leaf():
            left.keys = left.keys + right.keys
            return left.split()

        p_key, p_ref = self.merge(left.children[-1], right.children[0])
        if p_key:
            left.keys.append(p_key)
            right.children[0] = p_ref
        else:
            right.children.remove(right.children[0])
        left.keys += right.keys
        left.children += right.children

        return left.split()

    def split(self):
        # max keys = m - 1
        if len(self.keys) < self.m:
            return None, None
        mid = len(self.keys) / 2
        key = self.keys[mid]

        # keep the left child
        # new a right child
        right_child = Node(m=self.m)
        right_child.keys = self.keys[mid + 1:]
        self.keys = self.keys[0: mid]

        if self.children:
            right_child.children = self.children[mid + 1:]
            self.children = self.children[0:mid + 1]

        return key, right_child

    def __repr__(self, label='root', level=0):
        ret = "\t" * level + repr(label) + ':' + repr(self.keys) + "\n"
        for i, child in enumerate(self.children):
            ret += child.__repr__('child', level + 1)
        return ret


class BTree(object):
    def __init__(self, m, unique=False):
        self.root = None
        self.m = m
        self.unique = unique

    def get(self, key):
        if self.root is None:
            return None
        else:
            return self._get(self.root, key)

    def _get(self, node, key):
        if node is None:
            return None
        elif node.has_key(key):
            return node
        else:
            i, child = node.get_child(key)
            return self._get(child, key)

    def add(self, key):
        if self.root is None:
            self.root = Node(key=key, m=self.m)
        else:
            p_key, p_ref = self._add(self.root, key)
            if p_key:
                new_node = Node(key=p_key, m=self.m)
                new_node.children.append(self.root)
                new_node.children.append(p_ref)
                self.root = new_node

    def _add(self, node, key):
        if self.unique and node.has_key(key):
            return None, None
        elif node.is_leaf():
            return node.add_key(key, None)
        else:
            i, child = node.get_child(key)
            p_key, p_ref = self._add(child, key)
            if p_key is None:
                return None, None
            else:
                return node.add_key(p_key, p_ref)

    def delete(self, key):
        self._delete(self.root, key)
        if not self.root.keys:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        if node is None:
            return
        if node.has_key(key):
            node.remove(key)
        else:
            index, child = node.get_child(key)
            self._delete(child, key)
            if node.children:
                for child in [node.children[index], node.children[index + 1]]:
                    # min keys = m/2 - 1
                    if (child.children and len(child.keys) < self.m / 2 - 1) or len(child.keys) == 0:
                        key = node.keys[index]
                        # add key to the child
                        self._add(child, key)
                        # remove the key from node
                        node.remove(key, index=index)
                        break


if __name__ == '__main__':
    tree = BTree(6)
    s = '6 6 6 6 6 10 4 14 5 11 15 3 2 12 1 7 8 8 6 3 6 21 5 15 15 6 32 23 45 65 7 8 6 5 4'
    for i in s.split(' '):
        tree.add(int(i))
    # tree.add(3)
    print tree.root
    tree.delete(11)
    tree.delete(10)
    print tree.root
    # tree.add(1)
    # tree.add(3)
    # tree.add(10)
    # tree.add(11)
    # tree.add(9)
    # tree.add(6)
    # tree.add(4)
    # tree.add(-1)
    # tree.add(20)
    # tree.add(61)
    # tree.add(62)
    # tree.add(22)
    # tree.add(5)
    # tree.add(30)
    # tree.add(31)
    # tree.add(7)
    # tree.add(8)
    # print tree.root
    #
    # tree.delete(6)
    # print tree.root
    # tree.delete(5)
    # print tree.root
    # tree.delete(31)
    # print tree.root
    # tree.delete(20)
    # print tree.root
    # tree.delete(-1)
    # print tree.root
    # tree.delete(1)
    # print tree.root
