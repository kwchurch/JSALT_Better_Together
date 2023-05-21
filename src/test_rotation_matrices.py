#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

from scipy.linalg import orthogonal_procrustes

t0 = time.time()

# example usage:
# cd /work/k.church/JSALT-2023/semantic_scholar/embeddings/specter.K280
# sbatch -p debug -t 19 /work/k.church/githubs/JSALT_Better_Together/src/create_rotation_matrix.py -i ../specter.K280,../proposed -N 100000 -o rot

# assumes the two input directories contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

# choose N offsets into map
# filter out unavailable values (<= 0)
# get matrix from the two embedding.f files for the rows that pass the filter
# compute the rotation matrix and save it

parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, help='set seet', default=None)
parser.add_argument("-i", "--input_directories", help="two directories, comma separated", required=True)
# parser.add_argument("-o", "--output", required=True)
parser.add_argument("-R", "--rotation_matrices", help="comma separated files in *.npy format", required=True)
parser.add_argument("-N", "--N", type=int, required=True)

args = parser.parse_args()

# print('seed: ' + str(args.seed), file=sys.stderr)

if not args.seed is None:
    np.random.seed(args.seed)

rotation_matrices = [np.load(f) for f in args.rotation_matrices.split(',')]

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return int(fd.read().split('\t')[0])

def map_from_dir(dir):
    fn = dir + '/map.old_to_new.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def embedding_from_dir(dir, K):
    fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : map_from_dir(dir),
             'embedding' : embedding_from_dir(dir, K)}

inputs = args.input_directories.split(',')

# print(inputs, file=sys.stderr)

assert len(inputs) == 2, 'confusion'

configs = [directory_to_config(d) for d in inputs]

map0 = configs[0]['map']
map1 = configs[1]['map']

choices = np.random.choice(min(len(map0), len(map1)), args.N)
# print(choices, file=sys.stderr)

choices0 = map0[choices]
choices1 = map1[choices]

choices2 = sorted(np.array([i for i,choice0,choice1 in zip(choices,choices0,choices1) if choice0 > 0 and choice1 > 0 ]))

# print('choices2: ' + str(choices2))

new_idx0 = map0[choices2]
new_idx1 = map1[choices2]

# print('new_idx0: ' + str(new_idx0))
# print('new_idx1: ' + str(new_idx1))

emb0 = configs[0]['embedding']
emb1 = configs[1]['embedding']

# print('emb0.shape: ' + str(emb0.shape), file=sys.stderr)
# print('emb1.shape: ' + str(emb1.shape), file=sys.stderr)

emb0a = normalize(emb0[new_idx0,:])
emb1a = normalize(emb1[new_idx1,:])

norm0 = np.linalg.norm(emb0a, axis=1)
norm1 = np.linalg.norm(emb1a, axis=1)

# print('norm0: ' + str(norm0), file=sys.stderr)
# print('norm1: ' + str(norm1), file=sys.stderr)

# print('emb0a.shape: ' + str(emb0a.shape), file=sys.stderr)
# print('emb1a.shape: ' + str(emb1a.shape), file=sys.stderr)

def my_cos(X, Y):
    return [ cosine_similarity(X[i,:].reshape(1,-1), Y[i,:].reshape(1,-1))[0,0] for i in range(X.shape[0]) ]

scores = np.array([ my_cos(emb0a @ R,  emb1a) for R in rotation_matrices ])
# scores = np.array([ np.linalg.norm(emb0a @ R - emb1a, axis=1) for R in rotation_matrices ])

# print('scores.shape: ' + str(scores.shape), file=sys.stderr)
# print('scores: ' + str(scores))

np.savetxt(sys.stdout, scores.T, fmt='%0.3f')
