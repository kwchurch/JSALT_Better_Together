#!/usr/bin/env python

import numpy as np
import sys,argparse,time,json
from sklearn.metrics.pairwise import cosine_similarity

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-X", "--X", help="a filename", required=True)
parser.add_argument("-Y", "--Y", help="a filename", required=True)
parser.add_argument("-K", "--record_size", type=int, help="a filename", default=None);
args = parser.parse_args()

def load_file(fn):
    if fn.endswith('.npy'):
        return np.load(fn)
    elif fn.endswith('f'):
        assert not args.record_size is None, '--record_size is required with *.f input files'
        with open(fn, 'rb') as fd:
            return np.frombuffer(fd.read(), dtype=np.float32).reshape(-1, args.record_size)
    else: assert False, 'load_file, unknown file extension; ' + fn

X = load_file(args.X)    
Y = load_file(args.Y)

assert X.shape[1] == Y.shape[1], 'shape mismatch: X.shape = ' + str(X.shape) + ' and Y.shape = ' + str(Y.shape)

sim = cosine_similarity(X, Y)

import pdb
pdb.set_trace()
