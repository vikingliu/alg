# coding=utf-8
import bitmap


class BloomFilter(object):
    def __init__(self, size, functions):
        self.functions = functions
        self.bitset = bitmap.Bitmap(size)

    def add(self, value):
        if not value:
            return False

        for f in self.functions:
            self.bitset.set(f.hash(value))
        return True

    def contains(self, value):
        if not value:
            return False

        ret = True
        for f in functions:
            ret = self.bitset.get(f.hash(value))
            if not ret:
                break
        return ret


class HashFunction(object):
    def __init__(self, size, seed):
        self.size = size
        self.seed = seed

    def hash(self, value):
        result = 0
        for c in value:
            result = seed * result + ord(c)

        return (size - 1) & result


if __name__ == '__main__':
    size = 100000
    seeds = [3, 5, 7, 11, 13, 31, 37, 61]
    functions = [HashFunction(size, seed) for seed in seeds]
    bloomfilter = BloomFilter(size, functions)

    values = ['when', 'how', 'where', 'too', 'there', 'to', 'when']
    for value in values:
        if not bloomfilter.contains(value):
            bloomfilter.add(value)
        else:
            print 'find:%s' % value
