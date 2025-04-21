#!/usr/bin/env python

import sys,argparse
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from scipy.linalg import svd

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="filename", required=True)
# parser.add_argument("-o", "--output", help="filename", required=True)
parser.add_argument("--topN", type=int, help="number of values to keep", default=2)
# parser.add_argument("--n_components", type=int, help="number of values to keep", default=None)
# parser.add_argument("--jpeg", help="filename", default=None)
args = parser.parse_args()

f=args.input

if f.endswith('npz'):
    Z=np.load(f)['embeddings'].astype('float32')
else:
    Z=np.load(f).astype('float32')

S = cosine_similarity(Z)

for i in range(len(S)):
    o = np.argsort(-S[i,:])[0:args.topN]
    for j,v in zip(o, S[i,o]):
        if i != j:
            print('\t'.join(map(str, [i, j, v])))


