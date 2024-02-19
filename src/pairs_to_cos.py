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
parser.add_argument('--binary_input', help="input file (optional, use text input from stdin by default)", default=None)
parser.add_argument('--input_new_pairs', action='store_true')
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
# parser.add_argument("--directory_to_find_references", help="use Semantic Scholar API if None", default=None)
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)
parser.add_argument('--number_of_landmarks', type=int, default=50)
parser.add_argument('--landmarks', help="output info about landmarks", action='store_true')
parser.add_argument('--skip_cos', help="output None instead of cosine to save time", action='store_true')
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

def map32_from_dir(dir):
    fn = dir + '/map.old_to_new.i'
    if not os.path.exists(fn): return None
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def imap32_from_dir(dir):
    fn = dir + '/map.new_to_old.i'
    if not os.path.exists(fn): return None
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def map64_from_dir(dir):
    fn = dir + '/map.old_to_new.sorted.L'
    if not os.path.exists(fn): return None
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=int, shape=(int(fn_len/8)), mode='r')

def embedding_from_dir(dir, K):
    fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def postings_from_dir(dir):

    if not args.landmarks:
        return None

    fn = dir + '/class_pieces/top50/landmarks.i'
    fn_len = os.path.getsize(fn)
    # print('fn_len: ' + str(fn_len))
    landmarks = np.memmap(fn,
                          shape=(int(fn_len/(args.number_of_landmarks*4)),
                                 args.number_of_landmarks),  
                          dtype=np.int32, mode='r')
    fn = dir + '/class_pieces/top50/postings.i'
    fn_len = os.path.getsize(fn)
    postings = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')

    fn = dir + '/class_pieces/top50/postings.idx.i'
    fn_len = os.path.getsize(fn)
    postings_idx = np.memmap(fn, shape=(int(fn_len/8)),  dtype=int, mode='r')

    return { 'landmarks' : landmarks,
             'postings' : postings,
             'postings_idx' : postings_idx }
    
def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map32' : map32_from_dir(dir),
             'imap32' : imap32_from_dir(dir),
             'map64' : map64_from_dir(dir),
             'embedding' : embedding_from_dir(dir, K),
             'postings' : postings_from_dir(dir)}

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

emb = config['embedding']

# print('maxid: ' + str(maxid), file=sys.stderr)

def get_mapped_refs(refs):
    if args.input_new_pairs:
        return refs
    if not config['map32'] is None:
        maxid = config['map32'].shape[0]
        my_map = config['map32'].reshape(-1)
        mapped_refs = np.array([ my_map[ref] for ref in refs if not ref is None and ref < maxid ], dtype=int)
        return mapped_refs[mapped_refs > 0]
    elif not config['map64'] is None:
        # print('get_mapped_refs: refs = ' + str(refs), file=sys.stderr)
        m = config['map64']
        s = np.searchsorted(m, refs)
        # print('get_mapped_refs: s = ' + str(s), file=sys.stderr)
        return np.array([ss for ss,rr in zip(s,refs) if m[ss] == rr])        

def new_to_old(new_id):
    imap = config['imap32']
    if not imap is None:
        maxid = imap.shape[0]
        if new_id >= maxid: return -1
        return imap.reshape(-1)[new_id]
    return 'new:' + str(new_id)

def old_to_new(old_id):
    imap = config['map32']
    if not map is None:
        maxid = imap.shape[0]
        if old_id >= maxid: return -1
        return imap.reshape(-1)[old_id]
    return 'new:' + str(new_id)

def centroid(refs):
    mapped_refs = get_mapped_refs(refs)
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

def get_vec(id, use_references):
    new_id = None
    if use_references == 'never':
        m = get_mapped_refs([id])
        if len(m) < 1: return None
        if m[0] < 0 or m[0] > len(emb): return None
        return emb[m[0],:]
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

def get_landmarks(old_id):
    # return config['postings']['landmarks'][old_to_new(old_id),:].reshape(-1)
    try: 
        return config['postings']['landmarks'][old_to_new(old_id),:].reshape(-1)
    except:
        return None    

def posting_length(p):
    idx = config['postings']['postings_idx']
    if p == 0:
        return idx[0]
    else:
        return idx[p] - idx[p-1]

def do_it(id1, id2, extras):
    if args.skip_cos:
        cos = None
    else:
        vec1 = get_vec(id1, args.use_references)
        if vec1 is None:
            print('-1\t' + rline)
            return
        vec2 = get_vec(id2, args.use_references)
        if vec2 is None:
            print('-1\t' + rline)
            return

        if args.verbose:
            print('id1: ' + str(id1), file=sys.stderr)
            print('id2: ' + str(id2), file=sys.stderr)
            print('vec1.shape: ' + str(vec1.shape), file=sys.stderr)
            print('vec2.shape: ' + str(vec2.shape), file=sys.stderr)
            print('np.sum(vec1): ' + str(np.sum(vec1)), file=sys.stderr)
            print('np.sum(vec2): ' + str(np.sum(vec2)), file=sys.stderr)

        cos = cosine_similarity(vec1.reshape(1,-1),vec2.reshape(1,-1))[0,0]

    if args.input_new_pairs:
        id1 = new_to_old(id1)
        id2 = new_to_old(id2)

    if args.landmarks:
        l1 = get_landmarks(id1)
        l2 = get_landmarks(id2)
        if l1 is None or l2 is None:
            joint = None
        else:
            joint = set(l1).intersection(set(l2))
        posting_lengths = np.array([posting_length(j) for j in joint])
        if len(posting_lengths) == 0:
            stats = [0]
        else:
            stats = [len(posting_lengths),
                     np.exp(np.mean(np.log(posting_lengths))),
                     np.median(posting_lengths),
                     np.min(posting_lengths),
                     np.max(posting_lengths),
                     np.sum(posting_lengths)]        
        print('\t'.join(map(str, [cos, id1, id2, '\t'.join(extras), '\t'.join(map(str, stats))])))
    else:
        print(str(cos) + '\t' + str(id1) + '\t' + str(id2) + '\t' + '\t'.join(extras))


if args.binary_input:
    input_ids = map_int64(args.binary_input).reshape(-1, 2)
    for id1,id2 in input_ids:
        do_it(id1, id2)
else:
    for line in sys.stdin:
        rline = line.rstrip()
        fields = rline.split()
        if len(fields) < 2: continue
        id1,id2 = fields[0:2]
        if not id1.isdigit() or not id2.isdigit(): continue
        do_it(int(id1), int(id2), fields[2:])

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
