#!/usr/bin/env python

import os,sys,argparse,time,glob
from scipy.sparse import lil_matrix,csr_matrix
import numpy as np

t0 = time.time()

print('merge_faiss_binary_output: ' + str(sys.argv), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input files; glob is ok", required=True)
parser.add_argument("--output", help="output", required=True)
parser.add_argument('--binary_input', help="input file (optional, use text input from stdin by default)", default=None)
parser.add_argument('--topN', type=int, help="top N to keep", default=40)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def map_float32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/4)), mode='r')

outX = open(args.output + ".X.i", "wb")
outY = open(args.output + ".Y.i", "wb")
outV = open(args.output + ".V.f", "wb")

Xfiles = glob.glob(args.input + '.X.i')
Yfiles = glob.glob(args.input + '.Y.i')
Vfiles = glob.glob(args.input + '.V.f')

print("len(Xfiles): " + str(len(Xfiles)), file=sys.stderr)

X=[map_int32(f) for f in Xfiles]
Y=[map_int32(f) for f in Yfiles]
V=[map_float32(f) for f in Vfiles]

Nx = max([np.max(x) for x in X]) + 1
Ny = max([np.max(y) for y in Y]) + 1

print("Nx, Ny = ", str((Nx, Ny)), file=sys.stderr)

Startx = min([np.min(x) for x in X])

# for x,F in zip(X,Xfiles):
#     print('\t'.join(map(str, [F, np.min(x), np.max(x)])))

# for y,F in zip(Y,Yfiles):
#     print('\t'.join(map(str, [F, np.min(y), np.max(y)])))

# for v,F in zip(V,Vfiles):
#     print('\t'.join(map(str, [F, np.min(v), np.max(v)])))

def my_matrix(x,y,v):
    s = y > 0
    return csr_matrix((v[s], (x[s], y[s])),
                      shape=(Nx, Ny),
                      dtype=np.float32)

M=[my_matrix(x,y,v) for x,y,v in zip(X,Y,V)]

for row in range(max(1,Startx), Nx):
    # print('row = ' + str(row), file=sys.stderr)
    Yrow = []
    Vrow = []
    for m in M:
        _,y = m[row,:].nonzero()
        if len(y) < 1: continue
        v = np.array(m[row,y].todense()).reshape(-1)

        # print('y.shape = ' + str(y.shape), file=sys.stderr)
        # print('v.shape = ' + str(v.shape), file=sys.stderr)

        assert len(y) == len(v), 'confusion 0'

        Yrow.append(y)
        Vrow.append(v)
    Yrow = np.concatenate(Yrow)
    Vrow = np.concatenate(Vrow)

    assert len(Yrow) == len(Vrow), 'confusion 1'

    o = np.argsort(Vrow)[0:args.topN]

    # print(o, file=sys.stderr)

    assert max(o) < len(Vrow), 'confusion 2'
    assert max(o) < len(Yrow), 'confusion 3'

    Xrow = np.repeat(row, args.topN).astype(np.int32)
    Xrow.tofile(outX)
    Yrow[o].tofile(outY)
    Vrow[o].tofile(outV)
    outX.flush()
    outY.flush()
    outV.flush()

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
