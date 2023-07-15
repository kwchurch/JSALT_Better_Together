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

print('ProNE_finish.py: sys.argv = ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()


parser = argparse.ArgumentParser()
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", required=True)
parser.add_argument("-U", "--U", help="input prefactorization", default=None)
parser.add_argument("--temp_file_prefix", help="input prefactorization", default=None)
parser.add_argument("--iteration", type=int, help="typically a number from 0 to 10", required=True)
# parser.add_argument("--mu", type=float, help="damping factor (defaults to 0.5)", default=0.5)
# parser.add_argument("--theta", type=float, help="bessel function parameter (defaults to 0.5)", default=0.5)
args = parser.parse_args()

def save_file(mat, suffix, iteration):
    np.save('%s.%s.%d.npy' % (args.temp_file_prefix, suffix, iteration), mat)

def load_file(suffix, iteration):
    return np.load('%s.%s.%d.npy' % (args.temp_file_prefix, suffix, iteration))    


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

print(str(time.time() - t0) + ' about to load U: %s' % (str(args.U)), file=sys.stderr)
sys.stderr.flush()

U = np.load(args.U) # .astype(np.float32)
N = U.shape[0]
K = U.shape[1]

print(str(time.time() - t0) + ' about to load G: %s' % (str(args.input_graph)), file=sys.stderr)
sys.stderr.flush()

G = load_npz(args.input_graph)
A = sparse.eye(N) + G

print(str(time.time() - t0) + ' about to load conv, iteration: %s' % (str(args.iteration)), file=sys.stderr)
sys.stderr.flush()


conv = load_file("conv", args.iteration)
mm = A @ (U - conv)

ngc = gc.collect()
print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc), file=sys.stderr)
print(gc.get_stats(), file=sys.stderr)


emb = svd_dense(mm, K)

# changed by kwc to float32
# emb = svd_dense(mm, K).astype(np.float32)

np.save(args.output, emb)

print('%0.2f sec: done' % (time.time() - t0), file=sys.stderr)

# clean up stuff at end
    # added by kwc
    # print('chebyshev_gaussian finishing %0.0f sec' % (time.time() - t0ch), file=sys.stderr)
    # mm = A @ (U - conv)
    # emb = svd_dense(mm, K)
    # return emb

