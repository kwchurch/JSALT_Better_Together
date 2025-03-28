#!/usr/bin/env python

import sys,argparse,scipy.sparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output filename", required=True)
parser.add_argument("--make_symmetric", action='store_true')
args = parser.parse_args()

X = []
Y = []

for line in sys.stdin:
    fields = line.rstrip().split('\t')
    if fields[0] == 'row': continue
    if len(fields) < 2: continue
    x,y = fields[0:2]
    X.append(int(x))
    Y.append([int(yy) for yy in y.split('|')])

X = np.array(X, dtype=int)
Y = np.array(Y, dtype=int)
N = max(np.max(X), np.max(Y))+1
V = np.ones(Y.shape, dtype=bool).reshape(-1)    
G = scipy.sparse.csr_matrix((V, (X.repeat(Y.shape[1]), Y.reshape(-1))), shape=(N, N), dtype=bool)
if args.make_symmetric:
    G = G + G.T
scipy.sparse.save_npz(args.output, G)
    
