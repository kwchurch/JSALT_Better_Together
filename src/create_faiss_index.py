#!/usr/bin/env python

# https://github.com/matsui528/faiss_tips
# https://www.pinecone.io/learn/series/faiss/vector-indexes/

# https://github.com/facebookresearch/faiss/wiki/Faiss-indexes#inverted-file-with-pq-refinement


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
parser.add_argument("--embedding", help='filename', default=None)
parser.add_argument("--output", help='filename', required=True)
parser.add_argument("--start", type=int, help='row to start on', default=0)
parser.add_argument("--end", type=int, help='row to end on', default=-1)
parser.add_argument("--old_ids", help='filename containing old ids', default=None)
parser.add_argument("--new_ids", help='filename containing new ids', default=None)
parser.add_argument("-i", "--input_directory", help="a directory", default=None)
parser.add_argument("--index_method", help="IVF|HNSW", required=True)
parser.add_argument("--HNSW_sample_size", type=int, help="used to create HNSW index", default=100000)
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
    # fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : map_from_dir(dir),
             'embedding' : embedding_from_dir(dir, K)}

config=None

if args.embedding is None:
    config = directory_to_config(args.input_directory)

if not args.new_ids is None:
    new_ids = np.loadtxt(args.new_ids, dtype=int)
    embedding = config['embedding'][new_ids,:]
elif not args.old_ids is None:
    old_ids = np.loadtxt(args.old_ids, dtype=int)
    M = config['map']
    old_ids = old_ids[old_ids < len(M)]
    new_ids = M[old_ids]
    new_ids = new_ids[new_ids > 0]
    embedding = config['embedding'][new_ids,:]
elif not args.embedding is None:
    embedding = np.load(args.embedding)
    if args.embedding.endswith('npz') and 'embedding' in embedding:
        embedding = embedding['embedding']
else:
    embedding = config['embedding'][args.start:args.end,:]

print('%0.f sec: about to index' % (time.time() -t0), file=sys.stderr)
sys.stderr.flush()

d=embedding.shape[1]

nlist = args.nlist
if nlist <= 0:
    nlist = int(np.sqrt(embedding.shape[0]))

if args.index_method == "IVF":
    quantizer = faiss.IndexFlatIP(d)  # how the vectors will be stored/compared
    index = faiss.IndexIVFFlat(quantizer, d, nlist)
    index.train(embedding)  # we must train the index to cluster into cells

elif args.index_method == "HNSW":
    choices = np.random.choice(args.HNSW_sample_size, embedding.shape[0])
    Xt = embedding[choices,:]  # 10000 vectors for training

    # Param of PQ
    # The number of sub-vector. Typically this is 8, 16, 32, etc.
    # This has to be a factor of d
    if d == 280 or d == 200:
        M = 40 
    elif d == 768:
        M = 48
    elif d == 1024:
        M = 64
    else:
        M = 1

    nbits = 8 # bits per sub-vector. This is typically 8, so that each sub-vec is encoded by 1 byte
    # Param of HNSW
    hnsw_m = 64  # The number of neighbors for HNSW. This is typically 32

    # Setup
    quantizer = faiss.IndexHNSWFlat(d, hnsw_m)
    index = faiss.IndexIVFPQ(quantizer, d, nlist, M, nbits)

    index.train(Xt)

elif args.index_method == "HNSW.new":

    if d == 280 or d == 200:
        M = 40 
    elif d == 768:
        M = 48
    elif d == 1024:
        M = 64
    else:
        M = 1

    ef_search = 32  # depth of layers explored during search
    ef_construction = 64  # depth of layers explored during index construction

    # initialize index (d == 128)
    index = faiss.IndexHNSWFlat(d, M)
    # set efConstruction and efSearch parameters
    index.hnsw.efConstruction = ef_construction
    index.hnsw.efSearch = ef_search

else:
    assert False, 'bad --index_method should be IVR or HNSW: ' + str(args.index_method)

print('%0.f sec: about to add centroids with shape: %s' % (time.time() -t0, str(embedding.shape)), file=sys.stderr)
# and levels (or layers) are now populated

try:
    levels = faiss.vector_to_array(index.hnsw.levels)
    print('%0.f sec: levels: %s' % (time.time() -t0, str(np.bincount(levels))), file=sys.stderr)
except:
    print('%0.f sec: levels NA')

sys.stderr.flush()

index.add(embedding)
index.nprobe = args.nprobe

# Show params
print("D:", index.d, file=sys.stderr)
print("N:", index.ntotal, file=sys.stderr)
try:
    print("M:", index.pq.M, file=sys.stderr)
    print("nbits:", index.pq.nbits, file=sys.stderr)
    print("nlist:", index.nlist, file=sys.stderr)
    print("nprobe:", index.nprobe, file=sys.stderr)
except:
    print("warning, failed to print params", file=sys.stderr)

try:
    levels = faiss.vector_to_array(index.hnsw.levels)
    print('%0.f sec: levels: %s' % (time.time() -t0, str(np.bincount(levels))), file=sys.stderr)
except:
    print('%0.f sec: levels NA')

faiss.write_index(index, args.output)
print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)



