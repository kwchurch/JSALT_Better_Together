#!/usr/bin/env python

import sys,scipy.sparse,time,argparse,socket,os
import numpy as np

print('shrink_matrix_V2.py: sys.argv = ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()


parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("--citations", help=".npy file", default=None)
parser.add_argument("-o", "--output", help="output filename", required=True)
parser.add_argument("-T", "--threshold", type=int, help="threshold on size on number of citations (defaults to 0)", default=0)
# parser.add_argument("-S", "--sample", type=float, help="fraction of edges", default=1.0)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' shrink_matrix_V2: my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
print(str(time.time() - t0) + ' shrink_matrix_V2: finished loading', file=sys.stderr)
sys.stderr.flush()

if args.citations is None:
    citationCounts = np.array(np.sum(M, axis=0))
    # np.save(args.graph + 'citations.axis0.npy', citationCounts)
else:
    citationCounts = np.load(args.citations)

citationCounts = citationCounts.reshape(-1)
print('citationCounts.shape: ' + str(citationCounts.shape), file=sys.stderr)

goodp = (citationCounts > args.threshold)
new_N = np.sum(goodp)
old_N = len(citationCounts)

print(str(time.time() - t0) + ' shrink_matrix_V2: new_N: %d, old_N: %d' % (new_N, old_N), file=sys.stderr)
sys.stderr.flush()


old_idx = np.arange(old_N, dtype=np.int32)
new_to_old = old_idx[goodp]
old_to_new = np.zeros(old_N, dtype=np.int32) - 1

old_to_new[new_to_old] = np.arange(len(new_to_old))

# for i,v in enumerate(new_to_old):
#     old_to_new[v]=i

# Free up this space
old_idx = new_idx = None

old_to_new.astype(np.int32).tofile(args.output + '.old_to_new.i')
new_to_old.astype(np.int32).tofile(args.output + '.new_to_old.i')

# np.savez(args.output, old_to_new=old_to_new, new_to_old=new_to_old)
print(str(time.time() - t0) + ' shrink_matrix_V2: finished relabling', file=sys.stderr)
sys.stderr.flush()

old_X,old_Y = M.nonzero()

print(str(time.time() - t0) + ' shrink_matrix_V2: M.shape: ' + str(M.shape), file=sys.stderr)
print(str(time.time() - t0) + ' shrink_matrix_V2: M.count_nonzero: ' + str(M.count_nonzero()), file=sys.stderr)
sys.stderr.flush()

X = old_X[goodp[old_X]]

print(str(time.time() - t0) + ' shrink_matrix_V2: finished X', file=sys.stderr)
sys.stderr.flush()

Y = old_Y[goodp[old_Y]]

print(str(time.time() - t0) + ' shrink_matrix_V2: finished Y', file=sys.stderr)
sys.stderr.flush()

new_X = old_to_new[X]

print(str(time.time() - t0) + ' shrink_matrix_V2: finished new_X', file=sys.stderr)
sys.stderr.flush()

new_Y = old_to_new[Y]

print(str(time.time() - t0) + ' shrink_matrix_V2: finished new_Y', file=sys.stderr)
sys.stderr.flush()

print(str(time.time() - t0) + ' shrink_matrix_V2: about to start the crux', file=sys.stderr)
sys.stderr.flush()

data = np.ones(len(new_X), dtype=bool)
newM = scipy.sparse.coo_matrix((data, (new_X, new_Y)), dtype=bool, shape=(new_N, new_N))

print(str(time.time() - t0) + ' shrink_matrix_V2: finished the crux', file=sys.stderr)
sys.stderr.flush()

newM2 = scipy.sparse.csr_matrix(newM)

print(str(time.time() - t0) + ' shrink_matrix_V2: about to save', file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(args.output + '.G2', newM2)

print(str(time.time() - t0) + ' shrink_matrix_V2: done', file=sys.stderr)
sys.stderr.flush()
