#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np


t0 = time.time()

def print_bytes(M, name):
    print('%0.2f minutes: %s has %0.2f B nonzeros, %0.2f GBytes' % ((time.time() - t0)/60,
                                                                    name,
                                                                    M.count_nonzero()/1e9,
                                                                    (M.indices.nbytes + M.indptr.nbytes + M.data.nbytes)/1e9))
    print(str(M.indices.nbytes) + ' bytes for indices')
    print(str(M.indptr.nbytes) + ' bytes for indptr')
    print(str(M.data.nbytes) + ' bytes for data')

    sys.stdout.flush()

def summarize_fanout(M, name):
    fan0 = np.sum(M, axis=0)
    print('%0.2f minutes: fan0 has %s has %0.2f B sum, max %d' % ((time.time() - t0)/60, name, np.sum(fan0), np.max(fan0)))
    sys.stdout.flush()
    fan1 = np.sum(M, axis=1)
    print('%0.2f minutes: fan1 has %s has %0.2f B sum, max %d' % ((time.time() - t0)/60, name, np.sum(fan1), np.max(fan1)))
    sys.stdout.flush()

big='/work/k.church/semantic_scholar/citations/graphs/freq_rows/C/threshold.100/pieces.100/big_sum.npz'
cocite='/work/k.church/semantic_scholar/citations/graphs/freq_rows/C/threshold.100/pieces.100/cocitations.npz'
Gbig=scipy.sparse.load_npz(big)
print_bytes(Gbig, 'sketch')

summarize_fanout(Gbig, 'sketch')

Gcocite=scipy.sparse.load_npz(cocite)
print_bytes(Gcocite, 'cocitations')

summarize_fanout(Gcocite, 'cocitations')

print('bincounts')
bc = np.bincount(Gcocite.data)
np.savetxt(sys.stdout, bc)
