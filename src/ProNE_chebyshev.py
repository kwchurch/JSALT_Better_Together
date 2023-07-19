#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

import numpy as np
import csrgraph as cg
from scipy import sparse,special
from scipy.sparse import load_npz, csr_matrix, save_npz
from sklearn import preprocessing
import os,sys,argparse,time,gc,socket

print('ProNE_chebyshev: sys.argv = ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()


parser = argparse.ArgumentParser()
# parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", required=True)
parser.add_argument("-U", "--U", help="input prefactorization", default=None)
parser.add_argument("--temp_file_prefix", help="input prefactorization", default=None)
parser.add_argument("--iteration", type=int, help="typically a number from 0 to 10", required=True)
# parser.add_argument("--mu", type=float, help="damping factor (defaults to 0.5)", default=0.5)
parser.add_argument("--mu", type=float, help="damping factor (defaults to 0.2)", default=0.2)
parser.add_argument("--theta", type=float, help="bessel function parameter (defaults to 0.5)", default=0.5)
args = parser.parse_args()

def save_file(mat, suffix, iteration):
    if mat.dtype != np.dtype('float32'):
        mat = mat.astype(np.float32)
    np.save('%s.%s.%d.npy' % (args.temp_file_prefix, suffix, iteration), mat)

def load_file(suffix, iteration):
    return np.load('%s.%s.%d.npy' % (args.temp_file_prefix, suffix, iteration))    

print(str(time.time() - t0) + ' about to load U: %s' % (str(args.U)), file=sys.stderr)
sys.stderr.flush()

# U = np.load(args.U).astype(np.float32)
U = np.load(args.U)
N = U.shape[0]
K = U.shape[1]
i = args.iteration

print('%0.2f sec: loaded U with shape: %s and dtype: %s' % (time.time() - t0, str(U.shape), str(U.dtype)), file=sys.stderr)
sys.stderr.flush()

M = None
M_filename = '%s.K%d.M.npz' % (args.temp_file_prefix, K)

# changed by kwc; want to make sure we recompute M on iteration 0
if i > 0:
    assert os.path.exists(M_filename), 'confusion: expected to find: ' + M_filename
    print('%0.2f sec: about to load M' % (time.time() - t0), file=sys.stderr)
    sys.stderr.flush()
    try: 
        M = load_npz(M_filename)
    except:
        print(str(time.time() - t0) + ' failed to load M in: %s' % (M_filename), file=sys.stderr)

if M is None:
    print('%0.2f sec: about to compute M' % (time.time() - t0), file=sys.stderr)
    sys.stderr.flush()
    G = load_npz(args.input_graph)
    A = sparse.eye(N) + G
    DA = preprocessing.normalize(A, norm='l1')

    # L is graph laplacian
    L = sparse.eye(N) - DA
    M = (L - args.mu * sparse.eye(N)) # .astype(np.float32)

    A = DA = L = None
    ngc = gc.collect()
    print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc), file=sys.stderr)
    print(gc.get_stats(), file=sys.stderr)

    save_npz(M_filename, M)    

print('%0.2f sec: loaded M' % (time.time() - t0), file=sys.stderr)
sys.stderr.flush()

if i == 0:
    Lx0 = U
    Lx1 = M @ U
    Lx1 = 0.5 * M @ Lx1 - U
    conv = special.iv(0, args.theta) * Lx0
    conv -= 2 * special.iv(1, args.theta) * Lx1
else:
    Lx0 = load_file("Lx0", i-1)
    Lx1 = load_file("Lx1", i-1)
    
    Lx2 = M @ Lx1
    Lx2 = (M @ Lx2 - 2 * Lx1) - Lx0

    # The equation above creates some garbage that we can recover
    print('%0.2f sec: about to collect garbage' % (time.time() - t0), file=sys.stderr)
    ngc = gc.collect()
    print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc), file=sys.stderr)
    print(gc.get_stats(), file=sys.stderr)

    conv = load_file("conv", i-1)
    # if i % 2 == 0:
    if i % 2 != 0:
        conv += 2 * special.iv(i, args.theta) * Lx2
    else:
        conv -= 2 * special.iv(i, args.theta) * Lx2
            
    Lx0 = Lx1
    Lx1 = Lx2
    del Lx2    # no point deleting this since we are essentially done

print('%0.2f sec: about to save files' % (time.time() - t0), file=sys.stderr)
sys.stderr.flush()

Lx0 = Lx0 # .astype(np.float32)
Lx1 = Lx1 # .astype(np.float32)
conv = conv # .astype(np.float32)

save_file(Lx0, "Lx0", i)
save_file(Lx1, "Lx1", i)
save_file(conv, "conv", i)

print('%0.2f sec: finished iteration %d' % (time.time() - t0, i), file=sys.stderr)

# clean up stuff at end
    # added by kwc
    # print('chebyshev_gaussian finishing %0.0f sec' % (time.time() - t0ch), file=sys.stderr)
    # mm = A @ (U - conv)
    # emb = svd_dense(mm, K)
    # return emb

