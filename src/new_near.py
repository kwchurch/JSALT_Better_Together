#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pdb

t0 = time.time()

# print('id_to_floats: ' + str(sys.argv), file=sys.stderr)

apikey=os.environ.get('SPECTER_API_KEY')

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument('--no_map', action='store_true')
parser.add_argument('--binary_output', default=None)
parser.add_argument('--topN', type=int, default=10)
parser.add_argument('--limit', type=int, default=1000)
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
# parser.add_argument("--directory_to_find_references", help="use Semantic Scholar API if None", default=None)
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)

args = parser.parse_args()

if args.no_map:
    assert args.use_references == 'never', 'with --no_map option, please use --use_references == "never"'

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

def imap_from_dir(dir):
    fn = dir + '/map.new_to_old.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def embedding_from_dir(dir, K):
    fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def classes_from_dir(dir):
    fn = dir + '/class_pieces/classes.i'
    fn_len = os.path.getsize(fn)
    classes = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')

    fn = dir + '/class_pieces/classes.idx.i'
    fn_len = os.path.getsize(fn)
    idx = np.memmap(fn, shape=(int(fn_len/8)),  dtype=int, mode='r')

    fn = dir + '/class_pieces/classes.inv.i'
    fn_len = os.path.getsize(fn)
    inv = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')

    return { 'classes' : classes,
             'idx' : idx,
             'inv' : inv }

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : {'old_to_new' : map_from_dir(dir),
                      'new_to_old' : imap_from_dir(dir)},
             'classes' : classes_from_dir(dir) ,
             'embedding' : embedding_from_dir(dir, K)}

config = directory_to_config(args.dir)

# def get_corpusId(ref):
#     try:
#         return ref['externalIds']['CorpusId']
#     except:
#         return None

# def id_to_references(my_id):

#     if not args.graph is None:
#         return extract_row(int(my_id))

#     cmd = 'https://api.semanticscholar.org/graph/v1/paper/CorpusId:' + str(my_id) + '/?fields=references,references.externalIds'
#     j = requests.get(cmd, headers={"x-api-key": apikey}).json()
#     if 'references' in j and not j['references'] is None:
#         return [ get_corpusId(ref) for ref in j['references']]
#     else:
#         return []

# maxid = config['map'].shape[0]
# my_map = config['map'].reshape(-1)
# emb = config['embedding']

# def centroid(refs):
#     mapped_refs = np.array([ my_map[ref] for ref in refs if not ref is None and ref < maxid ], dtype=int)
#     mapped_refs = mapped_refs[mapped_refs > 0]
#     vectors = emb[mapped_refs,:]
#     if args.verbose:
#         print('centroid: vectors.shape = ' + str(vectors.shape), file=sys.stderr)

#     if len(vectors) > 0:
#         return np.mean(vectors, axis=0)
#     else:
#         return np.zeros(emb.shape[1], dtype=int)

# def id_to_centroid(id):
#     return centroid(id_to_references(id))

# query=3051291
# ref = id_to_references(str(query))
# pdb.set_trace()

# ids = np.loadtxt(sys.stdin).astype(int)
# ids = np.array([int(i) for i in sys.stdin.read().split('\n') if len(i) > 0], dtype=int)

# if args.verbose:
#     print('ids.shape = ' + str(ids.shape), file=sys.stderr)

# if args.no_map:
#     result = emb[ids,:]
# elif args.use_references == 'never' or args.use_references == 'when_necessary':
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

def get_ids_for_class(new_id):
    c = config['classes']['classes'][new_id]
    idx = config['classes']['idx']
    # print('new_id: %d, class: %d' % (new_id, c), file=sys.stderr)
    if c == 0:
        start = 0
    else:
        start = idx[c-1]

    end = idx[c]
    if end - start > args.limit:
        end = start + args.limit
    
    return config['classes']['inv'][start:end]

def my_cos(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    return (v1 @ v2.T)[0,0]/(n1 * n2)

# for line in ['9024416']:
# for line in sys.stdin:
#     if len(line) > 0:
#         old_id = int(line)
#         new_id = config['map']['old_to_new'][old_id]
#         vec = config['embedding'][new_id,:].reshape(1,-1)
#         # pdb.set_trace()
#         near = get_ids_for_class(new_id)
#         for n in near:
#             o = config['map']['new_to_old'][n]
#             nvec = config['embedding'][n,:].reshape(1,-1)
#             s = cosine_similarity(vec,nvec)
#             ss = my_cos(vec,nvec)
#             print('\t'.join(map(str, [old_id, o, s, ss, vec.shape, nvec.shape])))

for line in sys.stdin:
    if len(line) > 0:
        old_id = int(line)
        new_id = config['map']['old_to_new'][old_id]
        vec = config['embedding'][new_id,:].reshape(1,-1)
        # pdb.set_trace()
        near = get_ids_for_class(new_id)
        # print('near.shape: ' + str(near.shape), file=sys.stderr)
        # print(near)

        # for n in near:
        #     o = config['map']['new_to_old'][n]
        #     nvec = config['embedding'][n,:].reshape(1,-1)
        #     s = cosine_similarity(vec,nvec)[0,0]
        #     print('\t'.join(map(str, [old_id, o, s])))

        o = config['map']['new_to_old'][near]
        nvec = config['embedding'][near,:]
        s = cosine_similarity(vec,nvec)


        best = np.argsort(-s[0,:])
        if len(best) > args.topN:
            best = best[0:args.topN]

        for oo,ss in zip(o[best], s[0,:][best]):
            print('\t'.join(map(str, [old_id, oo, ss])))

            


