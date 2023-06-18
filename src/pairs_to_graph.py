#!/usr/bin/env python

import os,sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-N", "--N", type=int, default=270000000)
parser.add_argument("-d", "--dtype", default='float16')
args = parser.parse_args()

dtypes = { 'int8' : np.int8,
           'int16' : np.int16,
           'int32' : np.int32,
           'int64' : int,
           'int' : int,
           'float16' : np.float16,
           'float32' : np.float32,
           'float64' : float,
           'float' : float}

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def map_int(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=int, shape=(int(fn_len/8)), mode='r')

def map_float32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/4)), mode='r')

assert args.dtype in dtypes, 'bad dtype arg: ' + args.dtype
X = map_int32(args.input + '.X.i')
Y = map_int32(args.input + '.Y.i')
V = map_float32(args.input + '.f')

print('X.shape: ' + str(X.shape), file=sys.stderr)
print('Y.shape: ' + str(Y.shape), file=sys.stderr)
print('V.shape: ' + str(V.shape), file=sys.stderr)

# pairs = np.loadtxt(sys.stdin, dtype=np.int32)

print(str(time.time() - t0) + ' loaded pairs', file=sys.stderr)
sys.stderr.flush()

# V = pairs[:,0].reshape(-1)
# X = pairs[:,0]
# Y = pairs[:,1]
# V = np.ones(len(X),dtype=bool)

# M = scipy.sparse.csr_matrix((V, (X, Y)), shape=(args.N, args.N), dtype=dtypes[args.dtype])
M = scipy.sparse.csr_matrix((V, (X, Y)), shape=(args.N, args.N))

M += M.T

print(str(time.time() - t0) + ' make symmetric', file=sys.stderr)
sys.stderr.flush()



scipy.sparse.save_npz(args.output, M)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
