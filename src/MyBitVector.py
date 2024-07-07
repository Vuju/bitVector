# Class file implementing an advanced bit-vector as explained in the lecture

class MyBitVector:
    """A bit vector which implements (somewhat) efficient rank and select operations.

        Attributes:
            vectorAsString: A string of 0 and 1 to read a text file.
        """
    def __init__(self, vectorAsString):
        self.len = len(vectorAsString)
        self.vector = [char for char in vectorAsString]

        log2 = (self.len.bit_length() - 1)
        self.log2sq = log2 ** 2
        self.log2hf = int(log2 / 2)
        self.rank = self._calculate_rank_super_block(self.vector, self.log2sq, self.log2hf)
        # todo: create select structure?

    def access(self, index):
        return self.vector[index]

    def rank(self, args):
        [b, index] = args
        rankOf1 = self.rank()[int(index / self.log2sq)].get_rank(index % self.log2sq)
        if b == 1:
            return rankOf1
        else:
            return index-rankOf1

    def select(self, args):
        [b, index] = args
        # todo: implement

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
        self.prevOffset = prevOffset
        self.blockLen = blockLen
        numBlocks = int(len(self.vector) / blockLen) + 1  # todo: check whether +1 is necessary, mby optimize
        self.blocks = [None] * numBlocks

        currentOffset = 0
        for i in range(numBlocks):
            self.blocks[i] = Block(vec[(i * blockLen): ((i + 1) * blockLen)], currentOffset)
            currentOffset = self.blocks[i].offset
        self.offset = prevOffset + currentOffset

    def get_rank(self, index):
        blockIndex = int(index / self.blockLen)
        mod = index % self.blockLen
        return self.prevOffset + self.blocks[blockIndex].get_rank(mod)


class Block:
    def __init__(self, vec, prevOffset):
        currentOffest = 0
        self.lookup = [None] * len(vec)
        for i in vec:
            if i == 1:
                currentOffest += 1
            self.lookup[i] = currentOffest
        self.prevOffset = prevOffset
        self.offset = prevOffset + currentOffest

    def get_rank(self, index):
        return self.prevOffset + self.lookup[index]

