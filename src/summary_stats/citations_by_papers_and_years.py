#!/usr/bin/env python

import numpy as np
import sys,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help="citation graph (*.X.i, *.Y.i)", required=True)
parser.add_argument("--year", help="*npy file", required=True)
parser.add_argument("--max_year", type=int, help="2025", default=2025)
parser.add_argument("--publication_year", type=int, help="2000", default=None)
parser.add_argument("--filter", help="txt file containing list of corpus ids", default=None)
parser.add_argument("--flush", action='store_true')
args = parser.parse_args()

year = np.load(args.year)

X=np.fromfile(args.graph + '.X.i', dtype=np.int32)
Y=np.fromfile(args.graph + '.Y.i', dtype=np.int32)

N = len(year)
# res=np.zeros((N, args.max_year - args.publication_year + 1, dtype=np.int32)

filter=None
if not args.filter is None:
    ids = np.loadtxt(args.filter, dtype=np.int32)
    filter = dict(zip(ids,ids))

Xyear= year[X]
Yyear= year[Y]

if not args.publication_year is None:
    S = Yyear == args.publication_year

    for id2,gap in zip(Y[S], Xyear[S] - args.publication_year):
        if filter is None or id2 in filter:
            print('\t'.join(map(str,[id2, gap])))
            if args.flush: sys.stdout.flush()

else:
    for id2,x,y in zip(Y, Xyear, Yyear):
        if filter is None or id2 in filter:
            print('\t'.join(map(str,[id2, x, y])))
            if args.flush: sys.stdout.flush()
    

# for id1,id2,y1,y2 in zip(X, Y, Xyear, Yyear):
#     print('\t'.join(map(str,[id1,id2, y1, y2])))


