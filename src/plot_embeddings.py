#!/usr/bin/env python

import sys
from matplotlib import pyplot as plt
import numpy as np
from scipy.cluster import hierarchy
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import svd

T = int(sys.argv[1])

o = None

for f in sys.argv[2:]:

    X = np.load(f)
    if f.endswith('npz'):
        X = X['embeddings']

    if len(X) > T:
        X = X[0:T,:]

    # if o is None:
    #     Z = hierarchy.ward(X)
    #     o = hierarchy.leaves_list(Z)

    # X = X[o,:]
    S = cosine_similarity(X)
    S1 = S.reshape(-1)

    m = np.quantile(S1, 0.95)
    S1 = S1[S1 > m]

    plt.clf()
    plt.hist(S1, bins=100)
    plt.savefig(f + '.hist.jpg')

    plt.clf()
    plt.imshow(S)
    plt.colorbar()
    plt.savefig(f + '.S.jpg')
    # plt.show()
    plt.clf()

    U,D,Vt = svd(S)
    Z = normalize(U @ np.diag(np.sqrt(D)))

    U,D,Vt = svd(Z)

    print('trace: %0.2f\tlarge values/T: %0.2f, where T=%d, and threshold for large value is %f\t%s' % (np.sum(D), len(S1)/float(T), T, m, f))
