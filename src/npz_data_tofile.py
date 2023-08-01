#!/usr/bin/env python

import sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-o", "--output", help="output", required=True)
args = parser.parse_args()

M = np.load(args.graph)

print(str(time.time() - t0) + ' loaded M', file=sys.stderr)
sys.stderr.flush()

M['data'].tofile(args.output + '.f')

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()

