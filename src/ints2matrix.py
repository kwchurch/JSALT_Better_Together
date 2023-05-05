#!/usr/bin/env python

import numpy as np
import os,sys,argparse,scipy.sparse,time

parser = argparse.ArgumentParser()
parser.add_argument("-X", "--X", help="filename", required=True)
parser.add_argument("-Y", "--Y", help="filename", required=True)
parser.add_argument('-V', '--vals', help="*.npz file", default=None)
parser.add_argument('-o', '--output', help="*.npz file", required=True)
parser.add_argument('-S', '--shape', help="108651994,77585514", required=True)
# Do not do this
# parser.add_argument('--normalize', help="normalize rows by l2", action='store_true')
# 108651994,77585514
args = parser.parse_args()

nX,nY = args.shape.split(',')

with open(args.X, 'rb') as fd:
    X = np.frombuffer(fd.read(), dtype=np.int32)

with open(args.Y, 'rb') as fd:
    Y = np.frombuffer(fd.read(), dtype=np.int32)

assert len(X) == len(Y), 'length mismatch: X != Y'

if not args.vals is None:
    with open(args.vals, 'rb') as fd:
        vals = np.frombuffer(fd.read(), dtype=np.int32)
        assert len(vals) == len(Y), 'length mismatch: vals != Y'
        M = scipy.sparse.csr_matrix((vals, (X, Y)), dtype=np.int32, shape=(int(nX), int(nY)))
        scipy.sparse.save_npz(args.output, M)

else:
    vals = np.ones(len(X), dtype=bool)
    M = scipy.sparse.csr_matrix((vals, (X, Y)), dtype=bool, shape=(int(nX), int(nY)))
    scipy.sparse.save_npz(args.output, M)


# if args.normalize:
#     from sklearn.preprocessing import normalize
#     Mnorm = normalize(M, norm='l2', axis=1)
#     scipy.sparse.save_npz(args.output, Mnorm)
# else:

