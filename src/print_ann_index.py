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
parser.add_argument("-i", "--input_directory", help="a directory (with embedding, record_size.yaml", required=True)
parser.add_argument("-o", "--output", help="output file", default=None)
parser.add_argument("-X", "--idx", help="an index", required=True)
parser.add_argument("-f", "--features", help="npy array of features", default=None)
parser.add_argument("-T", "--threshold", type=float, help="do not output cosines below this score", default=None)
args = parser.parse_args()

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

ind = args.input_directory

if slurm is None:
    idx = args.idx
    outf = args.output
else:
    idx = args.idx % int(slurm)
    outf = args.output % int(slurm)
    # print('inf: ' + str(inf), file=sys.stderr)

if outf is None:
    outf = sys.stdout
else:
    outf = open(outf, 'w')

SMALL=1e-9

def my_cos(a, b):
    la = np.linalg.norm(a)
    lb = np.linalg.norm(b)
    if la < SMALL or lb < SMALL: return -1.0
    return a.dot(b)/(la*lb)

def record_size_from_dir():
    with open(ind + '/record_size.yaml', 'r') as fd:
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
    fn = ind + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def directory_to_config():
    return { 'record_size' : record_size_from_dir(),
             'dir' : dir,
             'map_new_to_old' : map_int32(ind + '/map.new_to_old.i'),
             'map_old_to_new' : map_int32(ind + '/map.old_to_new.i'),
             'embedding' : embedding_from_dir(),
             'idx' : map_int(idx),
         }

config = directory_to_config()

idx=config['idx']
emb = config['embedding']
new_to_old = config['map_new_to_old']

if not args.features is None:
    features = np.load(args.features)

for i,v in enumerate(idx):
    if i == 0: continue;
    score = my_cos(emb[idx[i-1],:], emb[v,:])
    if not args.threshold is None and score < args.threshold:
        continue
    old_prev = new_to_old[idx[i-1]]
    old_i = new_to_old[v]
    if args.features is None:
        print('%0.3f\t%d\t%d' % (score, old_prev, old_i), file=outf)
    else:
        fprev=f=-1
        if old_prev < len(features): fprev = features[old_prev]
        if old_i < len(features): f = features[old_i]
        print('%0.3f\t%d\t%d\t%d\t%d' % (score, old_prev, old_i, fprev, f), file=outf)

