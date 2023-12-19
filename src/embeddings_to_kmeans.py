#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.cluster import MiniBatchKMeans

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
parser.add_argument("--seed", type=int, help='set seet', default=None)
parser.add_argument("-i", "--input_directory", help="a directory", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-K", "--K", type=int, help="number of kmeans", default=1000)
parser.add_argument("--sample", type=int, help="number of rows to sample from embedding", required=True)
parser.add_argument("--select_randomly", action='store_true')

args = parser.parse_args()

print('seed: ' + str(args.seed), file=sys.stderr)

if not args.seed is None:
    np.random.seed(args.seed)

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

config = directory_to_config(args.input_directory)
embedding = config['embedding']
s = np.random.choice(embedding.shape[0], args.sample, replace=False)
s.sort()
sampled_embedding = normalize(embedding[s,:])

if args.select_randomly:
    np.savez(args.output, centroids=sampled_embedding)
else:
    kmeans = MiniBatchKMeans(n_clusters=args.K, random_state = args.seed).fit(sampled_embedding)
    print('%0.f sec: finished clustering' % (time.time() -t0), file=sys.stderr)
    np.savez(args.output, labels=kmeans.labels_, centroids=kmeans.cluster_centers_)

print('%0.f sec: done' % (time.time() - t0), file=sys.stderr)
