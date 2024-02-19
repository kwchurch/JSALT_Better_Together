#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pdb

t0 = time.time()

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument('--number_of_landmarks', type=int, default=100)
parser.add_argument('--landmarks_dir', default='/class_pieces/top100')
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

Y = idx = None

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
    fn_len = os.path.getsize(fn)
    postings = np.memmap(fn, shape=(int(fn_len/4)),  dtype=np.int32, mode='r')

    fn = dir + args.landmarks_dir + '/postings.idx.i'
    fn_len = os.path.getsize(fn)
    postings_idx = np.memmap(fn, shape=(int(fn_len/8)),  dtype=int, mode='r')

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

for line in sys.stdin:
    fields = line.rstrip().split('\t')
    if len(fields) == 1:
        c = int(fields[0])
        p = get_postings(c)
        for pp in p:
            print(fields[0] + '\t' + str(pp))
