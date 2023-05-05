#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np
import random

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-l", "--limit", type=int, help="max number of steps", default=3)
parser.add_argument("-s", "--starting_point", type=int, help="starting point", required=True)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
print(str(time.time() - t0) + ' finished loading', file=sys.stderr)
sys.stderr.flush()

reachable = {}

def do_step(step):
    sstep = str(step)
    found = np.array([k for k in reachable], dtype=int)
    _,Y = M[found,:].nonzero()
    for y in Y:
        if not y in reachable:
            reachable[y]=step
            print(str(y) + '\t' + sstep);
    X,_ = M[:,found].nonzero()
    for x in X:
        if not x in reachable:
            reachable[x]=step
            print(str(x) + '\t' + sstep);

# for line in sys.stdin:
#     rline = line.rstrip()
#     if len(rline) > 0:
#         reachable[int(rline)] = -1

reachable[args.starting_point] = -1
print(str(args.starting_point) + '\t-1')
sys.stdout.flush()

for step in range(args.limit):
    do_step(step)
    print(str(time.time() - t0) + ' finished step: ' + str(step) + ' ; len(reachable): ' + str(len(reachable)), file=sys.stderr)
    sys.stdout.flush()

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
