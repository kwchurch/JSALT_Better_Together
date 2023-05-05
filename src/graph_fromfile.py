#!/usr/bin/env python

import sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-N", "--N", type=int, default=None)
parser.add_argument("-d", "--dtype", default='int32')

args = parser.parse_args()

dtypes = { 'int32' : np.int32,
           'int64' : np.int64}

assert args.dtype in dtypes, 'bad dtype arg: ' + args.dtype

X = np.fromfile(args.input + '.X', dtypes[args.dtype])
Y = np.fromfile(args.input + '.Y', dtypes[args.dtype])

print(str(time.time() - t0) + ' loaded X and Y', file=sys.stderr)
sys.stderr.flush()

print('X.min: ' + str(np.min(X)), file=sys.stderr)
print('X.max: ' + str(np.max(X)), file=sys.stderr)
print('len(X): ' + str(len(X)), file=sys.stderr)
print('X[0:10]: ' + '|'.join(map(str, X[0:10])), file=sys.stderr)

print('Y.min: ' + str(np.min(Y)), file=sys.stderr)
print('Y.max: ' + str(np.max(Y)), file=sys.stderr)
print('len(Y): ' + str(len(Y)), file=sys.stderr)
print('Y[0:10]: ' + '|'.join(map(str, Y[0:10])), file=sys.stderr)

sys.stderr.flush()

if args.N is None:
    N = 1+max(np.max(Y), np.max(X))
else:
    N = args.N

V = np.ones(len(X), dtype=bool)

M = scipy.sparse.csr_matrix((V, (X, Y)), shape=(N, N), dtype=bool)
scipy.sparse.save_npz(args.output, M)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
