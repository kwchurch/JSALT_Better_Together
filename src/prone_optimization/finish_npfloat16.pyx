#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

import scipy
from scipy import sparse, linalg, special
from sklearn import preprocessing
import numpy as np
from scipy.sparse import load_npz, csr_matrix, save_npz
import os,sys,argparse,time,gc,socket

def svd_dense(matrix, dimension):
    """
    dense embedding via linalg SVD
    """
    U, s, Vh = linalg.svd(matrix, full_matrices=False, 
                          check_finite=False, 
                          overwrite_a=True)
    U = np.array(U)
    U = U[:, :dimension]
    s = s[:dimension]
    s = np.sqrt(s)
    U = U * s
    U = preprocessing.normalize(U, "l2")
    return U

def finish(G, U, t0, conv, output, iteration):
    N = U.shape[0]
    K = U.shape[1]
    A = sparse.eye(N) + G
    del G
    mm = A @ (U - conv)
    del U
    del conv
    ngc = gc.collect()
    print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc))
    print(gc.get_stats())
    emb = svd_dense(mm, K).astype(np.float16)
    np.save(output, emb)
    print('%0.2f sec: finishcomplete %d' % (time.time() - t0, iteration))
