# coding=utf-8

# B+树
# 
class Node(object):
    def __init__(self, key=None, m=2):
        self.keys = []
        if key:
            self.keys.append(key)
        self.children = []
        self.m = m
        self.next = None
        self.pre = None

    def is_leaf(self):
        return len(self.children) == 0

    def has_key(self, key):
        return key in self.keys

    def get_child(self, key):
        # return key index, child
        # 二分查找
        index = 0
        for i, item in enumerate(self.keys):
            if key <= item:
                index = i - 1 if i > 0 else i
                break
            index = i
        child = self.children[index] if self.children else None
        return index, child

    def add_key(self, key, child=None, index=-1):
        if index == -1:
            index = 0
            for i, item in enumerate(self.keys):
                index = i
                if key <= item:
                    break
                index = i + 1

        self.keys.insert(index, key)
        if child:
            self.children.insert(index, child)

        return self.split()

    def remove(self, key, index=-1):
        if self.is_leaf():
            self.keys.remove(key)
        else:
            index = self.keys.index(key) if index < 0 else index
            child = self.children[index]
            new_key = child.remove(key)
            if new_key:
                self.keys[index] = new_key
                if child and len(child.keys) < self.m / 2:
                    self.balance(index, child)
            else:
                self.keys.remove(key)
                self.children.remove(child)

        return self.keys[0] if self.keys else None

    def balance(self, index, child):
        if 0 <= index < len(self.keys):
            if len(child.keys) < self.m / 2:
                if index + 1 < len(self.keys):
                    left = child
                    right = self.children[index + 1]
                    index = index + 1
                elif index > 0:
                    left = self.children[index - 1]
                    right = child

                left_key, right_key, right_child = self.merge(left, right)

                if right_key:
                    self.children[index] = right_child
                    self.keys[index] = right_key
                else:
                    self.children.remove(right)
                    self.keys.remove(self.keys[index])

    def merge(self, left, right):
        if left.is_leaf() and right.is_leaf():
            left.keys = left.keys + right.keys
            if right.next:
                right.next.pre = left
            left.next = right.next
            return left.split()

        left_key, right_key, right_child = self.merge(left.children[-1], right.children[0])
        if left_key:
            left.keys[-1] = left_key
        if right_key:
            right.keys[0] = right_key
            right.children[0] = right_child
        left.keys += right.keys
        left.children += right.children

        return left.split()

    def split(self):
        # max keys = m - 1
        left_key = self.keys[0] if self.keys else None
        if len(self.keys) <= self.m:
            return left_key, None, None
        mid = len(self.keys) / 2

        # keep the left child
        # new a right child
        right_child = Node(m=self.m)
        right_child.keys = self.keys[mid:]
        self.keys = self.keys[0: mid]

        if self.children:
            right_child.children = self.children[mid:]
            self.children = self.children[0:mid]
        else:
            if self.next:
                self.next.pre = right_child
                right_child.next = self.next
            right_child.pre = self
            self.next = right_child

        right_key = right_child.keys[0]
        return left_key, right_key, right_child

    def __repr__(self, label='root', level=0):
        ret = "\t" * level + repr(label) + ':' + repr(self.keys) + "\n"
        for i, child in enumerate(self.children):
            ret += child.__repr__('child', level + 1)
        return ret


class BPlusTree(object):
    def __init__(self, m, unique=False):
        self.root = None
        self.m = m
        self.unique = unique
        self.head = None

    def get(self, key):
        if self.root is None:
            return None
        else:
            return self._get(self.root, key)

    def _get(self, node, key):
        if node is None:
            return None
        elif node.is_leaf() and node.has_key(key):
            return node
        else:
            i, child = node.get_child(key)
            return self._get(child, key)

    def add(self, key):
        if self.root is None:
            self.root = Node(key=key, m=self.m)
            self.head = self.root
            self.head.pre = None
        else:
            left_key, right_key, right_child = self._add(self.root, key)
            if right_key:
                new_node = Node(key=left_key, m=self.m)
                new_node.keys.append(right_key)
                new_node.children.append(self.root)
                new_node.children.append(right_child)
                self.root = new_node

    def _add(self, node, key):
        if self.unique and node.has_key(key):
            return None, None, None
        elif node.is_leaf():
            return node.add_key(key, None)
        else:
            i, child = node.get_child(key)
            left_key, right_key, right_child = self._add(child, key)
            node.keys[i] = left_key
            if right_key is None:
                return node.keys[0], None, None
            else:
                return node.add_key(right_key, right_child, index=i + 1)

    def delete(self, key):
        self._delete(self.root, key)
        if len(self.root.keys) == 1:
            tmp = self.root
            self.root = self.root.children[0]
            del tmp
        if not self.head.keys:
            self.head = self.head.next
            self.head.pre = None

    def _delete(self, node, key):
        if node is None:
            return
        if node.has_key(key):
            return node.remove(key)
        else:
            index, child = node.get_child(key)
            self._delete(child, key)
            # min keys = m/2 - 1
            if child and len(child.keys) < self.m / 2:
                node.balance(index, child)


if __name__ == '__main__':
    tree = BPlusTree(3)

    s = '6 10 4 14 5 11 15 3 2 12 1 7 8 8 6 3 6 21 5 15 15 6 32 23 45 65 7 8 6 5 4 6 6 6 6 6 6 6 6 6 6'
    for i in s.split(' '):
        tree.add(int(i))
    print tree.root
    arr = [int(i) for i in s.split(' ')]
    # tree.add(10)
    # tree.add(11)
    # tree.add(9)
    # tree.add(-1)
    # tree.add(6)
    # tree.add(4)
    # tree.add(20)
    # tree.add(61)
    # tree.add(62)
    # tree.add(22)
    # tree.add(5)
    # tree.add(30)
    # tree.add(31)
    # tree.add(7)
    # tree.add(8)
    tree.delete(6)
    arr.remove(6)
    tree.delete(4)
    arr.remove(4)
    tree.delete(5)
    arr.remove(5)
    tree.delete(1)
    arr.remove(1)
    tree.delete(2)
    arr.remove(2)
    tree.delete(3)
    arr.remove(3)
    tree.delete(3)
    arr.remove(3)
    tree.delete(4)
    arr.remove(4)
    tree.delete(10)
    arr.remove(10)
    tree.delete(11)
    arr.remove(11)
    tree.delete(12)
    arr.remove(12)
    tree.delete(5)
    arr.remove(5)
    tree.delete(5)
    arr.remove(5)
    tree.delete(6)
    arr.remove(6)
    tree.delete(6)
    arr.remove(6)
    tree.delete(6)
    arr.remove(6)

    tree.delete(6)
    arr.remove(6)
    tree.delete(6)
    arr.remove(6)
    tree.delete(7)
    arr.remove(7)
    tree.delete(7)
    arr.remove(7)
    tree.delete(8)
    arr.remove(8)
    tree.delete(8)
    arr.remove(8)
    tree.delete(8)
    arr.remove(8)
    tree.delete(8)
    # arr.remove(8)
    tree.delete(14)
    arr.remove(14)
    tree.delete(15)
    arr.remove(15)
    tree.delete(15)
    arr.remove(15)
    print tree.root
    head = tree.head
    while head:
        s1 = [str(key) for key in head.keys]
        print ' '.join(s1),
        head = head.next
    print ''

    arr = [str(i) for i in sorted(arr)]
    print ' '.join(arr)
