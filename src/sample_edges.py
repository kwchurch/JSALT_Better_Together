#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-S", "--sample", type=float, help="fraction of edges (float strickly between 0 and 1)", default=0.1)
parser.add_argument("-s", "--seed", type=int, help="random seed", default=None)

args = parser.parse_args()

print(str(time.time() - t0) + ' sample_edges:  seed = ' + str(args.seed), file=sys.stderr)
if not args.seed is None:
    np.random.seed(args.seed)

def my_load(f):
    print(str(time.time() - t0) + ' sample_edges: my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
print(str(time.time() - t0) + ' sample_edges:  finished loading', file=sys.stderr)
sys.stderr.flush()



X,Y = M.nonzero()
E = len(X)
new_E = int(args.sample * E)

print(str(time.time() - t0) + ' sample_edges:  new_E = ' + str(new_E), file=sys.stderr)

selection = np.random.choice(E, new_E)
V = np.ones(new_E, dtype=bool)

new_X = X[selection]
new_Y = Y[selection]

print(str(time.time() - t0) + ' sample_edges: len(X) = %d, len(new_X) = %d' % (len(X), len(new_X)), file=sys.stderr)
print(str(time.time() - t0) + ' sample_edges: len(Y) = %d, len(new_Y) = %d' % (len(Y), len(new_Y)), file=sys.stderr)

new_M = scipy.sparse.csr_matrix((V, (new_X, new_Y)), shape=M.shape, dtype=bool)

print(str(time.time() - t0) + ' sample_edges:  finished computing new_M', file=sys.stderr)
sys.stderr.flush()

scipy.sparse.save_npz(args.output, new_M)

print(str(time.time() - t0) + ' sample_edges:  done', file=sys.stderr)
sys.stderr.flush()
