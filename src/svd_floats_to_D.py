#!/usr/bin/env python

import sys,argparse,time
import numpy as np
import scipy
from scipy import linalg
from sklearn import preprocessing
# from sklearn.utils.extmath import randomized_svd

print('svd_floats_to_D.py: ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-K", "--K", type=int, help='number of hidden dimensions', default=-1)

args = parser.parse_args()


if args.input.endswith('.npy'):
    M = np.load(args.input)
else:
    assert K > 0, 'Need to specify K (hidden dimensions)'
    M = np.fromfile(args.input, np.float32).reshape(-1, args.K)

print(str(time.time() - t0) + ' loaded M with shape: ' + str(M.shape), file=sys.stderr)
sys.stderr.flush()

U, D, Vh = linalg.svd(M, full_matrices=False, check_finite=False, overwrite_a=True)

print(str(time.time() - t0) + ' SVD done', file=sys.stderr)
sys.stderr.flush()

np.savetxt(sys.stdout, D)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
