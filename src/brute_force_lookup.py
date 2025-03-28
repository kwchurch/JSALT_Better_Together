#!/usr/bin/env python

# https://github.com/matsui528/faiss_tips
# https://www.pinecone.io/learn/series/faiss/vector-indexes/

import os,sys,argparse,time,glob
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# from sklearn.preprocessing import normalize
# from sklearn.metrics.pairwise import euclidean_distances

t0 = time.time()

print('brute_force_lookup.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

# assumes the input directory contain 
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--embedding", help='filename', default=None)
parser.add_argument("--topN", type=int, default=20)
args = parser.parse_args()


embedding = np.load(args.embedding)
S = cosine_similarity(embedding)

for row in range(len(embedding)):
    o = np.argsort(-S[row,:])[0:args.topN]
    print(str(row) + '\t' + '|'.join(map(str, o)) + '\t' + '|'.join(map(str, S[row,o])))

print('%0.f sec: done' % (time.time() -t0), file=sys.stderr)



