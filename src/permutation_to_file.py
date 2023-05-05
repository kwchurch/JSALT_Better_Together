#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np
import random

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-S", "--seed", type=int, default=42)
parser.add_argument("-N", "--N", type=int, required=True)
args = parser.parse_args()

np.random.seed(args.seed)

N=args.N
idx = np.arange(N, dtype=np.int32)
P = np.random.permutation(N).astype(np.int32)
Pinv = np.zeros(N, dtype=np.int32)
Pinv[P] = idx

P.tofile(args.output + '.P')
Pinv.tofile(args.output + '.Pinv')
