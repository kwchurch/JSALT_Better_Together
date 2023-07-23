#!/usr/bin/env python

import sys,argparse
import numpy as np
import numpy.linalg

parser = argparse.ArgumentParser()
parser.add_argument("--embedding", required=True)
parser.add_argument("--map", required=True)
args = parser.parse_args()

M = np.load(args.embedding)

map = np.load(args.map + '.old_to_new.i.npy')

def my_cos(vec1, vec2):
    return vec1.dot(vec2)/(np.linalg.norm(vec1) * np.linalg.norm(vec2))

for line in sys.stdin:
    fields = line.rstrip().split()
    if len(fields) >= 2:
        id1 = int(fields[0])
        id2 = int(fields[1])
        if id1 < len(map) and id2 < len(map):
            print(str(my_cos(M[map[id1],:], M[map[id2],:])) + '\t' + line.rstrip())
        else:
            print('-1\t' + line.rstrip())

