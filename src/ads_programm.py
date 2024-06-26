# parser script to interpret input file

# todo accept parameters

inputFile = "input.txt"
outputFile = "output.txt"

with open(inputFile) as f:
    cmdCount = int(f.readline())
    bitVectorString = f.readline()

    # todo init bitVector

    for line in f:
        cmd = line.strip().split(" ")
        print(cmd)
        # todo switch over possible commands


# optional todo: implement any amount of error handling
