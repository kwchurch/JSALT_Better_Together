#!/usr/bin/env python

import numpy as np
import csrgraph as cg
from scipy import sparse, special
from scipy.sparse import load_npz, csr_matrix, save_npz
from sklearn import preprocessing
import os, sys, argparse, time, gc, socket

def save_file(mat, suffix, iteration):
    np.save('%s.%s.%d.npy' % (args.temp_file_prefix, suffix, iteration), mat)

def load_file(suffix, iteration):
    return np.load('%s.%s.%d.npy' % (args.temp_file_prefix, suffix, iteration))

@profile
def first_iter(i, temp_file_prefix, theta):
    if (i == 0):
        print(str(time.time() - t0) + ' about to load U: %s' % (str(args.U)), file=sys.stderr)
        sys.stderr.flush() 
        U = np.load(args.U).astype(np.float32)
        N = U.shape[0]
        K = U.shape[1]
        sys.stderr.flush()
        print('%0.2f sec: loaded U with shape: %s' % (time.time() - t0, str(U.shape)), file=sys.stderr)
        t = time.time()
        Lx0 = U
        M = load_m(temp_file_prefix, K, N)
        Lx1 = M @ Lx0
        Lx1 = 0.5 * M @ Lx1 - Lx0
        del M
        conv = special.iv(0, theta) * Lx0
        conv -= 2 * special.iv(1, theta) * Lx1
        print('First iteration computation: ', time.time() - t)
        return Lx0, Lx1, conv

#@profile
def load_m(temp_file_prefix, K, N):
    M = None
    M_filename = '%s.K%d.M.npz' % (temp_file_prefix, K)
    if os.path.exists(M_filename):
        print('%0.2f sec: about to load M' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        try:
            M = load_npz(M_filename)
            return M
        except:
            print(str(time.time() - t0) + ' failed to load M in: %s' % (M_filename), file=sys.stderr)
    else:
        print('%0.2f sec: about to compute M' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        G = load_npz(args.input_graph)
        A = sparse.eye(N) + G
        DA = preprocessing.normalize(A, norm='l1')
        L = sparse.eye(N) - DA
        M = (L - args.mu * sparse.eye(N)).astype(np.float32)
        A = DA = L = None
        ngc = gc.collect()
        print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc), file=sys.stderr)
        print(gc.get_stats(), file=sys.stderr)
        save_npz(M_filename, M)
        print('%0.2f sec: loaded M' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        return M

@profile
def subsequent_iteration(i, temp_file_prefix, theta):
    Lx0 = load_file("Lx0", i - 1)
    N = Lx0.shape[0]
    K = Lx0.shape[1]
    M = load_m(temp_file_prefix, K, N)
    Lx1 = load_file("Lx1", i - 1)
    Lx2 = M @ Lx1
    Lx2 = (M @ Lx2 - 2 * Lx1) - Lx0
    del M
    print('%0.2f sec: about to collect garbage' % (time.time() - t0), file=sys.stderr)
    ngc = gc.collect()
    print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc), file=sys.stderr)
    print(gc.get_stats(), file=sys.stderr)
    conv = load_file("conv", i - 1)
    if i % 2 == 0:
        conv += 2 * special.iv(i, theta) * Lx2
    else:
        conv -= 2 * special.iv(i, theta) * Lx2
    Lx0 = Lx1
    Lx1 = Lx2
    return Lx0, Lx1, conv

@profile
def save_files(Lx0, Lx1, conv):
    Lx0 = Lx0.astype(np.float32)
    Lx1 = Lx1.astype(np.float32)
    conv = conv.astype(np.float32)
    save_file(Lx0, "Lx0", i)
    save_file(Lx1, "Lx1", i)
    save_file(conv, "conv", i)
    print('%0.2f sec: finished iteration %d' % (time.time() - t0, i), file=sys.stderr)

if __name__=="__main__":
    print('ProNE_chebyshev: sys.argv = ' + str(sys.argv), file=sys.stderr)
    t0 = time.time()
    print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (
    socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
    sys.stderr.flush()
    parser = argparse.ArgumentParser()
    parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", required=True)
    parser.add_argument("-U", "--U", help="input prefactorization", default=None)
    parser.add_argument("--temp_file_prefix", help="input prefactorization", default=None)
    parser.add_argument("--iteration", type=int, help="typically a number from 0 to 10", required=True)
    parser.add_argument("--mu", type=float, help="damping factor (defaults to 0.5)", default=0.5)
    parser.add_argument("--theta", type=float, help="bessel function parameter (defaults to 0.5)", default=0.5)
    args = parser.parse_args()
    sys.stderr.flush()
    i = args.iteration
    if(i == 0):
        Lx0, Lx1, conv = first_iter(i, args.temp_file_prefix, args.theta)
        print('%0.2f sec: about to save files' % (time.time() - t0), file=sys.stderr)
        save_files(Lx0, Lx1, conv)
        print('%0.2f sec: finished iteration %d' % (time.time() - t0, i), file=sys.stderr)
    else:
        Lx0, Lx1, conv = subsequent_iteration(i, args.temp_file_prefix, args.theta)
        print('%0.2f sec: about to save files' % (time.time() - t0), file=sys.stderr)
        save_files(Lx0, Lx1, conv)
        print('%0.2f sec: finished iteration %d' % (time.time() - t0, i), file=sys.stderr)
