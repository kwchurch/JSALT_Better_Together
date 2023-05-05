#!/usr/bin/env python

import sys,argparse,scipy.sparse

parser = argparse.ArgumentParser()
parser.add_argument("-N", "--number_of_nodes", type=int, help="number of nodes", default=300000000)
parser.add_argument("-i", "--input", help="list of edges", required=True)
parser.add_argument("-o", "--output", help="filename", required=True)
args = parser.parse_args()

errors=0

def pairs_to_matrix():
    N = args.number_of_nodes
    res = scipy.sparse.dok_matrix((N, N), dtype=bool)
    with open(args.input, 'r') as fd:
        for line in fd:
            fields = line.rstrip().split()
            if len(fields) >= 2:
                a,b = fields[0:2]
                if a.startswith('id') and b.startswith('id'):
                    ai = int(a[2:])
                    bi = int(b[2:])
                    if ai < 0 or ai >= N or bi < 0 or bi >= N:
                        errors += 1
                    else:
                        res[ai,bi]=True
    return scipy.sparse.csr_matrix(res)

M = pairs_to_matrix()
print('%d errors' % errors, file=sys.stderr)

scipy.sparse.save_npz(args.output, M)


# reconstitute with:
# M = scipy.sparse.load_npz('dicts/en-es.0-5000.npz')

