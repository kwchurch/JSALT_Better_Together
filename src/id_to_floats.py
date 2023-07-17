#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np

t0 = time.time()

# assumes the input directory contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
args = parser.parse_args()

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

ids = np.loadtxt(sys.stdin).astype(int)
maxid = config['map'].shape[0]
# print('maxid: ' + str(maxid), file=sys.stderr)
mapped_ids = np.zeros(len(ids), dtype=int)
my_map = config['map'].reshape(-1)

for e,i in enumerate(ids):
    if i < maxid:
        mapped_ids[e] = my_map[i]

emb = config['embedding']

result = emb[mapped_ids,:]
result[mapped_ids == 0,:] = 0

np.savetxt(sys.stdout, result)
