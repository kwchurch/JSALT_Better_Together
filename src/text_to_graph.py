#!/usr/bin/env python

import sys,scipy.sparse,time
import numpy as np

t0 = time.time()

print('text_to_graph: ' + str(sys.argv), file=sys.stderr)

def load_text_file(fn):
    # N =  270000000
    # A = 2300000000
    x = np.loadtxt(fn, dtype=int)
    print('load_text_file: ' + str(fn) + ' shape= ' + str(x.shape), file=sys.stderr)
    sys.stderr.flush()
    return x
   
    # X = x[:,0].reshape(-1)
    # Y = x[:,1].reshape(-1)
    # V = np.ones(len(X), dtype=bool)
    # return scipy.sparse.csr_matrix((V, (X, Y)), shape=(N, A), dtype=bool)

def my_to_matrix(x, shape):
    X = x[:,0].reshape(-1)
    Y = x[:,1].reshape(-1)
    V = np.ones(len(X), dtype=bool)
    return scipy.sparse.csr_matrix((V, (X, Y)), shape=shape, dtype=bool)

M0 = [ load_text_file(fn) for fn in sys.argv[2:] ]

print(str(time.time() - t0) + ' loaded M0', file=sys.stderr)
sys.stderr.flush()

N0 = 1+max([np.max(x[:,0]) for x in M0])
N1 = 1+max([np.max(x[:,1]) for x in M0])
shape = (N0, N1)

print(str(time.time() - t0) + ' shape: ' + str(shape), file=sys.stderr)
sys.stderr.flush()

M = [ my_to_matrix(m,shape) for m in M0 ]

print(str(time.time() - t0) + ' loaded M', file=sys.stderr)
sys.stderr.flush()

print(str(time.time() - t0) + ' about to sum', file=sys.stderr)
sys.stderr.flush()

MM = sum(M)

GB = (MM.data.nbytes + MM.indices.nbytes + MM.indptr.nbytes)/1e9

print(str(time.time() - t0) + ' about to save, MM has %0.3f GB' % GB, file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(sys.argv[1], MM)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
