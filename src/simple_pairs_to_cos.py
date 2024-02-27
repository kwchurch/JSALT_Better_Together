#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

t0 = time.time()

print('pairs_to_cos: ' + str(sys.argv), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

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

emb = config['embedding']

def get_mapped_refs(refs):
    if not config['map32'] is None:
        maxid = config['map32'].shape[0]
        my_map = config['map32'].reshape(-1)
        mapped_refs = np.array([ my_map[ref] for ref in refs if not ref is None and ref < maxid ], dtype=int)
        return mapped_refs[mapped_refs > 0]
    elif not config['map64'] is None:
        m = config['map64']
        s = np.searchsorted(m, refs)
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

def get_vec(id):
    new_id = None
    m = get_mapped_refs([id])
    if len(m) < 1: return None
    if m[0] < 0 or m[0] > len(emb): return None
    return emb[m[0],:]

def do_it(id1, id2, extras):
    vec1 = get_vec(id1)
    if vec1 is None:
        print('-1\t' + rline)
        return
    vec2 = get_vec(id2)
    if vec2 is None:
        print('-1\t' + rline)
        return

    cos = cosine_similarity(vec1.reshape(1,-1),vec2.reshape(1,-1))[0,0]
    print(str(cos) + '\t' + str(id1) + '\t' + str(id2) + '\t' + '\t'.join(extras))

for line in sys.stdin:
    rline = line.rstrip()
    fields = rline.split()
    if len(fields) < 2: continue
    id1,id2 = fields[0:2]
    if not id1.isdigit() or not id2.isdigit(): continue
    do_it(int(id1), int(id2), fields[2:])

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
