# coding=utf-8
from enum import Enum

# 红黑树(RBTree)的定义
# 1.任何一个节点都有颜色，黑色或者红色
# 2.根节点是黑色的
# 3.父子节点之间不能出现两个连续的红节点
# 4.任何一个节点向下遍历到其子孙的叶子节点，所经过的黑节点个数必须相等
# 5.空节点被认为是黑色的
# https://blog.csdn.net/tcorpion/article/details/54968644

COLOR = Enum('COLOR', ('red', 'black'))


class TreeNode:
    def __init__(self, val, left=None, right=None, parent=None, color=COLOR.black):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color

    def __repr__(self, label='root', level=0):
        ret = "\t" * level + repr(label) + ':' + repr(self.val) + "," + repr(self.color.name) + "\n"
        if self.left:
            ret += self.left.__repr__('left', level + 1)
        if self.right:
            ret += self.right.__repr__('right', level + 1)
        return ret


def parent_of(node):
    return node.parent if node else None


def left_of(node):
    return node.left if node else None


def right_of(node):
    return node.right if node else None


def color_of(node):
    return node.color if node else None


def set_color(node, color):
    if node:
        node.color = color


class RBTree:
    def __init__(self):
        self.root = None

    def find(self, key):
        return self._find(key, self.root)

    def _find(self, key, node):
        if node is None:
            return None
        if key == node.val:
            return node

        if key < node.val:
            return self._find(key, node.left)
        return self._find(key, node.right)

    def add(self, key):
        if self.root is None:
            self.root = TreeNode(key, color=COLOR.black)
            return
        is_left = False
        node = self.root
        while node:
            parent = node
            if key < node.val:
                node = node.left
                is_left = True
            elif key > node.val:
                node = node.right
                is_left = False
            else:
                return
        node = TreeNode(key)
        node.parent = parent
        if is_left:
            parent.left = node
        else:
            parent.right = node
        self.fix_after_add(node)

    # 新插入的节点是红色的，插入修复操作如果遇到父节点的颜色为黑则修复操作结束。也就是说，只有在父节点为红色节点的时候是需要插入修复操作的。
    #
    # 插入修复操作分为以下的三种情况，镜像对称后总共六种，而且新插入的节点的父节点都是红色的：
    # case 1.叔叔节点也为红色。
    # case 2.叔叔节点为黑色，且祖父节点、父节点和新节点不处于一条斜线上。
    # case 3.叔叔节点为黑色，且祖父节点、父节点和新节点处于一条斜线上。
    def fix_after_add(self, x):
        x.color = COLOR.red
        while x and x != self.root and x.parent.color == COLOR.red:
            if parent_of(x) == left_of(parent_of(parent_of(x))):
                y = right_of(parent_of(parent_of(x)))
                # case 1
                if color_of(y) == COLOR.red:
                    set_color(parent_of(x), COLOR.black)
                    set_color(y, COLOR.black)
                    set_color(parent_of(parent_of(x)), COLOR.red)
                    x = parent_of(parent_of(x))
                else:
                    # case 2 left rotate to case 3
                    if x == right_of(parent_of(x)):
                        x = parent_of(x)
                        self.left_rotate(x)
                    # case 3 right rotate
                    set_color(parent_of(x), COLOR.black)
                    set_color(parent_of(parent_of(x)), COLOR.red)
                    self.right_rotate(parent_of(parent_of(x)))
            else:
                y = left_of(parent_of(parent_of(x)))
                if color_of(y) == COLOR.red:
                    set_color(parent_of(x), COLOR.black)
                    set_color(y, COLOR.black)
                    set_color(parent_of(parent_of(x)), COLOR.red)
                    x = parent_of(parent_of(x))
                else:
                    if x == left_of(parent_of(x)):
                        x = parent_of(x)
                        self.right_rotate(x)
                    set_color(parent_of(x), COLOR.black)
                    set_color(parent_of(parent_of(x)), COLOR.red)
                    self.left_rotate(parent_of(parent_of(x)))
        self.root.color = COLOR.black

    # 删除修复操作分为四种情况：
    #
    # case1: 待删除的节点的兄弟节点是红色的节点；
    # case2: 待删除的节点的兄弟节点是黑色的节点，且兄弟节点的子节点都是黑色的;
    # case3: 待调整的节点的兄弟节点是黑色的节点，且兄弟节点的左子节点是红色的，右节点是黑色的(兄弟节点在右边)，如果兄弟节点在左边的话，就是兄弟节点的右子节点是红色的，左节点是黑色的;
    # case4: 待调整的节点的兄弟节点是黑色的节点，且右子节点是是红色的(兄弟节点在右边)，如果兄弟节点在左边，则就是对应的就是左节点是红色的。

    def remove(self, key):
        node = self.find(key)
        self._remove(node)
        return node

    def _remove(self, p):
        if p.left and p.right:
            s = self.successor(p)
            p.val = s.val
            p = s

        replacement = p.left if p.left else p.right

        if replacement:
            # Link replacement to parent
            replacement.parent = p.parent
            if p.parent is None:
                self.root = replacement
            elif p == p.parent.left:
                p.parent.left = replacement
            else:
                p.parent.right = replacement

            p.left = p.right = p.parent = None

            # Fix replacement
            if p.color == COLOR.black:
                self.fix_after_remove(replacement)
        elif p.parent is None:
            self.root = None
        else:
            if p.color == COLOR.black:
                self.fix_after_remove(p)

            if p.parent:
                if p == p.parent.left:
                    p.parent.left = None
                elif p == p.parent.right:
                    p.parent.right = None
                p.parent = None

    def successor(self, p):
        p = p.right
        while p.left:
            p = p.left
        return p

    # 删除修复操作分为四种情况：
    #
    # case1: 待删除的节点的兄弟节点是红色的节点；
    # case2: 待删除的节点的兄弟节点是黑色的节点，且兄弟节点的子节点都是黑色的;
    # case3: 待调整的节点的兄弟节点是黑色的节点，且兄弟节点的左子节点是红色的，右节点是黑色的(兄弟节点在右边)，如果兄弟节点在左边的话，就是兄弟节点的右子节点是红色的，左节点是黑色的;
    # case4: 待调整的节点的兄弟节点是黑色的节点，且右子节点是是红色的(兄弟节点在右边)，如果兄弟节点在左边，则就是对应的就是左节点是红色的。
    def fix_after_remove(self, x):
        while x != self.root and color_of(x) == COLOR.black:
            if x == left_of(parent_of(x)):
                brother = right_of(parent_of(x))
                # case 1: brother is red
                if color_of(brother) == COLOR.red:
                    # brother black
                    set_color(brother, COLOR.black)
                    # parent red
                    set_color(parent_of(x), COLOR.red)
                    # left rotate: brother -- parent, to case 2/3/4
                    self.left_rotate(parent_of(x))
                    # parent.right changed
                    brother = right_of(parent_of(x))

                # case 2: brother's are black
                if color_of(left_of(brother)) == COLOR.black and color_of(right_of(brother)) == COLOR.black:
                    # set brother to red
                    set_color(brother, COLOR.red)
                    # up
                    x = parent_of(x)
                else:
                    # case 3: brother's left is red, right is black
                    if color_of(right_of(brother)) == COLOR.black:
                        # set brother's left to black
                        set_color(left_of(brother), COLOR.black)
                        # set brother to red
                        set_color(brother, COLOR.red)
                        # right rotate to case 4
                        self.right_rotate(brother)
                        # parent.right changed
                        brother = right_of(parent_of(x))

                    # case 4:
                    set_color(brother, color_of(parent_of(x)))
                    set_color(parent_of(x), COLOR.black)
                    set_color(right_of(brother), COLOR.black)
                    self.left_rotate(parent_of(x))
                    x = self.root
            else:
                # symmetric
                brother = left_of(parent_of(x))
                if color_of(brother) == COLOR.red:
                    set_color(brother, COLOR.black)
                    set_color(parent_of(x), COLOR.red)
                    self.right_rotate(parent_of(x))
                    brother = left_of(parent_of(x))

                if color_of(right_of(brother)) == COLOR.black and color_of(left_of(brother)) == COLOR.black:
                    set_color(brother, COLOR.red)
                    x = parent_of(x)
                else:
                    if color_of(left_of(brother)) == COLOR.black:
                        set_color(right_of(brother), COLOR.black)
                        set_color(brother, COLOR.red)
                        self.left_rotate(brother)
                        brother = left_of(parent_of(x))
                    set_color(brother, color_of(parent_of(x)))
                    set_color(parent_of(x), COLOR.black)
                    set_color(left_of(brother), COLOR.black)
                    self.right_rotate(parent_of(x))
                    x = self.root
        set_color(x, COLOR.black)

    # 对节点进行向右旋转操作，返回旋转后的根节点l
    #      p                   l
    #     / \                 /  \
    #    l  T4  向右旋转(y)   z     p
    #   / \    ---------->  / \   / \
    #  z  T3              T1  T2 T3 T4
    # / \
    # T1 T2
    def right_rotate(self, p):
        if p:
            # 取出p的左儿子
            l = p.left
            # 然后将p的左儿子的右儿子，也就是p的右孙子变成p的左儿子
            p.left = l.right
            if l.right:
                # p的右孙子的父亲现在是p
                l.right.parent = p

            # 然后把p的父亲，设置为p左儿子的父亲
            l.parent = p.parent
            # 这说明p原来是root节点
            if p.parent is None:
                self.root = l
            elif p.parent.left == p:
                p.parent.left = l
            else:
                p.parent.right = l
            l.right = p
            p.parent = l

    # 对节点进行向左旋转操作，返回旋转后的根节点r
    #   p                 r
    #  / \               /  \
    # T1  r  向左旋转(p) p    z
    #    / \ -------> / \   / \
    #   T2  z        T1 T2 T3 T4
    #      / \
    #     T3 T4
    def left_rotate(self, p):
        if p:
            # 取出p的右儿子
            r = p.right
            # 然后将p的右儿子的左儿子，也就是p的左孙子变成p的右儿子
            p.right = r.left
            if r.left:
                # p的左孙子的父亲现在是p
                r.left.parent = p

            # 然后把p的父亲，设置为p右儿子的父亲
            r.parent = p.parent
            # 这说明p原来是root节点
            if p.parent is None:
                self.root = r
            elif p.parent.left == p:
                p.parent.left = r
            else:
                p.parent.right = r
            r.left = p
            p.parent = r


if __name__ == '__main__':
    tree = RBTree()
    tree.add(1)
    tree.add(10)
    tree.add(9)
    tree.add(2)
    tree.add(3)
    tree.add(8)
    tree.add(7)
    tree.add(4)
    tree.add(5)
    tree.add(6)
    tree.remove(1)
    tree.remove(7)
    print tree.root
