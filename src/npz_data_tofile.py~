#!/usr/bin/env python

import sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-T", '--transpose', action='store_true')
parser.add_argument("-S", '--make_symmetric', action='store_true')
parser.add_argument("-d", "--dtype", default=None)
# parser.add_argument("-s", '--sep', help="arg to numpy.ndarray.tofile", default='')
args = parser.parse_args()

# print(str(time.time() - t0) + ' args.sep = ' + str(args.sep), file=sys.stderr)
# sys.stderr.flush()

dtypes = { 'int8' : np.int8,
           'int16' : np.int16,
           'int32' : np.int32,
           'int64' : int,
           'int' : int,
           'float16' : np.float16,
           'float32' : np.float32,
           'float64' : float,
           'float' : float}

assert args.dtype is None or args.dtype in dtypes, 'bad arg: ' + str(args.dtype)

M = scipy.sparse.load_npz(args.graph)

print(str(time.time() - t0) + ' loaded M', file=sys.stderr)
sys.stderr.flush()

if args.transpose: M = M.T
if args.make_symmetric: M += M.T

print(str(time.time() - t0) + ' transpose/symmetry done ', file=sys.stderr)
sys.stderr.flush()


X,Y = M.nonzero()

print('X.dtype: ' + str(X.dtype), file=sys.stderr)
print('X.min: ' + str(np.min(X)), file=sys.stderr)
print('X.max: ' + str(np.max(X)), file=sys.stderr)
print('len(X): ' + str(len(X)), file=sys.stderr)
print('X[0:10]: ' + '|'.join(map(str, X[0:10])), file=sys.stderr)

print('Y.dtype: ' + str(Y.dtype), file=sys.stderr)
print('Y.min: ' + str(np.min(Y)), file=sys.stderr)
print('Y.max: ' + str(np.max(Y)), file=sys.stderr)
print('len(Y): ' + str(len(Y)), file=sys.stderr)
print('Y[0:10]: ' + '|'.join(map(str, Y[0:10])), file=sys.stderr)

print(str(time.time() - t0) + ' computed X and Y', file=sys.stderr)
sys.stderr.flush()

# I wanted to write these out as binary ints,
# but I think we have a bunch of incompatible hardwares across the cluster

if not args.dtype is None:
    M.data.astype(dtypes[args.dtype]).tofile(args.output + '.f')

X.tofile(args.output + '.X.i')
Y.tofile(args.output + '.Y.i')

print(str(time.time() - t0) + ' binary written', file=sys.stderr)
sys.stderr.flush()

# This seems to be too slow
# np.savetxt(args.output + '.X', X, fmt='%d')
# np.savetxt(args.output + '.Y', Y, fmt='%d')

# np.save(args.output + '.X', X)
# np.save(args.output + '.Y', Y)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()

