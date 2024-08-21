#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

import scipy
from scipy import sparse, linalg, special
from sklearn import preprocessing
import numpy as np
from scipy.sparse import load_npz, csr_matrix, save_npz
import os,sys,argparse,time,gc,socket

print('ProNE_finish.py: sys.argv = ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()

#G=/work/k.church/semantic_scholar/releases/2023-05-09/database/citations/graphs/citations.G.npz

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", required=True)
parser.add_argument("--seed", type=int, help="for repeatability; do not touch", default=0)
parser.add_argument("--bin", type=int, help="a number between 0 and 99", required=True)
parser.add_argument("--nbins", type=int, help="a number between 0 and 99", default=100)
args = parser.parse_args()

def map_ints(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def my_load(f):
    print(str(time.time() - t0) + ' shrink_matrix: my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    X = map_ints(f + '.X.i')
    Y = map_ints(f + '.Y.i')
    return X,Y

X,Y = my_load(args.input_graph)
print(str(time.time() - t0) + ' random_bin_assignment: finished loading', file=sys.stderr)
sys.stderr.flush()

np.random.seed(args.seed)
bins = np.random.randint(0, args.nbins, 1+np.max(X))
print('bincount(bins): ' + str(np.bincount(bins)), file=sys.stderr)
sys.stderr.flush()

S = ((bins[X] <= args.bin).astype(np.int8) + (bins[Y] <= args.bin).astype(np.int8))

print('S: ' + str(np.bincount(S)), file=sys.stderr)
sys.stderr.flush()

XX = X[S > 1].astype(np.int32)
YY = Y[S > 1].astype(np.int32)

XX.tofile(args.output + '.X.i')
YY.tofile(args.output + '.Y.i')
