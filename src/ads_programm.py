# parser script to interpret input file

import time
import sys
import MyBitVector

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
    options = {
        "rank": bitVector.rank,
        "select": bitVector.select,
        "access": bitVector.access
    }

    for line in f:
        cmd = line.strip().split(" ", 1)  # this only splits the command from the arguments,
        options[cmd[0]](cmd[1])           # therefore this line passes all arguments as a single string!

print("RESULT name=julian_vu time={0} space={1}".format(int((time.time() - start_time) / 1000), "dunno"))
# optional todo: implement any amount of error handling
