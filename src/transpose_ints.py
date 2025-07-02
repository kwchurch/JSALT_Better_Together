#!/usr/bin/env python

import os,sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

print('transpose_ints: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="filename (without .X.i and .Y.i)", required=True)
args = parser.parse_args()

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

X = map_int32(args.input + '.X.i')
Y = map_int32(args.input + '.Y.i')

Nx = 1+np.max(X)
Ny = 1+np.max(Y)

V = np.ones(len(X), dtype=bool)

M = scipy.sparse.csr_matrix((V, (Y, X)), shape=(Ny, Nx), dtype=bool)

print('sec: %0.2f: M.shape = %s' % (time.time() - t0, str(M.shape)), file=sys.stderr)
sys.stderr.flush()

X,Y = M.nonzero()

X.astype(np.int32).tofile(args.input + '.T.X.i')
Y.astype(np.int32).tofile(args.input + '.T.Y.i')

print('sec: %0.2f: done' % (time.time() - t0), file=sys.stderr)
