class Node:
    def __init__(self, value, obj=None):
        self.value = value
        self.obj = obj

    def __str__(self):
        return '%s, %s' % (self.value, self.obj)

class Heap:
    def __init__(self, max_size, big=True, data=[]):
        self.max_size = max_size
        self.big = big
        if data is None:
            data = []
        self.data = data
        if data:
            self.adjust()

    def is_full(self):
        return self.max_size == len(self.data)

    def add(self, item):
        if self.is_full():
            self.replace_head(item)
        else:
            self.data.append(item)
        self.adjust()

    def replace_head(self, item):
        if self.data:
            self.data[0] = item
            self._heap(self.data, 0, len(self.data))
        else:
            self.add(item)

    def head(self):
        return self.data[0] if self.data else None

    def adjust(self):
        n = len(self.data)
        for i in range(n/2 - 1, -1, -1):
            self._heap(self.data, i, n)

    def _heap(self, data, i, n):
        left = i * 2 + 1
        right = left + 1
        target = i
        if self.big:
            if left < n and data[left].value > data[target].value:
                target = left
            if right < n and data[right].value > data[target].value:
                target = right
        else:
            if left < n and data[left].value < data[target].value:
                target = left
            if right < n and data[right].value < data[target].value:
                target = right
        if target <> i:
            data[i], data[target] = data[target], data[i]
            self._heap(data, target, n)

    def __str__(self):
        rst = []
        for item in self.data:
            rst.append('%s' % item)
        return str(rst)


