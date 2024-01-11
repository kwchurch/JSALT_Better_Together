#!/usr/bin/env python

import faiss
import os,sys,argparse,time
import numpy as np
from sklearn.preprocessing import normalize
# from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics.pairwise import euclidean_distances

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
# parser.add_argument("--seed", type=int, help='set seet', default=None)
parser.add_argument("--start", type=int, help='row to start on', default=0)
parser.add_argument("--end", type=int, help='row to end on', default=-1)
parser.add_argument("-i", "--input_directory", help="a directory", required=True)
parser.add_argument("--kmeans", help="output from embeddings_to_kmeans.py", required=True)
parser.add_argument("--brute_force", action='store_true')
parser.add_argument("--topN", type=int, default=1)

args = parser.parse_args()

# print('seed: ' + str(args.seed), file=sys.stderr)

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

kmeans_obj = np.load(args.kmeans)

if args.brute_force:
    for row in range(embedding.shape[0]):
        print(np.argmin(euclidean_distances(normalize(embedding[row,:].reshape(1,-1)), kmeans_obj['centroids'])))
else:
    index = faiss.IndexFlatL2(embedding.shape[1]) 
    index.add(kmeans_obj['centroids'])
    end = embedding.shape[0]
    if args.end >= 0:
        end = args.end
    print('row\tclass\tdistance')
    sys.stdout.flush()
    for row in range(args.start, end):
        q = normalize(embedding[row,:].reshape(1,-1))
        D,I = index.search(q,args.topN)
        # print(str(row) + '\t' + str(I[0][0]) + '\t' + str(D[0][0]))
        print(str(row) + '\t' + '|'.join(map(str, I.reshape(-1))) + '\t' + '|'.join(map(str, D.reshape(-1))))
        sys.stdout.flush()
        # print(str(I.reshape(-1)) + '\t' + str(D.reshape(-1)))

print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)



