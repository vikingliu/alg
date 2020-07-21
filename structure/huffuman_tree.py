# coding=utf-8

class Node(object):
    def __init__(self, name, weight, left=None, right=None):
        self.name = name
        self.weight = weight
        self.left = left
        self.right = right

    def __str__(self):
        return 'name: %s, weight:%s' % (self.name, self.weight)


class Huffman(object):
    def __init__(self, data):
        """
        :param
        data: {name: {weight: xx}, name:{weight: xx} ... }
        data: [(name, weight), (name, weight), ....]
        data: {name: weight, name:weight, ....}

        """

        self.root = None
        if data:
            nodes = []
            if type(data) is list:
                self.codes = {}
                for name, weight in data:
                    nodes.append(Node(name, weight))
                    self.codes[name] = {'weight': weight}
            else:
                self.codes = data
                for name, value in data.items():
                    weight = value
                    if type(value) is dict:
                        weight = value['weight']
                    else:
                        self.codes[name] = {'weight': weight}
                    nodes.append(Node(name, weight))
            self.__huffman_tree(nodes)

    def __huffman_tree(self, data):
        self.__sort(data)
        n = len(data)
        for i in xrange(n - 1, 0, -1):
            item1 = data[0]
            data[0] = data[i]
            self.__build(data, 0, i)
            item2 = data[0]
            data[0] = Node('node', item1.weight + item2.weight, item1, item2)
            self.__build(data, 0, i)
        self.__to_code(data[0], '')
        self.root = data[0]

    def __to_code(self, node, code):
        if node is None:
            return
        if node.left is None and node.right is None:
            self.codes[node.name]['code'] = code
        self.__to_code(node.left, code + '0')
        self.__to_code(node.right, code + '1')

    def __sort(self, data):
        n = len(data)
        for i in xrange(n / 2, -1, -1):
            self.__build(data, i, n)

    def __build(self, data, i, n):
        left = 2 * i + 1
        right = 2 * i + 2
        min_i = i
        if left < n and data[left].weight < data[min_i].weight:
            min_i = left
        if right < n and data[right].weight < data[min_i].weight:
            min_i = right
        if min_i != i:
            data[i], data[min_i] = data[min_i], data[i]
            self.__build(data, min_i, n)


if __name__ == '__main__':
    char_weights = [('a', 5), ('b', 4), ('c', 10), ('d', 8), ('f', 15), ('g', 2)]
    word_dict = {}
    for name, weight in char_weights:
        word_dict[name] = {'weight': weight}
    print word_dict
    huffman = Huffman(char_weights)
    print huffman.codes
    print huffman.root
