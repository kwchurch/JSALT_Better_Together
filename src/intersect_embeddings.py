#!/usr/bin/env python

import argparse
import os,sys,argparse,time
import numpy as np

t0 = time.time()

print('intersect_embeddings: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

# assert False, 'not yet written'

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--input_dirs", help="two directories such as $proposed or $specter, comma separated", required=True)
parser.add_argument("--output_dirs", help="two directories such as $proposed or $specter, comma separated", required=True)
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

def create_record_size_file(dir, K):
    with open(dir + '/record_size', 'w') as fd:
        print(str(K), file=fd)
        fd.flush()

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

configs = [directory_to_config(dir) for dir in args.input_dirs.split(',')]
assert len(configs) == 2, 'expected two directories in --input_dirs: ' + args.input_dirs

N = min([config['embedding'].shape[0] for config in configs])

indexes = [config['map32'] for config in configs]
ll = min([len(idx) for idx in indexes])

common_indexes = np.arange(ll)[np.minimum(indexes[0][0:ll], indexes[1][0:ll]) > 0]

if np.max(common_indexes) >= N:
    common_indexes = np.arange(len(common_indexes))[common_indexes < N]

output_dirs = args.output_dirs.split(',')

def my_output(dir, config, indexes):
    print('%0.0f sec: outputing to %s' % (time.time() - t0, dir), file=sys.stderr)
    sys.stderr.flush()

    assert not os.path.exists(dir), 'my_output: %s already exists' % dir
    os.makedirs(dir)
    K = config['embedding'].shape[1]
    create_record_size_file(dir, K)
    np.savetxt(dir + '/mapping', indexes, fmt='%d')
    config['embedding'][indexes,:].tofile(dir + '/embedding.f')

my_output(output_dirs[0], configs[0], common_indexes)
my_output(output_dirs[1], configs[1], common_indexes)

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
