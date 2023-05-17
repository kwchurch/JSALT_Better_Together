#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np

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
parser.add_argument("-i", "--input_directories", help="two directories, comma separated", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-N", "--N", type=int, required=True)

args = parser.parse_args()

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

choices2 = np.array([i for i,choice0,choice1 in zip(choices,choices0,choices1) if choice0 > 0 and choice1 > 0 ])

# print('choices2: ' + str(choices2))

new_idx0 = map0[choices2]
new_idx1 = map1[choices2]

# print('new_idx0: ' + str(new_idx0))
# print('new_idx1: ' + str(new_idx1))

emb0 = configs[0]['embedding']
emb1 = configs[1]['embedding']

print('emb0.shape: ' + str(emb0.shape))
print('emb1.shape: ' + str(emb1.shape))

emb0a = np.copy(emb0[new_idx0,:])
emb1a = np.copy(emb1[new_idx1,:])

print('emb0a.shape: ' + str(emb0a.shape))
print('emb1a.shape: ' + str(emb1a.shape))

print('%0.f sec: about to call orthogonal procrustes' % (time.time() - t0))

R,scale = orthogonal_procrustes(emb0a, emb1a)

np.save(args.output, R)

print('%0.f sec: done' % (time.time() - t0))
