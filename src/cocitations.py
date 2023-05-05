#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np
import random

t0 = time.time()

assert False, 'Deprecated; use /work/k.church/semantic_scholar/citations/graphs/src/C/cocitations.c'

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", default='/work/k.church/semantic_scholar/citations/graphs/citations.G.npz')
parser.add_argument("-o", "--output", help="output", default='/work/k.church/semantic_scholar/citations/graphs/co-citations.G.npz')
parser.add_argument("-A", '--do_all', action='store_true')

args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
print(str(time.time() - t0) + ' finished loading', file=sys.stderr)
sys.stderr.flush()

if args.do_all:
    Mint = scipy.sparse.csr_matrix(M.T, dtype=int);
    # M2 = M.T @ M
    M2 = Mint @ Mint.T

    print(str(time.time() - t0) + ' finished computing', file=sys.stderr)
    sys.stderr.flush()

    scipy.sparse.save_npz(args.output, M2)

else:
    print('\t'.join(["p1", "p1_fanin", "p1_fanout", "p2", "p2_fanin", "p2_fanout", "cocites", "cotrash"]))
    for line in sys.stdin:
        fields = line.rstrip().split()
        if len(fields) >= 2:
            p1,p2 = fields[0:2]
            p1 = int(p1)
            p2 = int(p2)
            cocites = M.T[p1,:] @ M[:,p2]
            cotrash = M[p1,:] @ M.T[:,p2]

            p1_fanin = M[:,p1].count_nonzero()
            p1_fanout = M[p1,:].count_nonzero()

            p2_fanin = M[:,p2].count_nonzero()
            p2_fanout = M[p2,:].count_nonzero()

            print('\t'.join(map(str, [p1, p1_fanin, p1_fanout, p2, p2_fanin, p2_fanout, cocites, cotrash])))
            sys.stdout.flush()

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
