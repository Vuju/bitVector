# parser script to interpret input file

import time
import sys

from MyBitVector import MyBitVector

start_time = time.time()

inputFile = "./src/input.txt"
outputFile = "./src/output.txt"

try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
except IndexError:
    pass

with open(inputFile) as input:
    cmdCount = int(input.readline())
    bitVectorString = input.readline().strip()

    bitVector = MyBitVector(bitVectorString)

    ops = {
        "rank": bitVector.rank,
        "select": bitVector.select,
        "access": bitVector.access
    }

    
    
    output = open(outputFile, 'w+')
    for line in input:
        comm = line.strip().split(" ", 1)                   # this only splits the command from the arguments,
        output.write(str(ops[comm[0]](comm[1])) + '\n')     # therefore this line passes all arguments as a single string!
    output.close()

print("RESULT name=julian_vu time={0} space={1}".format(((time.time() - start_time) / 1000), bitVector.space()))

# optional todo: implement any amount of error handling
