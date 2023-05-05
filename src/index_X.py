#!/usr/bin/env python

import sys,argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-X", "--X", help=".npy file", required=True)
parser.add_argument("-O", "--output", required=True)
args = parser.parse_args()

assert args.X.endswith('.npy') or args.X.endswith('.i'), 'bad -X arg'
assert args.output.endswith('.npy') or args.output.endswith('.i'), 'bad -O arg'

if args.X.endswith('.npy'):
    X = np.load(args.X)
else:
    X = np.fromfile(args.X, dtype=np.int32)

idx = np.cumsum(np.bincount(X))

if args.output.endswith('.npy'): 
    np.save(args.output, idx)
else:
    idx.astype(np.int32).tofile(args.output)

