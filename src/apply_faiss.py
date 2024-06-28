#!/usr/bin/env python

# https://github.com/matsui528/faiss_tips
# https://www.pinecone.io/learn/series/faiss/vector-indexes/

import faiss
import os,sys,argparse,time
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import euclidean_distances

t0 = time.time()

print('apply_faiss.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

# assumes the input directory contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, help='row to start on', default=0)
parser.add_argument("--end", type=int, help='row to end on', default=-1)
parser.add_argument("-i", "--input_directory", help="a directory", default=None)
parser.add_argument("--IVF", help="use inverted files for indexing", action='store_true')
parser.add_argument("--HNSW", help="use HNSW for indexing", action='store_true')
parser.add_argument("--topN", type=int, default=20)
parser.add_argument("--HNSW_sample_size", type=int, help="use to create HNSW index", default=10000)
parser.add_argument("--nprobe", help="how many nearest cells to search (for IVF and HNSW)", type=int, default=8)
parser.add_argument("--nlist", help="number of cells/clusters to partition data into (for IVF and HNSW)", type=int, default=-1)

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

print('row\tclass\tdistance')
sys.stdout.flush()
print('%0.f sec: about to index' % (time.time() -t0), file=sys.stderr)
sys.stderr.flush()

d=embedding.shape[1]

nlist = args.nlist
if nlist <= 0:
    nlist = int(np.sqrt(embedding.shape[0]))

if args.IVF:
    index_file = args.input_directory + '/faiss.IVF.index'
    if os.path.exists(index_file):
        index = faiss.read_index(index_file)
    else:
        quantizer = faiss.IndexFlatIP(d)  # how the vectors will be stored/compared
        index = faiss.IndexIVFFlat(quantizer, d, nlist)
        index.train(embedding)  # we must train the index to cluster into cells

        try:
            faiss.write_index(index, index_file)
            print('%0.f sec: saved index: %s' % (time.time() -t0, index_file), file=sys.stderr)
        except:
            print('%0.f sec: unable to save index: %s' % (time.time() -t0, index_file), file=sys.stderr)

elif args.HNSW:
    index_file = args.input_directory + '/faiss.HNSW.index'
    if os.path.exists(index_file):
        index = faiss.read_index(index_file)
    else:
        choices = np.random.choice(args.HNSW_sample_size, embedding.shape[0])
        Xt = embedding[choices,:]  # 10000 vectors for training

        # Param of PQ
        # The number of sub-vector. Typically this is 8, 16, 32, etc.
        # This has to be a factor of d
        if d == 280 or d == 200:
            M = 20 
        elif d == 768:
            M = 24
        else:
            M = 1

        nbits = 8 # bits per sub-vector. This is typically 8, so that each sub-vec is encoded by 1 byte
        # Param of HNSW
        hnsw_m = 32  # The number of neighbors for HNSW. This is typically 32

        # Setup
        quantizer = faiss.IndexHNSWFlat(d, hnsw_m)
        index = faiss.IndexIVFPQ(quantizer, d, nlist, M, nbits)

        index.train(Xt)

        try:
            faiss.write_index(index, index_file)
            print('%0.f sec: saved index: %s' % (time.time() -t0, index_file), file=sys.stderr)
        except:
            print('%0.f sec: unable to save index: %s' % (time.time() -t0, index_file), file=sys.stderr)

else:
    index = faiss.IndexFlatIP(d) 

print('%0.f sec: about to add centroids with shape: %s' % (time.time() -t0, str(embedding.shape)), file=sys.stderr)
sys.stderr.flush()

if index.ntotal == 0:
    index.add(embedding)
    if args.HNSW or args.IVF:
        if args.HNSW:
            index_file = args.input_directory + '/faiss.HNSW.index'
        else:
            index_file = args.input_directory + '/faiss.IVF.index'
        try:
            faiss.write_index(index, index_file)
            print('%0.f sec: saved index: %s' % (time.time() -t0, index_file), file=sys.stderr)
        except:
            print('%0.f sec: unable to save index: %s' % (time.time() -t0, index_file), file=sys.stderr)

if args.IVF or args.HNSW:
    index.nprobe = args.nprobe

print('%0.f sec: finished indexing' % (time.time() -t0), file=sys.stderr)

sys.stderr.flush()
end = embedding.shape[0]
if args.end >= 0:
    end = args.end

for row in range(args.start, end):
    q = embedding[row,:].reshape(1,-1)
    D,I = index.search(q,args.topN)
    print(str(row) + '\t' + '|'.join(map(str, I.reshape(-1))) + '\t' + '|'.join(map(str, D.reshape(-1))))
    sys.stdout.flush()

print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)



