# Class file implementing an advanced bit-vector as explained in the lecture


class MyBitVector:
    """A bit vector which implements (somewhat) efficient rank and select operations.

        Attributes:
            vectorAsString: A string of 0 and 1 to read a text file.
        """

    def __init__(self, vectorAsString):
        self.len = len(vectorAsString)
        self.vector = vectorAsString

        self.log2 = (self.len.bit_length() - 1)
        self.log2sq = self.log2 ** 2
        self.log2hf = int(self.log2 / 2)
        self.rankVector = _calculate_rank_super_block(self.vector, self.log2sq, self.log2hf)
        
        self.chunkOffsets = [None, None]
        self.sparseLookup = [None, None]
        self.subChunkOffsets = [None, None]
        self.denseSparseLookup = [None, None]
        self.denseDenseLookup = [None, None]
        
        self.chunkOffsets[0], self.sparseLookup[0], self.subChunkOffsets[0], self.denseSparseLookup[0], self.denseDenseLookup[0] = _calculate_select_structure(self.vector, self.log2, '0')
        self.chunkOffsets[1], self.sparseLookup[1], self.subChunkOffsets[1], self.denseSparseLookup[1], self.denseDenseLookup[1] = _calculate_select_structure(self.vector, self.log2, '1')


    def access(self, index):
        return self.vector[int(index)]

    def rank(self, args):
        [b, index] = [int(n) for n in args.split(" ")]
        rankOf1 = self.rankVector[int(index / self.log2sq)].get_rank(index % self.log2sq)
        if b == 1:
            return rankOf1
        else:
            return index - rankOf1

    def select(self, args):
        [bitChar, elementString] = args.split(" ")
        
        #print("lets go:")
        b = int(bitChar)
        element = int(elementString)        
        #print(self.chunkOffsets[b])
        
        chunkId = int(element / self.log2sq)
        #print(chunkId)
        
        if (self.chunkOffsets[b][chunkId + 1] - self.chunkOffsets[b][chunkId]) > (self.log2 ** 4):
            #print("Sparse!")
            return self.sparseLookup[b][element]
        else: 
            #print("Dense")
            offset = self.chunkOffsets[b][chunkId]
            subChunks = self.subChunkOffsets[b][offset]
            #print(self.subChunkOffsets[b])
            remainder = (element - 1) % self.log2sq            
            subChunkId = int(remainder / int(self.log2 ** (1/2)))
            #print(str(subChunkId) + " = " + str(remainder) + " / " + str(self.log2 ** (1/2)))
            relativeOffset = subChunks[subChunkId]
            if (subChunks[subChunkId + 1] - relativeOffset) > self.log2hf:
                #print("-> Sparse!")
                #print(self.denseSparseLookup[b])
                return self.denseSparseLookup[b][element]
            else:
                #print("-> Dense!")
                #print(self.denseDenseLookup[b])
                #print("Offset: " + str(offset) + ", relOff: " + str(relativeOffset))
                key = self.vector[offset + relativeOffset : offset + subChunks[subChunkId + 1]]
                subSubIndex = (remainder % int(self.log2 ** (1/2)))
                #print(str(key) + ": " + str(subSubIndex))
                return (offset + relativeOffset + self.denseDenseLookup[b][str(key)][subSubIndex])


def _calculate_rank_super_block(vec, log2sq, log2hf):
    numSuperBlocks = int(len(vec) / log2sq) + 1  # optional todo: optimize if no rounding happens
    superBlocks = [None] * numSuperBlocks
    # print("Number and lenght of SB is: " + str(numSuperBlocks) + " and " + str(log2sq))

    currentOffset = 0
    for i in range(numSuperBlocks):
        superBlocks[i] = SuperBlock(vec[(i * log2sq): ((i + 1) * log2sq)], currentOffset, log2hf)
        currentOffset = superBlocks[i].offset
        # print("Offset of SB " + str(i) + " is " + str(currentOffset))

    return superBlocks


def _calculate_select_structure(vector, log2, b):
    chunkWeight = log2 ** 2
    chunkOffsets = [0]
    counter = 0    
    
    # calculate offesets of big chunks
    for i in range(len(vector)):
        if vector[i] == b:
            counter += 1
            if counter > chunkWeight:
                chunkOffsets.append(i)
                counter = 1
    
    # append vector length for sparseness calculation of the last chunk
    chunkOffsets.append(len(vector))
    
    sparseDef = log2 ** 4    
    isSparse = [i for i in range(len(chunkOffsets) - 1)]
    sparseLookup = {}
    subChunkOffsets = {}
    
    # calculate solutions within sparse chunks, and offsets of sub-chunks in dense chunks
    # optional todo: clean weird bool array
    for i in range(len(isSparse)):
        isSparse[i] = (chunkOffsets[i+1] - chunkOffsets[i]) > sparseDef
        
        if isSparse[i] == True:
            counter = 0
            for i2 in range(chunkOffsets[i], chunkOffsets[i + 1]):
                if vector[i2] == b:
                    counter += 1
                    sparseLookup[(i * chunkWeight) + counter] = i2
                    
        else: 
            subChunkWeight = log2 ** (1/2)
            relativeOffsets = [0]
            counter = 0
            for i2 in range(chunkOffsets[i], chunkOffsets[i + 1]):
                if vector[i2] == b:
                    counter += 1
                    if counter > subChunkWeight:
                        relativeOffsets.append(i2 - chunkOffsets[i])
                        counter = 1
            relativeOffsets.append(chunkOffsets[i+1]- chunkOffsets[i])
            subChunkOffsets[chunkOffsets[i]] = relativeOffsets
            
    denseSparseLookup = {}
    denseDenseLookup = {}
    
    # calculate solutions of dense/sparse sub-chunks and lookup entries of dense/dense sub-chunks
    for chunkOffset in subChunkOffsets:
        relativeOffsets = subChunkOffsets[chunkOffset]
        for i in range(len(relativeOffsets) - 1):
           
            if (relativeOffsets[i + 1] - relativeOffsets[i]) > (log2 / 2):  
                #print(chunkOffset)
                #print(relativeOffsets[i + 1])
                #print("------")
                counter = 0
                for i2 in range(relativeOffsets[i], relativeOffsets[i + 1]):
                    if vector[chunkOffset + i2] == b: # todo stopped working here
                        counter += 1
                        denseSparseLookup[
                            int((chunkOffsets.index(chunkOffset) * chunkWeight) 
                            + i * subChunkWeight
                            + counter)
                        ] = chunkOffset + i2  
                        #print("d-s-o: " + str((chunkOffsets.index(chunkOffset) * chunkWeight)) 
                            #+ " - " + str(i * subChunkWeight)
                            #+ " - " + str(counter))
            
            else: 
                key = vector[chunkOffset + relativeOffsets[i] : chunkOffset + relativeOffsets[i + 1]]
                if str(key) not in denseDenseLookup:
                    value = []
                    for i2 in range(relativeOffsets[i], relativeOffsets[i + 1]):
                        if vector[chunkOffset + i2] == b:
                            value.append(i2 - relativeOffsets[i])
                denseDenseLookup[str(key)] = value
    
    return chunkOffsets, sparseLookup, subChunkOffsets, denseSparseLookup, denseDenseLookup
                            
                
            
                    
         

class SuperBlock:
    def __init__(self, vec, prevOffset, blockLen):
        self.vector = vec
        self.prevOffset = prevOffset
        self.blockLen = blockLen
        numBlocks = int(len(self.vector) / blockLen) + 1  # todo: check whether +1 is necessary, mby optimize
        self.blocks = [None] * numBlocks
        self.rankLookup = {}

        currentOffset = 0
        for i in range(numBlocks):
            self.blocks[i] = Block(vec[(i * blockLen): ((i + 1) * blockLen)], currentOffset)
            currentOffset = self.blocks[i].offset
            # print("Offset of Block " + str(i) + " is " + str(currentOffset))
        self.offset = prevOffset + currentOffset

    def get_rank(self, index):
        blockIndex = int(index / self.blockLen)
        mod = index % self.blockLen
        return self.prevOffset + self.blocks[blockIndex].get_rank(mod)


class Block:
    def __init__(self, vec, prevOffset):
        currentOffest = 0
        self.lookup = [None] * len(vec)
        for i in range(len(vec)):
            if vec[i] == '1':
                currentOffest += 1
            self.lookup[i] = currentOffest
        self.prevOffset = prevOffset
        self.offset = prevOffset + currentOffest

    def get_rank(self, index):
        return self.prevOffset + self.lookup[index]


# copied singleton metaclass from: https://stackoverflow.com/a/6798042
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RankLookup(object):
    __metaclass__ = Singleton
    
    def __init__(self) -> None:
        self.table = {}