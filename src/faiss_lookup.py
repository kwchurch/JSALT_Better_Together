#!/usr/bin/env python

# https://github.com/matsui528/faiss_tips
# https://www.pinecone.io/learn/series/faiss/vector-indexes/

import faiss
import os,sys,argparse,time,glob
import numpy as np
# from sklearn.preprocessing import normalize
# from sklearn.metrics.pairwise import euclidean_distances

t0 = time.time()

print('faiss_lookup.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

# assumes the input directory contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, help='row to start on', default=0)
parser.add_argument("--end", type=int, help='row to end on', default=-1)
parser.add_argument("--input_vectors", help='npy file (alternative to --input_directory)', default=None)
parser.add_argument("-i", "--input_directory", help="a directory", default=None)
parser.add_argument("--topN", type=int, default=20)
parser.add_argument("--nprobe", help="how many nearest cells to search (for IVF and HNSW)", type=int, default=8)
parser.add_argument("--suffix", help="magic (suggest you use the default)", default="")
args = parser.parse_args()

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return int(fd.read().split()[0])

def map_from_dir(dir):
    fn = dir + '/map.old_to_new.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def embedding_from_dir(dir, K):
    fn = dir + '/embedding.norm.f'
    # fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def indexes_from_dir(dir):
    print('%0.f sec: about to load indexes' % (time.time() -t0), file=sys.stderr)
    files = glob.glob(dir + '/faiss.*.index.[0-9][0-9][0-9]' + args.suffix)
    indexes = [ faiss.read_index(f) for f in files]
    print('%0.f sec: loaded %d indexes' % (time.time() -t0, len(files)), file=sys.stderr)
    sys.stderr.flush()
    return indexes

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : map_from_dir(dir),
             'embedding' : embedding_from_dir(dir, K),
             'indexes': indexes_from_dir(dir),
         }

config = directory_to_config(args.input_directory)

print('row\tclass\tdistance')

if args.input_vectors:
    queries = np.load(args.input_vectors)
    from sklearn.preprocessing import normalize
    queries = normalize(queries)
    end = len(queries)
    if args.end >= 0:
        end = min(args.end, end)

else:
    embedding = config['embedding']
    d=embedding.shape[1]
    end = embedding.shape[0]
    if args.end >= 0:
        end = min(args.end, end)
        queries = embedding[args.start:end,:]

result_heap = faiss.ResultHeap(nq=len(queries), k=args.topN)
indexes = config['indexes']
z = np.zeros(1, dtype=int)
totals = np.append(z, np.cumsum(np.array([idx.ntotal for idx in indexes])))

for idx,tot in zip(indexes, totals):
    D,I = idx.search(queries,args.topN)
    result_heap.add_result(D=D, I=I + tot)
result_heap.finalize()

for row,I,D in zip(range(args.start,end),result_heap.I,result_heap.D):
    print(str(row) + '\t' + '|'.join(map(str, I.reshape(-1))) + '\t' + '|'.join(map(str, D.reshape(-1))))

print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)



