#!/usr/bin/env python

import numpy as np
import sys,argparse

parser = argparse.ArgumentParser()
parser.add_argument("--graph", help="citation graph (*.X.i, *.Y.i)", required=True)
parser.add_argument("--year", help="*npy file", required=True)
parser.add_argument("--max_year", type=int, help="2025", default=2025)
parser.add_argument("--publication_year", type=int, help="2000", default=2000)

args = parser.parse_args()

year = np.load(args.year)

X=np.fromfile(args.graph + '.X.i', dtype=np.int32)
Y=np.fromfile(args.graph + '.Y.i', dtype=np.int32)

N = len(year)
# res=np.zeros((N, args.max_year - args.publication_year + 1, dtype=np.int32)

Xyear= year[X]
Yyear= year[Y]
S = Yyear == args.publication_year

corpusids = X[S]
gap = Yyear[S] - args.publication_year

for id,g in zip(corpusids, gap):
    print(str(id) + '\t' + str(g))


