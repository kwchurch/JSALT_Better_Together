#!/usr/bin/env python

import sys,argparse,time
import numpy as np
import scipy
from scipy import linalg
from sklearn import preprocessing
# from sklearn.utils.extmath import randomized_svd

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-K", "--n_componenents", help='K (before), K (after)', required=True)

args = parser.parse_args()

Ks = args.n_componenents.split(',')
print(Ks, file=sys.stderr)

assert len(Ks) > 1, 'confusion'

K_before, K_after = map(int, Ks[0:2])

# print(K_before)
# print(K_after)

def svd_dense(matrix, dimension):
    """
    dense embedding via linalg SVD
    """
    
    t0_svd = time.time()        # added by kwc

    U, s, Vh = linalg.svd(matrix, full_matrices=False, 
                          check_finite=False, 
                          overwrite_a=True)
    U = np.array(U)
    U = U[:, :dimension]
    s = s[:dimension]
    s = np.sqrt(s)
    U = U * s
    U = preprocessing.normalize(U, "l2")

    # added by kwc
    print('%0.0f sec: ProNE svd_dense; U.shape = %s' % (time.time() - t0_svd, str(U.shape)), file=sys.stderr)
    sys.stderr.flush()
    
    return U

# def tsvd_rand(matrix, n_components):
#     """
#     Sparse randomized tSVD for fast embedding
#     """

#     # Is this csc conversion necessary?
#     smat = sparse.csc_matrix(matrix)
#     U, Sigma, VT = randomized_svd(smat, 
#                                   n_components=n_components, 
#                                   n_iter=5, random_state=None)
#     try:
#         print('tsvd_rand: %d bytes for U (for %d n_components)' % (U.nbytes, n_components), file=sys.stderr)
#     except:
#         print('tsvd_rand: diagnostic msg failed', file=sys.stderr)
        
#         U = U * np.sqrt(Sigma)
#         U = preprocessing.normalize(U, "l2")
#         return U

M = np.fromfile(args.input, np.float32).reshape(-1, K_before)

print(str(time.time() - t0) + ' loaded M with shape: ' + str(M.shape), file=sys.stderr)
sys.stderr.flush()

U = svd_dense(M, K_after)

print(str(time.time() - t0) + ' SVD done', file=sys.stderr)
sys.stderr.flush()

U.save(args.output)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
