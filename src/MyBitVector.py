# Class file implementing an advanced bit-vector as explained in the lecture

class MyBitVector:
    def __init__(self, vectorAsString):
        self.len = len(vectorAsString)
        self.vector = [char for char in vectorAsString]

        log2 = (self.len.bit_length() - 1)
        log2sq = log2 ** 2
        log2hf = int(log2 / 2)
        self.rank = self._calculate_rank_super_block(self.vector, log2sq, log2hf)

    def access(self, index):
        return self.vector[index]

    def rank(self):
        pass

    def select(self):
        pass

    def _calculate_rank_super_block(self, vec, log2sq, log2hf):
        numSuperBlocks = int(len(vec) / log2sq) + 1  # todo: optimize if no rounding happens
        superBlocks = [None] * numSuperBlocks

        currentOffset = 0
        for i in range(numSuperBlocks):
            superBlocks[i] = SuperBlock(vec[(i * log2sq): ((i + 1) * log2sq)], currentOffset, log2hf)
            currentOffset = superBlocks[i].offset

        return superBlocks


class SuperBlock:
    def __init__(self, vec, prevOffset, blockLen):
        self.vector = vec
        numBlocks = int(len(self.vector) / blockLen) + 1  # todo: check whether +1 is necessary, mby optimize
        blocks = [None] * numBlocks

        currentOffset = 0
        for i in range(numBlocks):
            blocks[i] = Block(vec[(i * blockLen): ((i + 1) * blockLen)], currentOffset)
            currentOffset = blocks[i].offset

        self.offset = prevOffset + currentOffset


class Block:
    def __init__(self, vec, prevOffset):
        currentOffest = 0
        # todo create lookup table
        for i in vec:
            if i == 1:
                currentOffest += 1
            # todo: update lookup table
        self.offset = prevOffset + currentOffest
