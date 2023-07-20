#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
import pdb
import heapq


t0 = time.time()

apikey=os.environ.get('SPECTER_API_KEY')
parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)
parser.add_argument("-K", "--K", help="The K closest papers in cosine similarity to our desired paper", default=10)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

Y = idx = None

if not args.graph is None:
    Y = map_int32(args.graph + '.Y.i')

    if not os.path.exists(args.graph + '.X.i.idx'):
        print('%0.0f sec: computing idx' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        X = map_int32(args.graph + '.X.i')
        res = np.cumsum(np.bincount(X))
        res.tofile(args.graph + '.X.i.idx')
        print('%0.0f sec: idx computed' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()

    idx = map_int64(args.graph + '.X.i.idx')

def extract_row(x):
    # print('extract_row: ' + str(x))
    if x >= len(idx) or x < 0:
        return []
    if x == 0:
        return Y[:idx[0]]
    else:
        return Y[idx[x-1]:idx[x]]

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return int(fd.read().split('\t')[0])

def map_from_dir(dir):
    fn = dir + '/map.old_to_new.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def imap_to_dir(dir):
    fn = dir + '/map.new_to_old.i'
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
             'imap': imap_to_dir(dir),
             'embedding' : embedding_from_dir(dir, K)}

t0 = time.time()
config = directory_to_config(args.dir)
print('config: ', config['map'])
print('config contents: ', config['map'][0])
def get_corpusId(ref):
    try:
        return ref['externalIds']['CorpusId']
    except:
        return None

def id_to_references(my_id):
    if not args.graph is None:
        return extract_row(int(my_id))
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/CorpusId:' + str(my_id) + '/?fields=references,references.externalIds'
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if 'references' in j and not j['references'] is None:
        return [ get_corpusId(ref) for ref in j['references']]
    else:
        return []

maxid = config['map'].shape[0]
my_map = config['map'].reshape(-1)
emb = config['embedding']


def centroid(refs):
    mapped_refs = np.array([ my_map[ref] for ref in refs if not ref is None and ref < maxid ], dtype=int)
    mapped_refs = mapped_refs[mapped_refs > 0]
    vectors = emb[mapped_refs,:]
    if args.verbose:
        print('centroid: vectors.shape = ' + str(vectors.shape), file=sys.stderr)
    if len(vectors) > 0:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(emb.shape[1], dtype=int)

def id_to_centroid(id):
    return centroid(id_to_references(id))

ids = np.array([int(i) for i in sys.stdin.read().split('\n') if len(i) > 0], dtype=int)
if args.verbose:
    print('ids.shape = ' + str(ids.shape), file=sys.stderr)
if args.use_references == 'never' or args.use_references == 'when_necessary':
    mapped_ids = np.zeros(len(ids), dtype=int)
    for e,i in enumerate(ids):
        if i < maxid:
            mapped_ids[e] = my_map[i]
    result = emb[mapped_ids,:]
    result[mapped_ids == 0,:] = 0
elif args.use_references == 'always':
    result = np.array([id_to_centroid(id) for id in ids])
else:
    assert False, 'bad arg: use_references = ' + str(args.use_references)

if args.verbose:
    print('result.shape: ' + str(result.shape), file=sys.stderr)


# instead of saving this output, we want to find the highest K cosine similarities
#np.savetxt(sys.stdout, result)
def cosine_similarity_vector_matrix(vector, matrix):
    dot_product = np.dot(matrix, vector)
    norm_vector = np.linalg.norm(vector)
    norm_matrix = np.linalg.norm(matrix, axis=1)

    # Ensure denominator is non-zero to avoid division by zero
    denominator = norm_vector * norm_matrix
    denominator[denominator == 0] = 1  # Set 1 for zero values to avoid division by zero

    similarity = dot_product / denominator

    return similarity

cosines = cosine_similarity_vector_matrix(np.array(result).reshape(-1), emb)
print("Found cosines in %0.2f seconds." % (time.time() - t0))
# then we find the K largest cosine values

def find_k_largest_with_indices(array, K):
    max_heap = []
    for i, num in enumerate(array):
        if len(max_heap) < K:
            heapq.heappush(max_heap, (num, i))
        else:
            if num > max_heap[0][0]:
                heapq.heappop(max_heap)
                heapq.heappush(max_heap, (num, i))
    result_indices = []
    result_values = []
    while max_heap:
        num, i = heapq.heappop(max_heap)
        result_indices.append(i)
        result_values.append(num)

    result_indices.reverse()  
    result_values.reverse()
    return result_values, result_indices

result_values, result_indices = find_k_largest_with_indices(cosines, args.K)
print("Found %0.2f closest values in %0.2f seconds." % (args.K, time.time() - t0))
print("Sorted result_values:", result_values) 
print("Sorted result_indices:", result_indices)
print("IDs: ", [config['imap'][index] for index in result_indices])
