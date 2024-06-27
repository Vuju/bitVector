# Class file implementing an advanced bit-vector as explained in the lecture

class myBitVector:
    def __init__(self, vectorAsString):
        self.len = len(vectorAsString)
        self.vector = int(vectorAsString, 2)

    def access(self, index):
        return (self.vector >> (self.len - 1 - index)) & 1

    def rank(self, index):
        return bin(self.vector & ((1 << (index + 1)) - 1)).count("1")

    def select(self, index):
        return bin(self.vector & (((1 << (index + 1)) - 1) << (self.len - index - 1))).count("1")

    def space(self):
        return self.len