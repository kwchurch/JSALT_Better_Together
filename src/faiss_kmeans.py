#!/usr/bin/env python

# https://github.com/matsui528/faiss_tips
# https://www.pinecone.io/learn/series/faiss/vector-indexes/

import faiss
import os,sys,argparse,time
import numpy as np

t0 = time.time()

print('faiss_kmeans.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

# assumes the input directory contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, help='row to start on', default=0)
parser.add_argument("--end", type=int, help='row to end on', default=-1)
parser.add_argument("-i", "--input_directory", help="a directory", default=None)
parser.add_argument("-K", "--K", type=int, help="number of clusters", required=True)
parser.add_argument("--niter", type=int, help="number of iterations", default=20)
parser.add_argument("--output_faiss_index", help="file name for output index", default=None)
parser.add_argument("--output_centroids", help="file name for output centroids", default=None)
parser.add_argument("--output_labels", help="file name for output labels", default=None)
parser.add_argument("--verbose", help="turn on kmeans verbose flag", action='store_true')
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

# def indexes_from_dir(dir):
#     print('%0.f sec: about to load indexes' % (time.time() -t0), file=sys.stderr)
#     files = glob.glob(dir + '/faiss.*.index.[0-9][0-9][0-9]')
#     indexes = [ faiss.read_index(f) for f in files]
#     print('%0.f sec: loaded %d indexes' % (time.time() -t0, len(files)), file=sys.stderr)
#     sys.stderr.flush()
#     return indexes

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : map_from_dir(dir),
             'embedding' : embedding_from_dir(dir, K),
         }

config = directory_to_config(args.input_directory)
embedding = config['embedding']

d=embedding.shape[1]

end = embedding.shape[0]
if args.end >= 0:
    end = min(args.end, embedding.shape[0])

queries = embedding[args.start:end,:]

kmeans = faiss.Kmeans(d=d, k=args.K, niter=args.niter, verbose=args.verbose)
kmeans.train(queries)

print('%0.f sec: finished kmeans' % (time.time() -t0), file=sys.stderr)

if not args.output_centroids is None:
    np.save(args.output_centroids, kmeans.centroids)

if not args.output_faiss_index is None:
    faiss.write_index(kmeans.index, args.output_faiss_index)

if not args.output_labels is None:
    dist, labels = kmeans.index.search(queries, 1)
    labels = labels.reshape(-1)
    if args.output_labels.endswith('.i'):
        labels = labels.astype(np.int32)
        labels.tofile(args.output_labels)
    else:
        np.save(args.output_labels, labels)

print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)



