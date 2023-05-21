#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-C", "--components", help="output file", required=True)
# parser.add_argument("-S", "--sample", type=float, help="fraction of edges", default=1.0)
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' connected_compenents: my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
print(str(time.time() - t0) + ' connected_compenents: finished loading', file=sys.stderr)
sys.stderr.flush()

n,comp = scipy.sparse.csgraph.connected_components(M,directed=False)

print('n: ' + str(n), file=sys.stderr)
print(str(time.time() - t0) + ' connected_compenents: finished computing connected components', file=sys.stderr)
sys.stderr.flush()

np.save(args.components, comp)
print(str(time.time() - t0) + ' connected_compenents: finished saving components', file=sys.stderr)

freq = np.bincount(np.array(comp))
freq2 = np.bincount(freq)
for i,f in enumerate(freq2):
    if f > 0:
        print('freq[%d] = %d' % (i,f), file=sys.stderr)

print(str(time.time() - t0) + ' connected_compenents: done', file=sys.stderr)

