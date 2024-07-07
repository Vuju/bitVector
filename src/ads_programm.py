# parser script to interpret input file

import time
import sys
import MyBitVector
start_time = time.time()


# todo accept parameters

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

    MyBitVector

    for line in f:
        cmd = line.strip().split(" ")
        print(cmd)
        # todo switch over possible commands
        time.sleep(1)

print("RESULT name=julian_vu time={0} space={1}".format(int((time.time() - start_time) / 1000), "dunno"))
# optional todo: implement any amount of error handling
