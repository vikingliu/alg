#coding=utf8
class Bitmap(object):
    def __init__(self, num):
        self.size  = self.calc_elem_index(num, True)
        self.array = [0 for i in range(self.size)]

    def calc_elem_index(self, num, up=False):
        #up为True则为向上取整, 否则为向下取整
        if up:
            return int((num + 31 - 1) / 31) #向上取整
        return num / 31

    def calc_bit_index(self, num):
        return num % 31

    def set(self, num):
        elemIndex = self.calc_elem_index(num)
        byteIndex = self.calc_bit_index(num)
        elem      = self.array[elemIndex]
        self.array[elemIndex] = elem | (1 << byteIndex)

    def get(self, num):
        elemIndex = self.calc_elem_index(num)
        byteIndex = self.calc_bit_index(num)
        elem      = self.array[elemIndex]
        return elem & (1 << byteIndex) > 0

    def clean(self, i):
        elemIndex = self.calc_elem_index(i)
        byteIndex = self.calc_bit_index(i)
        elem      = self.array[elemIndex]
        self.array[elemIndex] = elem & (~(1 << byteIndex))
