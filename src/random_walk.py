#!/usr/bin/env python

import scipy.sparse,argparse,numpy.random

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-N", "--restarts", type=int, help="rstarts", default=1000)
parser.add_argument("-D", "--depth", type=int, help="rstarts", default=10)
parser.add_argument("-S", "--make_symmetric", action='store_true')
parser.add_argument("-T", "--transpose", action='store_true')
args = parser.parse_args()

M = scipy.sparse.load_npz(args.graph)

if args.make_symmetric:
    M = M + M.T

if args.transpose:
    M = M.T

def walk(s0, i, depth):
    print('\t'.join(map(str, [s0, i, depth])))
    if depth < args.depth:
        X,Y = M[i,:].nonzero()
        if len(Y) > 0:
            j = numpy.random.choice(Y)        
            walk(s0, j, depth+1)

X,Y = M.nonzero()

for i in numpy.random.choice(X, args.restarts):
    walk(i, i, 0)


