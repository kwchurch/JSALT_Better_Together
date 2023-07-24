#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
parser.add_argument('--binary_output', action='store_true')
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
# parser.add_argument("--directory_to_find_references", help="use Semantic Scholar API if None", default=None)
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)
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

# print('maxid: ' + str(maxid), file=sys.stderr)


def centroid(refs):
    mapped_refs = np.array([ my_map[ref] for ref in refs if not ref is None and ref < maxid ], dtype=int)
    # print('mapped_refs (raw): ' + str(mapped_refs), file=sys.stderr)
    mapped_refs = mapped_refs[mapped_refs > 0]
    # print('mapped_refs (filtered): ' + str(mapped_refs), file=sys.stderr)
    vectors = emb[mapped_refs,:]
    # print('centroid: vectors.shape = ' + str(vectors.shape), file=sys.stderr)

    if len(vectors) > 0:
       m = np.mean(vectors, axis=0)
       # print('m.shape: ' + str(m.shape),  file=sys.stderr)
       return m
    else:
        return None # np.zeros(emb.shape[1], dtype=int)

def id_to_centroid(id):
    refs = id_to_references(id)
    if len(refs) > 0:
        # print('id_to_centroid: id = %s, refs = %s' % (str(id), str(refs)), file=sys.stderr)
        sys.stderr.flush()
    return centroid(refs)

# if args.use_references == 'never' or args.use_references == 'when_necessary':
#     mapped_ids = np.zeros(len(ids), dtype=int)
#     for e,i in enumerate(ids):
#         if i < maxid:
#             mapped_ids[e] = my_map[i]

def get_vec(id, use_references):
    new_id = None
    if use_references == 'never':
        if id >= maxid: return None
        new_id = my_map[id]
        if new_id <= 0: return None
        return emb[new_id,:]
    elif use_references == 'always':
        return id_to_centroid(id)
    elif use_references == 'when_necessary':
        vec = get_vec(id, 'never')
        if not vec is None:
            return vec
        else: return get_vec(id, 'always')
    else:
        assert False, 'use_references should not be: ' + use_references

# query=3051291
# ref = id_to_references(str(query))
# pdb.set_trace()

# ids = np.loadtxt(sys.stdin).astype(int)
for line in sys.stdin:
    rline = line.rstrip()
    fields = rline.split()
    if len(fields) < 2: continue
    id1,id2 = fields[0:2]
    vec1 = get_vec(int(id1), args.use_references)
    if vec1 is None:
        print('-1\t' + rline)
        continue
    vec2 = get_vec(int(id2), args.use_references)
    if vec2 is None:
        print('-1\t' + rline)
        continue

    if args.verbose:
        print('id1: ' + str(id1), file=sys.stderr)
        print('id2: ' + str(id2), file=sys.stderr)
        print('vec1.shape: ' + str(vec1.shape), file=sys.stderr)
        print('vec2.shape: ' + str(vec2.shape), file=sys.stderr)
        print('np.sum(vec1): ' + str(np.sum(vec1)), file=sys.stderr)
        print('np.sum(vec2): ' + str(np.sum(vec2)), file=sys.stderr)

    cos = cosine_similarity(vec1.reshape(1,-1),vec2.reshape(1,-1))[0,0]
    print(str(cos) + '\t' + rline)
    sys.stdout.flush()


print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
