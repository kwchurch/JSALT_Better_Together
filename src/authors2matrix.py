#!/usr/bin/env python

import numpy as np
import os,sys,argparse,scipy.sparse,time

t0 = time.time()
errors = 0

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="filename", required=True)
parser.add_argument("-o", "--output", help="filename", required=True)
parser.add_argument('-m', '--paper_map', help="*.npz file", default='/work/k.church/semantic_scholar/citations/graphs/citations.G.shrink.new.T1.npz')
parser.add_argument('-a', '--authors', help="*.L file", default='/work/k.church/semantic_scholar/authors/authors.id.L')
args = parser.parse_args()

slurm=os.environ.get('SLURM_ARRAY_TASK_ID')

if '%' in args.input and not slurm is None:
    input_file = args.input % int(slurm)
else:
    input_file = args.input

if '%' in args.output and not slurm is None:
    output_file = args.output % int(slurm)
else:
    output_file = args.input


paper_map = np.load(args.paper_map)
with open(args.authors, 'rb') as fd:
    authors = np.frombuffer(fd.read(), dtype=int)

npapers = len(paper_map['new_to_old'])
nauthors = len(authors)

authors_dict = dict(zip(authors, range(len(authors))))

print(str(time.time() - t0) + ' sec: finished initialization', file=sys.stderr)
sys.stderr.flush()

X = []
Y = []
with open(input_file, 'r') as fd:
    for lineno,line in enumerate(fd):
        if lineno % 100 == 0:
            print('sec: %0.f, lineno: %d' % (time.time() - t0, lineno), file=sys.stderr)
            sys.stderr.flush()
        fields = line.rstrip().split('\t')
        if len(fields) >= 2:
            p,a = fields[0:2]
            try:
                newp = paper_map['old_to_new'][int(p)]
                if newp <= 0: continue
                for oa in a.split('|'):
                    oai = int(oa)
                    if oai in authors_dict:
                        newa = authors_dict[int(oa)]
                        X.append(newp)
                        Y.append(newa)
            except:
                errors += 1

# print('X: ' + str(X), file=sys.stderr)
# print('Y: ' + str(Y), file=sys.stderr)

vals = np.ones(len(X), dtype=bool)

X = np.array(X, dtype=np.int32)
Y = np.array(Y, dtype=np.int32)

A = scipy.sparse.csr_matrix((vals, (X, Y)), shape=(npapers, nauthors), dtype=bool)

scipy.sparse.save_npz(output_file, A)

print(str(time.time() - t0) + ' sec: done; %d errors' % errors, file=sys.stderr)

# reconstitute with:
# M = scipy.sparse.load_npz('dicts/en-es.0-5000.npz')

