#!/usr/bin/env python

import sys,os,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", required=True)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

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

for line in sys.stdin:
    # print('line: ' + line)
    x = line.rstrip()
    if len(x) > 0:
        row = extract_row(int(x))
        # print(row)
        for y in row:
            print(x + '\t' + str(y))

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
