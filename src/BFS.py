#!/usr/bin/env python

import scipy.sparse,argparse,sys,time
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-D", "--maxdepth", type=int, help="maximum depth", default=10)
parser.add_argument("-V", '--verbose', action='store_true')
parser.add_argument("-q", '--quick', action='store_true')
args = parser.parse_args()

M = scipy.sparse.load_npz(args.graph)

if args.verbose:
    print('\t'.join(map(str,[">\tloaded graph", M.shape])), file=sys.stderr)
        
def path(M, source, destination):
    t0 = time.time()
    if args.verbose:
        print('\t'.join(map(str,[">\tcalling path", source, destination])), file=sys.stderr)
    queue=[]
    visited = np.zeros(M.shape[0], dtype=bool)
    queue.append((source, 0))
    while queue:
        n,d = queue.pop(0)
        if args.verbose:
            print('\t'.join(map(str,[">\tpop", 'node: ' + str(n), 'dest: ' + str(d), 'queue: ' + str(len(queue))])), file=sys.stderr)
        if n == destination:
            if args.quick:
                return { 'distance': d }
            else: return { 'distance': d,
                           'queuelen': len(queue),
                           'visited': np.sum(visited),
                           'time': time.time() - t0 }
        else:
            _,Y = M[n,:].nonzero()
            if args.verbose:
                print('\t'.join(map(str,[">\tfanout", n, len(Y)])), file=sys.stderr)
            if d < args.maxdepth:
                for y in Y:
                    if not visited[y]:
                        queue.append((y,d+1))
                        visited[y] = True
    if args.quick:
        return { 'distance': d }
    else: 
        return { 'distance': None,
                 'queuelen': len(queue),
                 'visited': np.sum(visited),
                 'time': time.time() - t0 }

for line in sys.stdin:
    rline = line.rstrip()
    fields = rline.split('\t')
    if len(fields) >= 2:
        s,d = fields[0:2]
        p = path(M, int(s), int(d))
        if args.quick:
            p = p['distance']
        print(str(p) + '\t' + rline)
        sys.stdout.flush()



