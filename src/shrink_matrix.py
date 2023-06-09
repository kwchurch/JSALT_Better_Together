#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-C", "--components", help=".npy file", required=True)
parser.add_argument("-o", "--output", help="output filename", required=True)
parser.add_argument("-T", "--threshold", type=int, help="threshold on size of connected components", default=1)
# parser.add_argument("-S", "--sample", type=float, help="fraction of edges", default=1.0)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' shrink_matrix: my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

CC = np.load(args.components)
freq = np.bincount(CC)
F = freq[CC]
old_N = len(CC)
goodp = (F > args.threshold)
new_N = np.sum(goodp)

print(str(time.time() - t0) + ' shrink_matrix: new_N: ' + str(new_N), file=sys.stderr)
sys.stderr.flush()

old_idx = np.arange(old_N, dtype=np.int32)
# new_idx = np.arange(new_N, dtype=np.int32)
new_to_old = old_idx[F > args.threshold]
old_to_new = np.zeros(old_N, dtype=np.int32)
for i,v in enumerate(new_to_old):
    old_to_new[v]=i

# Free up this space
old_idx = new_idx = None

# old_to_new = np.zeros(len(CC), dtype=np.int32)
# new_to_old = np.zeros(new_N, dtype=np.int32)

# n=0
# for o in range(len(F)):
#     if F[o] > args.threshold:
#         old_to_new[o] = n
#         new_to_old[n] = o
#         n += 1

np.savez(args.output, old_to_new=old_to_new, new_to_old=new_to_old)
print(str(time.time() - t0) + ' shrink_matrix: finished relabling', file=sys.stderr)
sys.stderr.flush()

M = my_load(args.graph)
print(str(time.time() - t0) + ' shrink_matrix: finished loading', file=sys.stderr)
sys.stderr.flush()



# for old_x,old_y in M.nonzero():
#     if CC[old_x] > 1 and CC[old_y] > 1:
#         new_x = old_to_new[old_x]
#         new_y = old_to_new[old_y]
#         newM[new_x,new_y]=True

old_X,old_Y = M.nonzero()

print(str(time.time() - t0) + ' shrink_matrix: M.shape: ' + str(M.shape), file=sys.stderr)
print(str(time.time() - t0) + ' shrink_matrix: M.count_nonzero: ' + str(M.count_nonzero()), file=sys.stderr)
sys.stderr.flush()

X = old_X[goodp[old_X]]

print(str(time.time() - t0) + ' shrink_matrix: finished X', file=sys.stderr)
sys.stderr.flush()

Y = old_Y[goodp[old_Y]]

print(str(time.time() - t0) + ' shrink_matrix: finished Y', file=sys.stderr)
sys.stderr.flush()

new_X = old_to_new[X]

print(str(time.time() - t0) + ' shrink_matrix: finished new_X', file=sys.stderr)
sys.stderr.flush()

new_Y = old_to_new[Y]

print(str(time.time() - t0) + ' shrink_matrix: finished new_Y', file=sys.stderr)
sys.stderr.flush()

# This is just wrong
# assert len(new_X) == new_N, 'len(new_X) is %d, but new_N is %d' % (len(new_X), new_N)
# assert len(new_Y) == new_N, 'len(new_Y) is %d, but new_N is %d' % (len(new_Y), new_N)

print(str(time.time() - t0) + ' shrink_matrix: about to start the crux', file=sys.stderr)
sys.stderr.flush()

# newM = scipy.sparse.dok_matrix((new_N, new_N), dtype=bool)
# for x,y in zip(new_X,new_Y):
#     newM[x,y]=True

data = np.ones(len(new_X), dtype=bool)
newM = scipy.sparse.coo_matrix((data, (new_X, new_Y)), dtype=bool, shape=(new_N, new_N))

print(str(time.time() - t0) + ' shrink_matrix: finished the crux', file=sys.stderr)
sys.stderr.flush()

newM2 = scipy.sparse.csr_matrix(newM)

print(str(time.time() - t0) + ' shrink_matrix: about to save', file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(args.output + '.G2', newM2)

print(str(time.time() - t0) + ' shrink_matrix: done', file=sys.stderr)
sys.stderr.flush()
