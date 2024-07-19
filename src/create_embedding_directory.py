#!/usr/bin/env python

import scipy
from scipy import sparse, linalg, special
from sklearn import preprocessing
import numpy as np
from scipy.sparse import load_npz, csr_matrix, save_npz
import os,sys,argparse,time,gc,socket

print('create_embedding_directory.py: sys.argv = ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output directory", required=True)
parser.add_argument("-i", "--input", help="input npy prone file from ProNE_finish, or input npz file from ProNE baseline", required=True)
parser.add_argument("-m", "--map", help="mapping files (from new_shrink_matrix)", default=None)
args = parser.parse_args()

if not os.path.exists(args.output):
    os.mkdir(args.output)

if args.input.endswith('.npz'):
    M = np.load(args.input)['edges'].astype(np.float32)
else:
    M = np.load(args.input).astype(np.float32)

M.tofile(args.output + '/embedding.f')

with open(args.output + '/record_size', 'w') as fd:
    print(M.shape[1], file=fd)
    print(6, file=fd)

with open(args.output + '/record_size.sh', 'w') as fd:
    print('K=' + str(M.shape[1]), file=fd)
    print('B=6', file=fd)

if not args.map is None:
    maps = np.load(args.map)
    for i in ['old_to_new', 'new_to_old']:
        with open(args.output   + '/map.' + i + '.i', 'wb') as fd:
            maps[i].tofile(fd)




