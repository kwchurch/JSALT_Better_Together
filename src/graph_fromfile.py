#!/usr/bin/env python

import os,sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

print('graph_fromfile: ' + str(sys.argv), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-N", "--N", type=int, default=None)
parser.add_argument("-d", "--dtype", default='int32')
parser.add_argument("-T", '--text_mode', action='store_true')
parser.add_argument("--suffix", default=None)

args = parser.parse_args()

dtypes = { 'int32' : np.int32,
           'int64' : np.int64}

assert args.dtype in dtypes, 'bad dtype arg: ' + args.dtype

def my_pathname(base, ext):
    res = base+ext;
    if args.suffix: res += args.suffix
    return res

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

if args.text_mode:
    X = np.loadtxt(args.input + '.X.txt', dtypes[args.dtype])
    Y = np.loadtxt(args.input + '.Y.txt', dtypes[args.dtype])
if dtypes[args.dtype] == np.int32:
    X = map_int32(my_pathname(args.input, '.X'))
    Y = map_int32(my_pathname(args.input, '.Y'))
else:
    X = np.fromfile(my_pathname(args.input, '.X'), dtypes[args.dtype])
    Y = np.fromfile(my_pathname(args.input, '.Y'), dtypes[args.dtype])

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
