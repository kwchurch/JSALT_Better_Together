x1#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np
from sklearn.preprocessing import normalize

t0 = time.time()

print('normalize_embedding.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

# assumes the input directory contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_directory", help="a directory", required=True)
parser.add_argument("--batch_size", type=int, help="do it in pieces", default=None)
args = parser.parse_args()

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return int(fd.read().split()[0])

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

config = directory_to_config(args.input_directory)
embedding = config['embedding']

if args.batch_size is None:
    norm = normalize(embedding)
    norm.tofile(args.input_directory + '/embedding.norm.f')

else:
    with open(args.input_directory + '/embedding.norm.f', 'wb') as fd:
        for i in range(0, len(embedding), args.batch_size):
            end = min(len(embedding), i+ args.batch_size)
            norm = normalize(embedding[i:end,:])
            norm.tofile(fd)

print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)
