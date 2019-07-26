# coding=utf-8


class Node(object):
    def __init__(self, name, value, left=None, right=None):
        self.name = name
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return 'name: %s, value:%s' % (self.name, self.value)


class Huffman(object):
    def __init__(self, data):
        """
        :param data: [(val1, count), (val2, count), .....]
        """

        self.codes = {}
        if data:
            self.data = []
            for item in data:
                self.data.append(Node(item[0], item[1]))
            self.__huffman_tree(self.data)

    def __huffman_tree(self, data):
        self.__sort(data)
        n = len(data)
        for i in xrange(n - 1, 0, -1):
            item1 = data[0]
            data[0] = data[i]
            self.__build(data, 0, i)
            item2 = data[0]
            data[0] = Node(item1.name + ',' + item2.name, item1.value + item2.value, item1, item2)
            self.__build(data, 0, i)
        self.__to_code(data[0], '')

    def __to_code(self, root, path):
        if root is None:
            return
        if root.left is None and root.right is None:
            self.codes[root.name] = path
        self.__to_code(root.left, path + '0')
        self.__to_code(root.right, path + '1')

    def __sort(self, data):
        n = len(data)
        for i in xrange(n / 2, -1, -1):
            self.__build(data, i, n)

    def __build(self, data, i, n):
        left = 2 * i + 1
        right = left + 1
        min_i = i
        if left < n and data[left].value < data[min_i].value:
            min_i = left
        if right < n and data[right].value < data[min_i].value:
            min_i = right
        if min_i != i:
            data[i], data[min_i] = data[min_i], data[i]
            self.__build(data, min_i, n)


if __name__ == '__main__':
    char_weights = [('a', 5), ('b', 4), ('c', 10), ('d', 8), ('f', 15), ('g', 2)]
    huffman = Huffman(char_weights)
    print huffman.codes
