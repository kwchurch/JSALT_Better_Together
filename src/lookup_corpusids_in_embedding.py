#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

# from scipy.linalg import orthogonal_procrustes

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
parser.add_argument("--input_directory", help="a directory", required=True)
parser.add_argument("--output", default=None)
parser.add_argument("--compute_trace", help="output args and trace instead of D", action='store_true')
parser.add_argument("--compute_cosines", help="output args, trace and summaries of cosines instead of D", action='store_true')
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
             'embedding' : embedding_from_dir(dir, K),
             'new_ids': []}

def old_to_new(old_id, mm):
    if old_id < 0 or old_id >= len(mm): return -1
    return mm[old_id]

for d in args.input_directory.split(','):
    print('# ' + d)

configs = [directory_to_config(d) for d in args.input_directory.split(',')]
# embedding = config['embedding']

for line in sys.stdin:
    old_id = int(line)
    new_ids = [old_to_new(old_id,config['map']) for config in configs]
    
    if min(new_ids) > 0:
        for new_id,config in zip(new_ids,configs):
            config['new_ids'].append(new_id)
    
if args.compute_trace or args.compute_cosines:
    trace = []
    vars = []
    l = 0
    times = []
    for config in configs:
        t1 = time.time()
        embedding = config['embedding']
        new_ids = np.array(config['new_ids'], dtype=int)
        Z = embedding[new_ids,:]
        U,D,Vt = np.linalg.svd(normalize(Z))
        trace.append(np.sum(D))
        l = len(new_ids)
        if args.compute_cosines:
            sim = cosine_similarity(Z @ Z.T)
            vars.append(np.var(sim))
        t2 = time.time()
        times.append(t2 -t1)
    print('\t'.join(['\t'.join(map(str, trace)),
                     '\t'.join(map(str, vars)),
                     '\t'.join(map(str, times)),
                     str(l)]))
          
# Need to fix this case
# if not args.output is None:
#     np.save(args.output, res)

print('%0.f sec: done' % (time.time() - t0), file=sys.stderr)
