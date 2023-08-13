#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
import heapq
from sklearn.metrics.pairwise import cosine_similarity

t0 = time.time()

print('brute_force_cosines_kwc.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

apikey=os.environ.get('SPECTER_API_KEY')
parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)
parser.add_argument("--topn", type=int, help="number of results to output", default=100)
parser.add_argument("--input_ids", help="input file", default=None)
parser.add_argument("--input_vectors", help="input file", default=None)
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

# print('config: ', config['map'])
# print('config contents: ', config['map'][0])

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


# if args.verbose:
#     print('ids.shape = ' + str(ids.shape), file=sys.stderr)

result = input_vectors = None

assert not ((args.input_ids is None) == (args.input_vectors is None)), 'please specify one (and only one) of --input_ids and --input_vectors'

if not args.input_ids is None:
    with open(args.input_ids, 'r') as fd:
        input_ids = np.array([int(i) for i in fd.read().split('\n') if len(i) > 0], dtype=int)

        if args.use_references == 'never' or args.use_references == 'when_necessary':
            mapped_ids = np.zeros(len(ids), dtype=int)
            for e,i in enumerate(input_ids):
                if i < maxid:
                    mapped_ids[e] = my_map[i]
            result = emb[mapped_ids,:]
            result[mapped_ids == 0,:] = 0
        elif args.use_references == 'always':
            result = np.array([id_to_centroid(id) for id in ids])
        else:
            assert False, 'bad arg: use_references = ' + str(args.use_references)

if not args.input_vectors is None:
    if args.input_vectors.endswith('.npy'):
        result = np.load(args.input_vectors)
    else:
        result = np.fromfile(args.input_vectors, dtype=np.float32).reshape(-1, config['record_size'])
    assert result.shape[1] == config['record_size'], 'bad shape: result.shape = %s, config[record_size] = %s' % (str(result.shape), str(config[record_size]))

if args.verbose:
    print('result.shape: ' + str(result.shape), file=sys.stderr)

# # instead of saving this output, we want to find the highest K cosine similarities
# def cosine_similarity_vector_matrix(vector, matrix):
#     dot_product = np.dot(matrix, vector)
#     norm_vector = np.linalg.norm(vector)
#     norm_matrix = np.linalg.norm(matrix, axis=1)
#     denominator = norm_vector * norm_matrix
#     denominator[denominator == 0] = 1  
#     similarity = dot_product / denominator
#     return similarity


SMALL=1e-6
result_norms = np.linalg.norm(result, axis=1)
good = result_norms > SMALL
good_indexes = np.arange(len(good))[good]
# good_indexes = config['imap'][good]

print("bincount(good) = " + str(np.bincount(good)), file= sys.stderr)
print("good_indexes = " + str(good_indexes), file= sys.stderr)
sys.stderr.flush()


print("about to compute cosines in %0.2f seconds" % (time.time() - t0), file= sys.stderr)
sys.stderr.flush()

cosines = cosine_similarity(result[good,:], emb)

print("Found cosines %s in %0.2f seconds." % (str(cosines.shape), time.time() - t0), file= sys.stderr)
sys.stderr.flush()
# then we find the K largest cosine values

quantiles = np.quantile(cosines, 1-args.topn/emb.shape[0], axis=1)

print("Found quantiles %s in %0.2f seconds." % (str(quantiles.shape), time.time() - t0), file= sys.stderr)
print(quantiles, file= sys.stderr)

sys.stderr.flush()
idx = np.arange(emb.shape[0])
# idx = config['imap']
imap = config['imap']

# j is a corpus id
# v is a score
# ii is a row from result
for i,q in enumerate(quantiles):
    ii = good_indexes[i]
    s = cosines[i,:] >= q
    for j,v in zip(idx[s], cosines[i,:][s]):
        if j < len(imap):
            print('\t'.join(map(str,[v, imap[j], ii])))

# def find_largest(array, topn):
#     max_heap = []
#     for i, num in enumerate(array):
#         if len(max_heap) < topn:
#             heapq.heappush(max_heap, (num, i))
#         else:
#             if num > max_heap[0][0]:
#                 heapq.heappop(max_heap)
#                 heapq.heappush(max_heap, (num, i))
#     result_indices = []
#     while max_heap:
#         num, i = heapq.heappop(max_heap)
#         result_indices.append(i)
#     result_indices.reverse()  
#     return result_indices

# result_indices = find_largest(cosines, args.topn)

# print("Found %0.2f closest values in %0.2f seconds." % (args.K, time.time() - t0))
# print("Sorted result_values:", result_values) 
# print("Sorted result_indices:", result_indices)
# print("IDs: ", [config['imap'][index] for index in result_indices])
