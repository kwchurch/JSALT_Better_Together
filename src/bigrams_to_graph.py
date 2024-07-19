#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-B", "--bigrams", help="filename of bigrams", required=True)
parser.add_argument("-o", "--output", help="npz file", required=True)
# parser.add_argument("-N", "--nodes", type=int, help="number of nodes; defaults to 300000000", default=300000000)
# parser.add_argument("-t", "--scipy_type", help="bsr|coo|csc|csr|dia [defaults to coo]; not supported: dok|lil", default="coo")
# parser.add_argument("-T", '--transpose', action='store_true')
args = parser.parse_args()

# scipy_types = { 'bsr' : scipy.sparse.bsr_matrix,
# 'coo': scipy.sparse.coo_matrix,
# 'csc': scipy.sparse.csr_matrix,
# 'csr': scipy.sparse.csr_matrix,
# 'dia': scipy.sparse.dia_matrix,
# # 'dok': scipy.sparse.dok_matrix,
# # 'lil': scipy.sparse.lil_matrix
# }

# assert args.scipy_type in scipy_types, 'bigrams_to_npz, bad type: ' + str(args.scipy_type)

with open(args.bigrams, 'rb') as fd:
    bigrams = fd.read()
    
print(str(time.time() - t0) + ' finished reading bigrams', file=sys.stderr)
sys.stderr.flush()

floats = np.frombuffer(bigrams, dtype=np.float32)
ints = np.frombuffer(bigrams, dtype=np.int32)

idx = np.arange(0,len(floats),3)

# vals = floats[idx]
X = ints[idx+1]
Y = ints[idx+2]

X.tofile(args.output + '.X.i')
Y.tofile(args.output + '.Y.i')

# f=scipy_types[args.scipy_type]
# if args.transpose:
#     M = f((vals, (Y, X)), dtype=np.float32, shape=(args.nodes, args.nodes))
# else:
#     M = f((vals, (X, Y)), dtype=np.float32, shape=(args.nodes, args.nodes))

# scipy.sparse.save_npz(args.output, M)

print(str(time.time() - t0) + ' done', file=sys.stderr)

