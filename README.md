# bitVector

As part of the lecture "Advanced Data Structures" at the KIT we are to implement and advanced bit-vector. 

Run with:

```
python (path to ads_program.py) (path to inputfile) (path to outputfile)
```

Default values for the paths are "./src/input.txt" and "./src/output.txt". The output file will be overwritten and automatically be created if it doesn't exist yet.

Contains the files
- ads_programm.py : the main script to read, interpret and evaluate the input file according to the given specifications
- MyBitVector.py : the data structure. Implements advanced structures for both rank and select requests, but is still pretty messy.
- total_size.py : contains a method to iteratively calculate the required space of some data structure, not written myself.

Imports:
- time: measure execution time
- sys: grab commandline arguments (file paths), as well as space req. calculations
- itertools: also space requirement calulations
- collections: also space requirement calculations

I tried implementing the data structures as explained in the following videos:
- Jacobson's rank: https://www.youtube.com/watch?v=M1sUZxXVjG8
- Clark's select: https://www.youtube.com/watch?v=_04wwUzqZCM

Script to iteratively calculate space requirements taken from https://code.activestate.com/recipes/577504-compute-memory-footprint-of-an-object-and-its-cont/ 
