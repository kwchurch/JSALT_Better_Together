#!/usr/bin/env python

import sys,argparse,time
import numpy as np
import scipy
# from scipy import linalg
from jax.numpy import linalg
from sklearn import preprocessing
from sklearn.preprocessing import normalize
# from sklearn.utils.extmath import randomized_svd

print('svd_floats_to_D.py: ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", default=None)
# parser.add_argument("--singular_values", type=int, default=None)
parser.add_argument("-K", "--K", type=int, help='number of hidden dimensions', default=-1)
parser.add_argument("--normalize", help="normalize embeddings before apply SVD", action='store_true')
args = parser.parse_args()


if args.input.endswith('.npy'):
    M = np.load(args.input)
else:
    assert args.K > 0, 'Need to specify K (hidden dimensions)'
    M = np.fromfile(args.input, dtype=np.float32).reshape(-1, args.K)

print(str(time.time() - t0) + ' loaded M with shape: ' + str(M.shape), file=sys.stderr)
print(str(time.time() - t0) + ' loaded M with dtype: ' + str(M.dtype), file=sys.stderr)
sys.stderr.flush()

if args.normalize:
    M = normalize(M)
    print(str(time.time() - t0) + ' normalized', file=sys.stderr)

# U, D, Vh = linalg.svd(M, full_matrices=False, check_finite=False, overwrite_a=True)

U, D, Vh = linalg.svd(M, full_matrices=False, compute_uv = not(args.output is None))

print(str(time.time() - t0) + ' SVD done', file=sys.stderr)
sys.stderr.flush()

np.savetxt(sys.stdout, D)
sys.stdout.flush()

if not args.output is None:
    np.savez(args.output, U=U, D=D)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
