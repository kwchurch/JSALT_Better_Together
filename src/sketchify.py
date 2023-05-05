#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np
import random

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-R", "--report", type=int, help="interval for reporting progress", default=1000)
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-T", '--transpose', action='store_true')
parser.add_argument("-K", '--n_components', type=int, default=100)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
if args.transpose: M = M.T

N = M.shape[0]
print(str(time.time() - t0) + ' finished loading M; shape: ' + str(M.shape), file=sys.stderr)
sys.stderr.flush()

P = np.random.permutation(N)
fanout = np.sum(M, axis=0)

def sketch(row):
    res = scipy.sparse.lil_matrix((1,N), dtype=bool)
    _,Y = row.nonzero()
    Ps = P[Y]
    pairs = sorted([ (p,y) for p,y in zip(Ps,Y)], key = lambda pair: pair[0])[0:args.n_components]
    for p,y in pairs:
        row[0,y]=1
    return res

S = scipy.sparse.lil_matrix(M.shape, dtype=bool)

print(str(time.time() - t0) + ' starting crux', file=sys.stderr)
sys.stderr.flush()

for i in range(N):
    if i>0 and i%args.report == 0:
        t1 = time.time() - t0
        print('i = %d of %d, sec = %f, i per sec = %f, ETA = %f' % (i, N, t1, i/t1, (N * t1/i - t1)), file=sys.stderr)
        sys.stderr.flush()
    f = fanout[0,i]
    if f <= 0: continue
    if f < args.n_components:
        S[i,:] = M[i,:]
    else:
        print('about to call sketch on i: %s with f: %d ' % (i, f), file=sys.stderr)
        sys.stderr.flush()
        S[i,:] = sketch(M[i,:])

print(str(time.time() - t0) + ' finished crux', file=sys.stderr)
sys.stderr.flush()

S = scipy.sparse.csr_matrix(S, dtype=bool)

print(str(time.time() - t0) + ' saving results', file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(args.output, S)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
