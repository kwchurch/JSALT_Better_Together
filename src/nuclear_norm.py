#!/usr/bin/env python

import numpy as np
import sys
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

def H(D):
    P = D/np.sum(D)
    logP = np.log(P)
    return np.sum(P * logP)/-np.log(2)

# deciles = np.arange(11)/10
# q = [0.9, 0.95, 0.99, 0.999]

for f in sys.argv[1:]:
    if f.endswith('npz'):
        Z=np.load(f)['embeddings'].astype('float32')
    else:
        Z=np.load(f).astype('float32')
    nZ = normalize(Z)
    U,D,Vt = np.linalg.svd(nZ)
    # S = cosine_similarity(Z)
    # print('\t'.join(map(str, [f, np.sum(D), np.var(S), '\t'.join(map(str, np.quantile(S, deciles)))])))
    print('\t'.join(map(str, [f, np.sum(D), np.sum(D[0:280]), H(D), H(D[0:280]), len(D), len(Z)])))
    print('#D: ' + ' '.join(map(str, D)))
    sys.stdout.flush()



