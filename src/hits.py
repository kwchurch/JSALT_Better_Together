#!/usr/bin/env python

import sys,scipy.sparse,argparse,time,json
import numpy as np
import networkx as nx

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-T", '--transpose', action='store_true')
# parser.add_argument("-a", "--alpha", type=float, help="argument to page rank", default=0.9)
args = parser.parse_args()

M = scipy.sparse.load_npz(args.graph)
if args.transpose: M = M.T

print(str(time.time() - t0) + ' loaded M', file=sys.stderr)
sys.stderr.flush()

G = nx.from_scipy_sparse_array(M)

print(str(time.time() - t0) + ' converted to nx graph', file=sys.stderr)
sys.stderr.flush()

h = nx.hits(G)

print(str(time.time() - t0) + ' hits computed', file=sys.stderr)
sys.stderr.flush()

with open(args.output, 'w') as fd:
    json.dump(h, fd)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()

