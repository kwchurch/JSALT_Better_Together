#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
from sklearn.cluster import KMeans

# import pdb

t0 = time.time()

print('pairs_to_cos: ' + str(sys.argv), file=sys.stderr)

apikey=os.environ.get('SPECTER_API_KEY')

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
# parser.add_argument('--binary_output', default=None)
# parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
# parser.add_argument("--directory_to_find_references", help="use Semantic Scholar API if None", default=None)
parser.add_argument("-A", "--author_to_papers", help="file (without .X.i and .Y.i)", required=True)
parser.add_argument("-O", "--output", help="output goes to .json file", required=True)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

# Y = my_idx = None
X = map_int64(args.author_to_papers + '.X.i')
Y = map_int64(args.author_to_papers + '.Y.i')


# kmeans = KMeans(n_clusters=np.int32(np.round(np.sqrt(X.shape[0])))).fit(X)

# This doesn't work with authorids, because they are too sparse
# if not args.author_to_papers is None:
#     Y = map_int64(args.author_to_papers + '.Y.i')

#     if not os.path.exists(args.author_to_papers + '.X.i.idx'):
#         print('%0.0f sec: computing idx' % (time.time() - t0), file=sys.stderr)
#         sys.stderr.flush()
#         X = map_int64(args.author_to_papers + '.X.i')
#         res = np.cumsum(np.bincount(X))
#         res.tofile(args.author_to_papers + '.X.i.idx')
#         print('%0.0f sec: idx computed' % (time.time() - t0), file=sys.stderr)
#         sys.stderr.flush()

#     my_idx = map_int64(args.author_to_papers + '.X.i.idx')

def extract_row(x):
    left = np.searchsorted(X, x, side='left')
    right = np.searchsorted(X, x, side='right')
    return Y[left:right]

    # print('extract_row: ' + str(x))
    # if x >= len(my_idx) or x < 0:
    #     return []
    # if x == 0:
    #     return Y[:my_idx[0]]
    # else:
    #     return Y[my_idx[x-1]:my_idx[x]]

def my_int(s):
    for i,c in enumerate(s):
        if not c.isdigit():
            return int(s[0:i])

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return my_int(fd.read())

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

config = directory_to_config(args.dir)

def get_corpusId(ref):
    try:
        return ref['externalIds']['CorpusId']
    except:
        return None

# def a2papers(my_id):

#     if not args.author_to_papers is None:
#         return extract_row(int(my_id))

#     cmd = 'https://api.semanticscholar.org/graph/v1/paper/CorpusId:' + str(my_id) + '/?fields=references,references.externalIds'
#     j = requests.get(cmd, headers={"x-api-key": apikey}).json()
#     if 'references' in j and not j['references'] is None:
#         return [ get_corpusId(ref) for ref in j['references']]
#     else:
#         return []

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
    return centroid(extract_row(id))

# query=3051291
# ref = id_to_references(str(query))
# pdb.set_trace()

# ids = np.loadtxt(sys.stdin).astype(int)
# ids = np.array([int(i) for i in sys.stdin.read().split('\n') if len(i) > 0], dtype=int)

# if args.verbose:
#     print('ids.shape = ' + str(ids.shape), file=sys.stderr)

# if args.use_references == 'never' or args.use_references == 'when_necessary':
#     mapped_ids = np.zeros(len(ids), dtype=int)
#     for e,i in enumerate(ids):
#         if i < maxid:
#             mapped_ids[e] = my_map[i]

#     result = emb[mapped_ids,:]
#     result[mapped_ids == 0,:] = 0
# elif args.use_references == 'always':
#     result = np.array([id_to_centroid(id) for id in ids])
# else:
#     assert False, 'bad arg: use_references = ' + str(args.use_references)

# if args.use_references == 'when_necessary':
#     for e,i in enumerate(ids):
#         if mapped_ids[e] == 0:
#             result[e,:] = id_to_centroid(i)

# if args.verbose:
#     print('result.shape: ' + str(result.shape), file=sys.stderr)

# if not args.binary_output is None:
#     np.save(args.binary_output, result)
# else:
#     np.savetxt(sys.stdout, result)

output_files = { 'authorids' : open(args.output + '.authorids.i', 'wb'),
                 'centroids' : open(args.output + '.centroids.f', 'wb'),
                 }

def cluster_author(authorid):

    # print('authorid: ' + str(authorid), file=sys.stderr)
    refs = extract_row(authorid)
    # print('len(refs): ' + str(len(refs)), file=sys.stderr)

    if len(refs) <= 0: return
    refs = refs[refs < maxid]
    if len(refs) <= 0: return

    mapped_refs = my_map[refs]
    X = emb[mapped_refs,:]

    n = int(np.round(len(refs)/10))
    if n <= 0: n = 1

    kmeans = KMeans(n_clusters=n, n_init='auto').fit(X)
    nn = kmeans.cluster_centers_.shape[0]

    (np.zeros(nn, dtype=int) + authorid).tofile(output_files['authorids'])
    # np.array(n).tofile(output_files['nclusters'])
    kmeans.cluster_centers_.astype(np.float32).tofile(output_files['centroids'])
    
    # j = {'authorid': authorid,
    #      'centroids': kmeans.cluster_centers_ }
    # print(json.dumps(j), file=sys.stdout)

for line in sys.stdin:
    rline = line.rstrip()
    if len(rline) > 0:
        authorid = int(rline)
        cluster_author(authorid)

