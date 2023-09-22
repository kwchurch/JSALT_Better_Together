#!/usr/bin/env python

# input: authors
# output: papers 

import numpy as np
import sys,json,requests,os,argparse
from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)
parser.add_argument("--use_references", help="never|always|when_necessary", default="never")
parser.add_argument('--input_new_pairs', action='store_true')
parser.add_argument('--output', help="output file", required=True)
args = parser.parse_args()

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def print_paper(paper, link_type, query):
    # print(paper)
    if 'externalIds' in paper and not paper['externalIds'] is None:
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], paper['title']])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

def safe(s):
    return s.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

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

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map32' : map32_from_dir(dir),
             'imap32' : imap32_from_dir(dir),
             'map64' : map64_from_dir(dir),
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

author_details = {}

def authorid2vec(authorid):
    # print('do_authorid: ' + str(authorid), file=sys.stderr)
    cmd = 'https://api.semanticscholar.org/graph/v1/author/' + str(authorid) + '/?fields=name,hIndex,papers,papers.externalIds'

    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    author_details[authorid] = j

    if not 'papers' in j: return None
    if len(j['papers']) <= 0: return None

    vecs = [get_vec(p['externalIds']['CorpusId'], args.use_references) for p in j['papers']]
    vecs = [v for v in vecs if not v is None ]

    if len(vecs) <= 0: return None

    vecs = np.array(vecs)

    # print('vecs.shape: ' + str(vecs.shape), file=sys.stderr)
    centroid = np.sum(vecs, axis=0)
    # print('centroid.shape: ' + str(centroid.shape), file=sys.stderr)
    return centroid

authors = np.loadtxt(sys.stdin, converters=int, dtype=int)

# print(authors)
centroids = [authorid2vec(a) for a in authors]

authors2 = []
centroids2 = []

for a,c in zip(authors, centroids):
    if not c is None:
        authors2.append(a)
        centroids2.append(c)

authors2 = np.array(authors, dtype=int)
centroids2 = np.array(centroids2)

from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import complete,leaves_list
o = leaves_list(complete(pdist(centroids2, metric='cosine')))

# np.set_printoptions(linewidth=200, precision=2)

# print(authors2[o])
sim = cosine_similarity(centroids2[o,:])

np.savetxt(args.output + '.sim.tsv', sim)

with open(args.output + '.author.tsv', 'w') as fd:
    print('\t'.join(['id', 'name', 'papers', 'hIndex']), file=fd)
    for a in authors2[o]:
        d = author_details[a]
        print('\t'.join(map(str, [a, d['name'], len(d['papers']), d['hIndex']])), file=fd)


