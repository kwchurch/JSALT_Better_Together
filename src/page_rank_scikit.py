#!/usr/bin/env python

# https://scikit-network.readthedocs.io/en/latest/tutorials/ranking/pagerank.html

import sys,scipy.sparse,argparse,time,json
import numpy as np
from sknetwork.ranking import PageRank
# import networkx as nx

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-T", '--transpose', action='store_true')
parser.add_argument("-d", "--damping_factor", type=float, help="argument to page rank [default: 0.85]", default=0.85)
parser.add_argument("-s", "--solver", help="piteration|diteration|lanczos|bicgstab|RH|push", default='piteration')
parser.add_argument("-N", "--n_iter", type=int, help="argument to page rank [default: 10]", default=10)
parser.add_argument("-t", "--tol", type=float, help="argument to page rank [default: 1e-6]", default=1e-6)
args = parser.parse_args()

M = scipy.sparse.load_npz(args.graph)
if args.transpose: M = M.T

print(str(time.time() - t0) + ' loaded M', file=sys.stderr)
sys.stderr.flush()

M = scipy.sparse.csr_matrix(M)

print(str(time.time() - t0) + ' converted to csr_matrix', file=sys.stderr)
sys.stderr.flush()

# G = nx.from_scipy_sparse_array(M)
# print(str(time.time() - t0) + ' converted to nx graph', file=sys.stderr)
# sys.stderr.flush()

pagerank = PageRank(damping_factor=args.damping_factor, solver=args.solver, n_iter=args.n_iter, tol=args.tol)
scores = pagerank.fit_transform(M)
# pr = nx.pagerank(G, alpha=args.alpha)

print(str(time.time() - t0) + ' page rank computed', file=sys.stderr)
sys.stderr.flush()

np.save(args.output, scores)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()

