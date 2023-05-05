#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-Y", "--years", help=".short file", required=True)
parser.add_argument("-o", "--output", help=".npz", required=True)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

with open(args.years, 'rb') as fd:
    years = np.frombuffer(fd.read(),dtype=np.int16)

M = my_load(args.graph)
print(str(time.time() - t0) + ' finished loading', file=sys.stderr)
sys.stderr.flush()

X,Y = M.nonzero()

print(str(time.time() - t0) + ' finished nonzero', file=sys.stderr)
sys.stderr.flush()

Xyears = years[X]
Yyears = years[Y]

np.savez(args.output, Xyears=Xyears, Yyears=Yyears)
