# parser script to interpret input file
import time
from MyBitVector import myBitVector
start_time = time.time()


# todo accept parameters

inputFile = "input.txt"
outputFile = "output.txt"

with open(inputFile) as f:
    cmdCount = int(f.readline())
    bitVectorString = f.readline()

    bitVector = myBitVector(bitVectorString)
    print(bitVector.vector)

    for line in f:
        cmd = line.strip().split(" ")
        print(cmd)
        # todo switch over possible commands

print("RESULT name=julian_vu time={0} space={1}".format(int((time.time() - start_time) / 1000), "dunno"))
# optional todo: implement any amount of error handling
