#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
import pdb

t0 = time.time()

apikey=os.environ.get('SPECTER_API_KEY')

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
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

# query=3051291
# ref = id_to_references(str(query))
# pdb.set_trace()

# ids = np.loadtxt(sys.stdin).astype(int)
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

np.savetxt(sys.stdout, result)
