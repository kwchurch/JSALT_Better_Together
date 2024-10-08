#!/usr/bin/env python

import json,requests,argparse
import os,sys,argparse,time
import numpy as np
import pdb

t0 = time.time()

print(' bigrams_to_bins: ' + str(sys.argv), file=sys.stderr)

apikey=os.environ.get('SPECTER_API_KEY')

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--bigrams", help="a file such as $proposed/bigrams or $specter/bigrams", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument('--ids_to_bins', help="a directory such as $JSALTdir/semantic_scholar/j.ortega/corpusId_to_bin.txt", required=True)
parser.add_argument('--output', help="output filename", required=True)
args = parser.parse_args()

def load_ids_to_bins():
    x = np.loadtxt(args.ids_to_bins).astype(int)
    nx = np.max(x[:,0]) + 1
    res = np.zeros(nx, dtype=np.int8)+100
    res[x[:,0]] = x[:,1]
    return res

def map_bigrams(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r').reshape(-1,3)

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

bigrams = map_bigrams(args.bigrams)
print('bigrams.shape: ' + str(bigrams.shape))

ids_to_bins = load_ids_to_bins()

print('ids_to_bins.shape: ' + str(ids_to_bins.shape))

b1 = ids_to_bins[bigrams[:,1]]
print('b1.shape: ' + str(b1.shape))
b2 = ids_to_bins[bigrams[:,2]]
print('b2.shape: ' + str(b2.shape))

b12 = b1  * 101 + b2
print('b12.shape: ' + str(b12.shape))

b = np.bincount(b12)

result = np.zeros(101*101, dtype=int)
result[0:len(b)] = b

result = result.reshape(101,101)
np.save(args.output, result)

