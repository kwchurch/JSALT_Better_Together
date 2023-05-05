#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

import numpy as np
import csrgraph as cg
from scipy import sparse
from scipy.sparse import load_npz, csr_matrix
from sklearn import preprocessing
from sklearn.utils.extmath import randomized_svd
import sys,argparse,time

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
parser.add_argument("-K", "--n_components", type=int, help="hidden dimensions [defaults = 32]", default=32)
# parser.add_argument("-S", '--make_symmetric', action='store_true')
parser.add_argument("-e", '--exponent', type=float, help="defaults to 0.75", default= 0.75)
args = parser.parse_args()

def tsvd_rand(matrix, n_components):
    """
    Sparse randomized tSVD for fast embedding
    """
    l = matrix.shape[0]
    # Is this csc conversion necessary?
    smat = sparse.csc_matrix(matrix)
    U, Sigma, VT = randomized_svd(smat, 
                                  n_components=n_components, 
                                  n_iter=5, random_state=None)

    # added by kwc
    try:
        print('tsvd_rand: %d bytes for U (for %d n_components)' % (U.nbytes, n_components), file=sys.stderr)
    except:
        print('tsvd_rand: diagnostic msg failed', file=sys.stderr)

    U = U * np.sqrt(Sigma)
    U = preprocessing.normalize(U, "l2")
    return U

def pre_factorization(G, n_components, exponent):
    """
    Network Embedding as Sparse Matrix Factorization
    """
    C1 = preprocessing.normalize(G, "l1")
    # Prepare negative samples
    neg = np.array(C1.sum(axis=0))[0] ** exponent
    neg = neg / neg.sum()
    neg = sparse.diags(neg, format="csr")
    neg = G @ neg
    # Set negative elements to 1 -> 0 when log
    C1.data[C1.data <= 0] = 1
    neg.data[neg.data <= 0] = 1
    C1.data = np.log(C1.data)
    neg.data = np.log(neg.data)
    C1 -= neg
    features_matrix = tsvd_rand(C1, n_components=n_components)
    return features_matrix

G = load_npz(args.input_graph)

print('# about to convert to csr_matrix: %0.2f' % (time.time() - t0), file=sys.stderr)
sys.stderr.flush()

# M = csr_matrix(G)

# if args.make_symmetric:
#     print('# enforcing symmetry: %0.2f' % (time.time() - t0), file=sys.stderr)
#     sys.stderr.flush()
#     G += G.T

print('# about to pre_factorize: %0.2f' % (time.time() - t0), file=sys.stderr)
sys.stderr.flush()

U = pre_factorization(G, args.n_components, args.exponent)

print('# about to save: %0.2f' % (time.time() - t0), file=sys.stderr)

np.save(args.output, U)

print('# done: %0.2f' % (time.time() - t0), file=sys.stderr)
