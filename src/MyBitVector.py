# Class file implementing an advanced bit-vector as explained in the lecture

class myBitVector:
    def __init__(self, vectorAsString):
        self.len = len(vectorAsString)
        self.vector = [char for char in vectorAsString]

    def access(self, index):
        return self.vector[index]

    def rank(self):
        pass

    def select(self):
        pass