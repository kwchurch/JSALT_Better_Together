#!/usr/bin/env python

import sys,argparse,time,math
import numpy as np
import scipy
from scipy import linalg,sparse
from sklearn import preprocessing

t0 = time.time()

parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--input", required=True)
# parser.add_argument("-o", "--output", required=True)
parser.add_argument("--seed", type=int, help='set seet', default=None)
parser.add_argument("-K", "--n_componenents", help='K (before), K (after)', required=True)
parser.add_argument("-B", "--block_size", type=int, help='number of rows to read in at a time', default=1000)
args = parser.parse_args()

print('seed: ' + str(args.seed), file=sys.stderr)

if not args.seed is None:
    np.random.seed(args.seed)

Ks = args.n_componenents.split(',')
print('Ks: ' + str(Ks), file=sys.stderr)

assert len(Ks) > 1, 'confusion'

K_before, K_after = map(int, Ks[0:2])

def create_R_matrix(K_before, K_after):
    s = 1/math.sqrt(K_before)
    # n = K_before * K_after * int(np.round(1/s))
    n = 4*int(np.round(1/s))

    print('s: ' + str(s), file=sys.stderr)
    print('n: ' + str(n), file=sys.stderr)

    
    # XY = np.random.choice(K_before * K_after, n * K_after, replace=False) 
    # V = np.concatenate([-np.ones(n//2), np.ones(n//2)])
    # R = np.zeros(K_before * K_after)
    # R[XY] = V
    # R2 = R.reshape(K_before, K_after)

    X = np.random.choice(K_before, n * K_after, replace=True) 
    Y = np.random.choice(K_after, n * K_after, replace=True)
    V = np.concatenate([-np.ones(K_after * n//2), np.ones(K_after * n//2)])
    
    R = np.array(scipy.sparse.csr_matrix((V, (X, Y)), shape=(K_before, K_after)).todense())
    Rnorm = preprocessing.normalize(R, 'l2')
    return Rnorm.astype(np.float32)

R = create_R_matrix(K_before, K_after)

print('R.shape: ' + str(R.shape), file=sys.stderr)
print('R.dtype: ' + str(R.dtype), file=sys.stderr)


# Rnz = R.count_nonzero()
# print('R.count_nonzero: %d (%f%%)' % (Rnz, Rnz/(K_before * K_after)), file=sys.stderr)

R1 = R.reshape(-1)

print('R.mean: ' + str(np.mean(R1)), file=sys.stderr)
print('R.sd: ' + str(np.sqrt(np.var(R1))), file=sys.stderr)
print('R.small (near zero): ' + str(np.sum(np.absolute(R1) < 1e-6)/len(R1)), file=sys.stderr)
print('R.neg: ' + str(np.sum(R1 < -1e-6)/len(R1)), file=sys.stderr)
print('R.pos: ' + str(np.sum(R1 > 1e-6)/len(R1)), file=sys.stderr)

sys.stderr.flush()

while True:
    block = np.fromfile(sys.stdin, dtype=np.float32, count=args.block_size * K_before)
    if len(block) == 0: break
    A = np.array(block).reshape(-1, K_before)
    B = A @ R
    B.tofile(sys.stdout)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
