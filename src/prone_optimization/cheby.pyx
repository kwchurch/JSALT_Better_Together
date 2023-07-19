#!/usr/bin/env python

import numpy as np
import csrgraph as cg
from scipy import sparse, special
from scipy.sparse import load_npz, csr_matrix, save_npz
from sklearn import preprocessing
import os, sys, argparse, time, gc, socket

def save_file(mat, suffix, iteration, temp_file_prefix):
    np.save('%s.%s.%d.npy' % (temp_file_prefix, suffix, iteration), mat)

def load_file(suffix, iteration, temp_file_prefix):
    return np.load('%s.%s.%d.npy' % (temp_file_prefix, suffix, iteration))

#@profile
def first_iter(i, temp_file_prefix, theta, t0, U, input_graph, mu):
    if (i == 0):
        print(str(time.time() - t0) + ' about to load U: %s' % (str(U)))
        sys.stderr.flush() 
        U = np.load(U).astype(np.float32)
        N = U.shape[0]
        K = U.shape[1]
        sys.stderr.flush()
        print('%0.2f sec: loaded U with shape: %s' % (time.time() - t0, str(U.shape)))
        t = time.time()
        Lx0 = U
        M, G = load_m(temp_file_prefix, K, N, t0, input_graph, mu)
        Lx1 = M @ Lx0
        Lx1 = 0.5 * M @ Lx1 - Lx0
        del M
        conv = special.iv(0, theta) * Lx0
        conv -= 2 * special.iv(1, theta) * Lx1
        print('First iteration computation: ', time.time() - t)
        return Lx0, Lx1, conv, U, G

#@profile
def load_m(temp_file_prefix, K, N, t0, input_graph, mu):
    G = load_npz(input_graph)
    M = None
    M_filename = '%s.K%d.M.npz' % (temp_file_prefix, K)
    if os.path.exists(M_filename):
        print('%0.2f sec: about to load M' % (time.time() - t0))
        sys.stderr.flush()
        try:
            M = load_npz(M_filename)
            return M, G
        except:
            print(str(time.time() - t0) + ' failed to load M in: %s' % (M_filename))
    else:
        print('%0.2f sec: about to compute M' % (time.time() - t0))
        sys.stderr.flush()
        #G = load_npz(input_graph)
        A = sparse.eye(N) + G
        DA = preprocessing.normalize(A, norm='l1')
        L = sparse.eye(N) - DA
        M = (L - mu * sparse.eye(N)).astype(np.float32)
        A = DA = L = None
                
        ngc = gc.collect()
        print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc))
        print(gc.get_stats())
        save_npz(M_filename, M)
        print('%0.2f sec: loaded M' % (time.time() - t0))
        sys.stderr.flush()
        return M, G

#@profile
def subsequent_iteration(i, temp_file_prefix, theta, t0, input_graph, mu):
    Lx0 = load_file("Lx0", i - 1)
    N = Lx0.shape[0]
    K = Lx0.shape[1]
    M, G = load_m(temp_file_prefix, K, N, input_graph, mu)
    Lx1 = load_file("Lx1", i - 1)
    Lx2 = M @ Lx1
    Lx2 = (M @ Lx2 - 2 * Lx1) - Lx0
    del M
    print('%0.2f sec: about to collect garbage' % (time.time() - t0))
    ngc = gc.collect()
    print('%0.2f sec: garbage collect returned %d' % (time.time() - t0, ngc))
    print(gc.get_stats())
    conv = load_file("conv", i - 1)
    if i % 2 != 0:
        conv += 2 * special.iv(i, theta) * Lx2
    else:
        conv -= 2 * special.iv(i, theta) * Lx2
    Lx0 = Lx1
    Lx1 = Lx2
    del Lx2
    return Lx0, Lx1, conv, G

#@profile
def save_files(i, Lx0, Lx1, conv, t0, temp_file_prefix):
    Lx0 = Lx0.astype(np.float32)
    Lx1 = Lx1.astype(np.float32)
    conv = conv.astype(np.float32)
    save_file(Lx0, "Lx0", i, temp_file_prefix)
    save_file(Lx1, "Lx1", i, temp_file_prefix)
    save_file(conv, "conv", i, temp_file_prefix)
    print('%0.2f sec: finished iteration %d' % (time.time() - t0, i))