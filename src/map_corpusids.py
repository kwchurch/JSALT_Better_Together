#!/usr/bin/env python

import os,sys,argparse
import numpy as np

# t0 = time.time()
# print('map_corpusids: ' + str(sys.argv), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument('--old_to_new', action='store_true')
parser.add_argument('--new_to_old', action='store_true')
args = parser.parse_args()

assert args.old_to_new != args.new_to_old, 'please specify --old_to_new or --new_to_old (but not both)'

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

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

def directory_to_config(dir):
    return { 'dir' : dir,
             'map32' : map32_from_dir(dir),
             'map64' : map64_from_dir(dir),
             'imap32' : imap32_from_dir(dir)}

config = directory_to_config(args.dir)

my_map = None

if args.old_to_new:
    my_map = config['map32']
    print('old\tnew')

if args.new_to_old:
    my_map = config['imap32']
    print('new\told')

assert not my_map is None, 'cannot determine my_map'

for line in sys.stdin:
    rline = line.rstrip()
    if len(rline) == 0: continue
    
    my_id = int(rline)
    
    print(str(my_id) + '\t' + str(my_map[my_id]))

# print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
