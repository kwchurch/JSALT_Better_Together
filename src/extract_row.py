#!/usr/bin/env python

import sys,os,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", required=True)
parser.add_argument('--has_values', action='store_true')
parser.add_argument('--longs_and_doubles', action='store_true')
args = parser.parse_args()

def map_float64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=float, shape=(int(fn_len/8)), mode='r')

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

if args.longs_and_doubles:
    Y = map_int64(args.graph + '.Y.i')
    if not os.path.exists(args.graph + '.X.i.idx'):
        print('%0.0f sec: computing idx' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        X = map_int64(args.graph + '.X.i')
        res = np.cumsum(np.bincount(X))
        res.tofile(args.graph + '.X.i.idx')
        print('%0.0f sec: idx computed' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
else:
    Y = map_int32(args.graph + '.Y.i')
    if not os.path.exists(args.graph + '.X.i.idx'):
        print('%0.0f sec: computing idx' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        X = map_int32(args.graph + '.X.i')
        res = np.cumsum(np.bincount(X))
        res.tofile(args.graph + '.X.i.idx')
        print('%0.0f sec: idx computed' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()

idx = map_int64(args.graph + '.X.i.idx')

vals = None

if args.has_values:
    vals = map_float64(args.graph + '.f')

# print('len(idx): ' + str(len(idx)))
# print(idx[0:10])

def extract_row(x):
    # print('extract_row: ' + str(x))
    if x >= len(idx) or x < 0:
        return []
    if x == 0:
        return Y[:idx[0]]
    else:
        return Y[idx[x-1]:idx[x]]

def extract_row_vals(x):
    # print('extract_row: ' + str(x))
    if x >= len(idx) or x < 0:
        return []
    if x == 0:
        return vals[:idx[0]]
    else:
        return vals[idx[x-1]:idx[x]]

if args.has_values:
    for line in sys.stdin:
        x = line.rstrip()
        ix = int(x)
        if len(x) > 0:
            for y,v in zip(extract_row(ix), extract_row_vals(ix)):
                print('\t'.join(map(str, [x, y, v])))
else:
    for line in sys.stdin:
        x = line.rstrip()
        if len(x) > 0:
            row = extract_row(int(x))
            for y in row:
                print(x + '\t' + str(y))

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
