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
        for i, item in enumerate(self.keys):
            if key < item:
                return i, self.children[i]
        return len(self.keys) - 1, self.children[-1]

    def add_key(self, key, child=None):
        index = 0
        for i, item in enumerate(self.keys):
            index = i
            if key < item:
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

    def merge(self, left, right):
        if left.is_leaf() and right.is_leaf():
            left.keys = left.keys + right.keys
            if right.next:
                right.next.pre = left
                left.next = right.next
            return left.split()

        p_key, p_ref = self.merge(left.children[-1], right.children[0])
        if p_key:
            left.keys += [p_key] + right.keys
            right.children[0] = p_ref
            left.children += right.children
        else:
            left.keys += right.keys
            right.children.remove(right.children[0])
            left.children = left.children + right.children

        return left.split()

    def split(self):
        # max keys = m - 1
        if len(self.keys) < self.m:
            return None, None
        mid = len(self.keys) / 2 - 1
        key = self.keys[mid]

        # keep the left child
        # new a right child
        right_child = Node(m=self.m)
        right_child.keys = self.keys[mid + 1:] if self.children else self.keys[mid:]
        self.keys = self.keys[0: mid]

        if self.children:
            right_child.children = self.children[mid + 1:]
            self.children = self.children[0:mid + 1]
        else:
            if self.next:
                self.next.pre = right_child
                right_child.next = self.next
            right_child.pre = self
            self.next = right_child

        return key, right_child

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
        self.tail = None

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
            self.tail = self.root
            self.tail.next = None
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
            if not node.is_leaf():
                # delete leaf key
                index = node.keys.index(key) + 1
                child = node.children[index]
                self._delete(child, key)
            node.remove(key)
        else:
            index, child = node.get_child(key)
            self._delete(child, key)
            left = node.children[index]
            right = node.children[index + 1]
            for child in [left, right]:
                # min keys = m/2 - 1
                if len(child.keys) < self.m / 2 - 1:
                    key = node.keys[index]
                    # add key to the child
                    if not child.is_leaf():
                        self._add(child, key)
                    # remove the key from node
                    node.remove(key, index=index)
                    break


if __name__ == '__main__':
    tree = BPlusTree(4)
    # s = '6 10 4 14 5 11 15 3 2 12 1 7 8 8 6 3 6 21 5 15 15 6 32 23 45 65 7 8 6 5 4'
    # for i in s.split(' '):
    #     tree.add(int(i))
    # print tree.root

    tree.add(1)
    tree.add(3)
    tree.add(10)
    tree.add(11)
    tree.add(9)
    tree.add(6)
    tree.add(4)
    tree.add(-1)
    tree.add(20)
    tree.add(61)
    tree.add(62)
    tree.add(22)
    tree.add(5)
    tree.add(30)
    tree.add(31)
    tree.add(7)
    tree.add(8)
    print tree.root
    tree.delete(10)
    print tree.root
    tree.delete(1)
    tree.delete(-1)
    print tree.root
    tree.delete(20)
    print tree.root
    head = tree.head
    while head:
        print head
        head = head.next
