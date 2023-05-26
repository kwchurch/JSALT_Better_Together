#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("--citations", help=".npy file", required=True)
parser.add_argument("-o", "--output", help="output filename", required=True)
parser.add_argument("-T", "--threshold", type=int, help="threshold on size on number of citations (defaults to 0)", default=0)
# parser.add_argument("-S", "--sample", type=float, help="fraction of edges", default=1.0)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' shrink_matrix: my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

citationCounts = np.load(args.citations).reshape(-1)
goodp = (citationCounts > args.threshold)
new_N = np.sum(goodp)
old_N = len(citationCounts)

print(str(time.time() - t0) + ' new_shrink_matrix: new_N: %d, old_N: %d' % (new_N, old_N), file=sys.stderr)
sys.stderr.flush()


old_idx = np.arange(old_N, dtype=np.int32)
new_to_old = old_idx[goodp]
old_to_new = np.zeros(old_N, dtype=np.int32)
for i,v in enumerate(new_to_old):
    old_to_new[v]=i

# Free up this space
old_idx = new_idx = None

np.savez(args.output, old_to_new=old_to_new, new_to_old=new_to_old)
print(str(time.time() - t0) + ' new_shrink_matrix: finished relabling', file=sys.stderr)
sys.stderr.flush()

M = my_load(args.graph)
print(str(time.time() - t0) + ' new_shrink_matrix: finished loading', file=sys.stderr)
sys.stderr.flush()

old_X,old_Y = M.nonzero()

print(str(time.time() - t0) + ' new_shrink_matrix: M.shape: ' + str(M.shape), file=sys.stderr)
print(str(time.time() - t0) + ' new_shrink_matrix: M.count_nonzero: ' + str(M.count_nonzero()), file=sys.stderr)
sys.stderr.flush()

X = old_X[goodp[old_X]]

print(str(time.time() - t0) + ' new_shrink_matrix: finished X', file=sys.stderr)
sys.stderr.flush()

Y = old_Y[goodp[old_Y]]

print(str(time.time() - t0) + ' new_shrink_matrix: finished Y', file=sys.stderr)
sys.stderr.flush()

new_X = old_to_new[X]

print(str(time.time() - t0) + ' new_shrink_matrix: finished new_X', file=sys.stderr)
sys.stderr.flush()

new_Y = old_to_new[Y]

print(str(time.time() - t0) + ' new_shrink_matrix: finished new_Y', file=sys.stderr)
sys.stderr.flush()

print(str(time.time() - t0) + ' new_shrink_matrix: about to start the crux', file=sys.stderr)
sys.stderr.flush()

data = np.ones(len(new_X), dtype=bool)
newM = scipy.sparse.coo_matrix((data, (new_X, new_Y)), dtype=bool, shape=(new_N, new_N))

print(str(time.time() - t0) + ' new_shrink_matrix: finished the crux', file=sys.stderr)
sys.stderr.flush()

newM2 = scipy.sparse.csr_matrix(newM)

print(str(time.time() - t0) + ' new_shrink_matrix: about to save', file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(args.output + '.G2', newM2)

print(str(time.time() - t0) + ' new_shrink_matrix: done', file=sys.stderr)
sys.stderr.flush()
