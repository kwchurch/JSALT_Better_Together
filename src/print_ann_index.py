#!/usr/bin/env python

import os,sys,argparse,time,yaml
import numpy as np
from sklearn.preprocessing import normalize

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
parser.add_argument("-i", "--input_directory", help="a directory (with embedding, record_size.yaml", required=True)
parser.add_argument("-X", "--idx", help="an index", required=True)
args = parser.parse_args()

if not args.seed is None:
    np.random.seed(args.seed)

def my_cos(a, b):
    la = np.linalg.norm(a)
    lb = np.linalg.norm(b)
    return a.dot(b)/(la*lb)

def record_size_from_dir():
    with open(args.input_directory + '/record_size.yaml', 'r') as fd:
        return yaml.safe_load(fd)['K']

# def load_idx():
#     fn = args.idx
#     fn_len = os.path.getsize(fn)
#     return np.memmap(fn, dtype=int, shape=(int(fn_len/8), K), mode='r')    

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def map_int(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=int, shape=(int(fn_len/8)), mode='r')

def map_float32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/8)), mode='r')

def embedding_from_dir():
    K = record_size_from_dir()
    fn = args.input_directory + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def directory_to_config():
    return { 'record_size' : record_size_from_dir(),
             'dir' : dir,
             'map_new_to_old' : map_int32(args.input_directory + '/map.new_to_old.i'),
             'map_old_to_new' : map_int32(args.input_directory + '/map.old_to_new.i'),
             'embedding' : embedding_from_dir(),
             'idx' : map_int(args.idx),
         }

config = directory_to_config()

idx=config['idx']
emb = config['embedding']
new_to_old = config['map_new_to_old']

for i,v in enumerate(idx):
    if i == 0: continue;
    score = my_cos(emb[idx[i-1],:], emb[v,:])
    old_prev = new_to_old[idx[i-1]]
    old_i = new_to_old[v]
    print('%0.3f\t%d\t%d' % (score, old_prev, old_i))
