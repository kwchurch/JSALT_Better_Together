#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


t0 = time.time()

print('nbest_to_graph: ' + str(sys.argv), file=sys.stderr)

apikey=os.environ.get('SPECTER_API_KEY')

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
# parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("--output", help="filename", required=True)
# parser.add_argument('--flush', action='store_true')
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
             'embedding' : embedding_from_dir(dir, K),}

# config = directory_to_config(args.dir)

# def get_vec(ids):
#     return config['embedding'][ids,:]

# imap = config['imap32']

Xfd = open(args.output + '.X.i', 'wb')
Yfd = open(args.output + '.Y.i', 'wb')

for line in sys.stdin:
    rline = line.rstrip()
    fields = rline.split('\t')
    if len(fields) < 2: continue
    id1,id2 = fields[0:2]
    if not id1.isdigit(): continue

    i1 = int(id1)
    ids2 = np.array([int(x) for x in id2.split('|')], dtype=np.int32)
    ids1 = np.zeros(len(ids2), dtype=np.int32) + i1
    ids1.tofile(Xfd)
    ids2.tofile(Yfd)

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
