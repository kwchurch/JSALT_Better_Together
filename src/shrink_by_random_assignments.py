#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np
import random

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
# parser.add_argument("-N", "--population_size", type=int, help="population size", required=True)
parser.add_argument("-n", "--newN", type=int, help="sample size", required=True)
parser.add_argument("-o", "--output", help="output", required=True)

args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
N = M.shape[0]
print(str(time.time() - t0) + ' finished loading', file=sys.stderr)
sys.stderr.flush()

# assignments
A = np.array(random.choices(np.arange(args.newN), k=N), dtype=np.int32)
np.save(args.output + '.assignments', A)

print(str(time.time() - t0) + ' finished assignments', file=sys.stderr)
sys.stderr.flush()

# convert the assignment vector A into a matrix
AA = scipy.sparse.coo_matrix((np.ones(N, dtype=bool), (np.arange(N, dtype=np.int32), A)), dtype=bool, shape=(N, args.newN))
AA = scipy.sparse.csr_matrix(AA)
newM = AA.T @ M @ AA
newM = scipy.sparse.csr_matrix(newM)

# old_X,old_Y = M.nonzero()
# new_X = old_X[A]
# new_Y = old_Y[A]

# data = np.ones(len(new_X), dtype=bool)
# newM = scipy.sparse.coo_matrix((data, (new_X, new_Y)), dtype=bool, shape=M.shape)
# newM2 = scipy.sparse.csr_matrix(newM)[0:args.newN,0:args.newN]

print(str(time.time() - t0) + ' saving', file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(args.output, newM)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
