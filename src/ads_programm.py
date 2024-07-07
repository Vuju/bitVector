# parser script to interpret input file

import time
import sys
from MyBitVector import MyBitVector

start_time = time.time()

inputFile = "input.txt"
outputFile = "output.txt"

try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
except IndexError:
    pass

with open(inputFile) as f:
    cmdCount = int(f.readline())
    bitVectorString = f.readline()

    bitVector = MyBitVector(bitVectorString)

    ops = {
        "rank": bitVector.rank,
        "select": bitVector.select,
        "access": bitVector.access
    }

    for line in f:
        comm = line.strip().split(" ", 1)  # this only splits the command from the arguments,
        print(ops[comm[0]](comm[1]))       # therefore this line passes all arguments as a single string!

print("RESULT name=julian_vu time={0} space={1}".format(int((time.time() - start_time) / 1000), "dunno"))

# todo: write back results
# todo: do proper analysis of time and space usage
# optional todo: implement any amount of error handling
