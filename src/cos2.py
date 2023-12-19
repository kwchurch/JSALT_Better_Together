#!/usr/bin/env python

import os,sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

assert len(sys.argv) == 3, 'expected 2 args'

SMALL = 1e-9

def my_cos(v0, v1):
    n0 = np.linalg.norm(v0)
    n1 = np.linalg.norm(v1)
    if n0 < SMALL or n1 < SMALL:
        return -2
    else:
        return v0.dot(v1)/(n0 * n1)

    # return cosine_similarity(v0.reshape(1,-1), v1.reshape(1,-1))[0,0]

vecs = [np.load(fn) for fn in sys.argv[1:]]

assert len(vecs[0]) == len(vecs[1]), 'lengths do not match: %d != %d' % (len(vecs[0]), len(vecs[1]))

res = np.array([ my_cos(vecs[0][i,:], vecs[1][i,:]) for i in range(len(vecs[0]))])

np.savetxt(sys.stdout, res)
