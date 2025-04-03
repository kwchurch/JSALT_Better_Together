#!/usr/bin/env python

import sys,argparse
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from scipy.linalg import svd

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="filename", required=True)
parser.add_argument("-o", "--output", help="filename", required=True)
parser.add_argument("--topN", type=int, help="number of values to keep", required=True)
parser.add_argument("--n_components", type=int, help="number of values to keep", default=None)
args = parser.parse_args()

f=args.input

if f.endswith('npz'):
    Z=np.load(f)['embeddings'].astype('float32')
else:
    Z=np.load(f)

K = args.n_components
if K is None or K > Z.shape[1]:
    K = Z.shape[1]

S = cosine_similarity(Z)
S2 = np.zeros(S.shape, dtype=np.float32)

for i in range(len(S)):
    o = np.argsort(-S[i,:])[0:args.topN]
    S2[i,o] = S[i,o]

S2 = np.maximum(S2,S2.T)

U,D,Vt = svd(S2)

if K < len(D):
    U = U[:,0:K]
    D = D[0:K]

Z2 = normalize(U @ np.diag(np.sqrt(D)))

np.save(args.output, Z2)



