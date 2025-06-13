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
parser.add_argument('--skip_cos', action='store_true')
parser.add_argument('--binary_output', default=None)
parser.add_argument('--topN', type=int, default=10)
parser.add_argument('--pad_factor', type=int, default=3)
parser.add_argument('--limit', type=int, default=100000)
parser.add_argument('--number_of_landmarks', type=int, default=50)
parser.add_argument('--landmarks_dir', default='/class_pieces/top100')
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
parser.add_argument("--verbose_save", help="filename", default=None)
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

def postings_from_dir(dir):
    fn = dir + args.landmarks_dir + '/landmarks.i'
    fn_len = os.path.getsize(fn)
    # print('fn_len: ' + str(fn_len))
    landmarks = np.memmap(fn,
                          shape=(int(fn_len/(args.number_of_landmarks*4)),
                                 args.number_of_landmarks),  
                          dtype=np.int32, mode='r')
    fn = dir + args.landmarks_dir + '/postings.i'
    assert os.path.exists(fn), str(fn) + ' does not exist'
    fn_len = os.path.getsize(fn)
    postings = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')
    print('postings.shape: ' + str(postings.shape), file=sys.stderr)

    fn = dir + args.landmarks_dir + '/postings.idx.i'
    assert os.path.exists(fn), str(fn) + ' does not exist'
    fn_len = os.path.getsize(fn)
    postings_idx = np.memmap(fn, shape=(int(fn_len/8)),  dtype=int, mode='r')
    print('postings_idx.shape: ' + str(postings_idx.shape), file=sys.stderr)

    return { 'landmarks' : landmarks,
             'postings' : postings,
             'postings_idx' : postings_idx }


# def classes_from_dir(dir):
#     fn = dir + '/class_pieces/classes.i'
#     fn_len = os.path.getsize(fn)
#     classes = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')

#     fn = dir + '/class_pieces/classes.idx.i'
#     fn_len = os.path.getsize(fn)
#     idx = np.memmap(fn, shape=(int(fn_len/8)),  dtype=int, mode='r')

#     fn = dir + '/class_pieces/classes.inv.i'
#     fn_len = os.path.getsize(fn)
#     inv = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')

#     return { 'classes' : classes,
#              'idx' : idx,
#              'inv' : inv }


def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : {'old_to_new' : map_from_dir(dir),
                      'new_to_old' : imap_from_dir(dir)},
             'postings' : postings_from_dir(dir),
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

# def get_ids_for_class(c):
#     idx = config['classes']['idx']
#     # print('new_id: %d, class: %d' % (new_id, c), file=sys.stderr)
#     if c == 0:
#         start = 0
#     else:
#         start = idx[c-1]

#     end = idx[c]
#     if end - start > args.limit:
#         end = start + args.limit
    
#     return config['classes']['inv'][start:end]

def get_postings(c):
    
    # print('get_postings: ' + str(c))

    idx = config['postings']['postings_idx']
    # print('new_id: %d, class: %d' % (new_id, c), file=sys.stderr)
    if c == 0:
        start = 0
    else:
        start = idx[c-1]

    end = idx[c]
    # if end - start > args.limit:
    #     end = start + args.limit
    
    # print('start: ' + str(start))
    # print('end: ' + str(end))
    res = config['postings']['postings'][start:end]
    # print('len(res): ' + str(len(res)))
    return res

def my_cos(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    return (v1 @ v2.T)[0,0]/(n1 * n2)

# numpy.unique(ar, return_index=False, return_inverse=False, return_counts=False, axis=None, *, equal_nan=True)

def output_nears(nears, fn):
    print('output_nears: ' + fn, file=sys.stderr)
    for i,n in enumerate(nears):
        n.tofile('%s.%03d.i' % (fn, i))

def summarize_nears(nears):
    if not args.verbose_save is None:
        output_nears(nears, args.verbose_save)
    l = sum([len(n) for n in nears])
    res = np.zeros(l, dtype=np.int32)
    i=0    
    for n in nears:
        i2 = i + len(n)
        res[i:i2] = n
        i=i2
    return np.unique(res, return_counts=True)

def old_summarize_nears(nears):
    res = {}
    for n in nears:
        # print('len(n): ' + str(len(n)))
        for nn in n:
            if not nn in res:
                res[nn] = 0;
            res[nn] += 1
    return res                

if args.skip_cos:
    print('corpus_id1\tcorpus_id2\tintersections')
else:
    print('corpus_id1\tcorpus_id2\tcos\trank\tintersections')

for line in sys.stdin:
    fields = line.rstrip().split('\t')
    if len(fields) == 1:
        old_id = int(fields[0])
        new_id = -1
        if old_id >= 0 and old_id < len(config['map']['old_to_new']):
            new_id = config['map']['old_to_new'][old_id]
        # print('new_id: ' + str(new_id))
        # print('old_id: ' + str(old_id))
        # print('shape: ' + str(config['postings']['landmarks'].shape))
        classes = None
        if new_id >= 0 and new_id < len(config['postings']['landmarks']):
            classes = config['postings']['landmarks'][new_id,:].reshape(-1)
            if args.verbose: print('classes: ' + str(classes), file=sys.stderr)
            if classes[0] == classes[1]:
                classes = None
            if args.verbose:
                print('classes: ' + str(classes))
        if classes is None:
            print(fields[0] + '\tNA')
            continue
    elif len(fields) != 3: continue
    else:
        row = fields[0]
        if row == 'row': continue
        classes = fields[1].split('|')
        new_id = int(row)
        old_id = config['map']['new_to_old'][new_id]
    vec = config['embedding'][new_id,:].reshape(1,-1)
    # nears = [get_ids_for_class(int(c)) for c in classes]

    # print('classes: ' + str(classes))
    nears = [get_postings(int(c)) for c in classes]

    summary_ids,summary_counts = summarize_nears(nears)

    c = np.bincount(summary_counts)
    cc = np.cumsum(c)
    
    N = np.sum(c)
    T = 0
    for i,x in enumerate(N - cc):
        if x > args.pad_factor*args.topN:
            T=i

    T = T+1
    s0 = summary_counts > T

    near0 = summary_ids[s0]
    inter0 = summary_counts[s0]

    shortfall = args.pad_factor*args.topN - len(near0)
    # print('shortfall: ' + str(shortfall) + ' len(near0): ' + str(len(near0)) + ' args.topN: ' + str(args.topN))

    if shortfall > 0:
        s1 = summary_counts == T
        sum_s1 = sum(s1)

        print('sum_s1: ' + str(sum_s1))
        print('shortfall: ' + str(shortfall))
        print('T: ' + str(T))
        
        if sum_s1 < shortfall:
            shortfall=s1

        near1 = summary_ids[s1][0:shortfall]
        near = np.append(near0, near1)

        inter1 = summary_counts[s1][0:shortfall]
        intersections = np.append(inter0, inter1)
    else:
        near = near0
        intersections = inter0

    # intersections = summary_counts[s]
    if not args.skip_cos:
        print('len(near): ' + str(len(near)))
    o = config['map']['new_to_old'][near]

    if args.skip_cos:
        for oo,inter in zip(o, intersections):
            print('\t'.join(map(str, [old_id, oo, inter])))
    else:
        nvec = config['embedding'][near,:]
        s = cosine_similarity(vec,nvec)
        best = np.argsort(-s[0,:])
        if len(best) > args.topN:
            best = best[0:args.topN]
        for jj, oo,ss,inter in zip(np.arange(len(best)), o[best], s[0,:][best], intersections[best]):
            print('\t'.join(map(str, [old_id, oo, ss, jj, inter])))
    sys.stdout.flush()

