#!/usr/bin/env python

import numpy as np
import csrgraph as cg
from scipy import sparse
from scipy.sparse import load_npz, csr_matrix
from sklearn import preprocessing
from sklearn.utils.extmath import randomized_svd
import sys,argparse,time,socket,os

print('prefactor_graph.py: sys.argv = ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()

JSALT=os.environ.get('JSALTdir')

parser = argparse.ArgumentParser()
parser.add_argument("-A", "--author", help="npz file (paper by author matrix)",
                    default=JSALT + '/semantic_scholar/releases/2023-06-20/database/papers/authors/papers_to_authors.npz')
parser.add_argument("--normalize", action='store_true')
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-B", "--bigrams", help="npz file", default=JSALT + '/semantic_scholar/embeddings/proposed/bigrams.npz')
args = parser.parse_args()

author = load_npz(args.author)

print('# loaded author, shape = %s: %0.2f' % (str(author.shape), time.time() - t0), file=sys.stderr)
sys.stderr.flush()

evidence = load_npz(args.bigrams)

print('# loaded evidence, shape = %s : %0.2f' % (str(evidence.shape), time.time() - t0), file=sys.stderr)
sys.stderr.flush()

author2 = author.T

if args.normalize:
    author2 = preprocessing.normalize(author2, "l1")
    print('# normalized author: %0.2f' % (time.time() - t0), file=sys.stderr)
    evidence = preprocessing.normalize(evidence, "l1")
    print('# normalized evidence: %0.2f' % (time.time() - t0), file=sys.stderr)

# res = author2 @ evidence @author2.T

N0 = author2.shape[1]
N1 = evidence.shape[0]

print('# N0 = %d, N1 = %d : %0.2f' % (N0, N1, time.time() - t0), file=sys.stderr)

if N0 > N1:
    evidence.resize(N0, evidence.shape[1])
elif N1 > N0:
    author2.resize(author2.shape[0], N1)

print('author2.shape = %s, evidence.shape = %s : %0.2f' % (str(author2.shape), str(evidence.shape), time.time() - t0), file=sys.stderr)

res = author2 @ evidence

print('# about to save: %0.2f' % (time.time() - t0), file=sys.stderr)
sys.stderr.flush()

save_npz(args.output, res)

print('# done: %0.2f' % (time.time() - t0), file=sys.stderr)
