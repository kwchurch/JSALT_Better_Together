#!/usr/bin/env python

import sys,scipy.sparse,time

t0 = time.time()

def my_load(f):
    t0a = time.time()
    sys.stderr.flush()
    m = scipy.sparse.load_npz(f)
    GB = (m.data.nbytes + m.indices.nbytes + m.indptr.nbytes)/1e9
    t1 = time.time()
    print('%0.0f my_load: %s (%0.3f GB; %0.2f seconds; %d nonzeros)' % (t1 - t0, f, GB, t1 - t0a, m.count_nonzero()), file=sys.stderr)
    return m

M = [ my_load(f) for f in sys.argv[2:]]
print(str(time.time() - t0) + ' finished loading', file=sys.stderr)
sys.stderr.flush()

shapes = [m.shape for m in M]
new_shape = ( max( [p[0] for p in shapes]),
              max( [p[1] for p in shapes]))

print(str(time.time() - t0) + ' new_shape: ' + str(new_shape), file=sys.stderr)
sys.stderr.flush()

newM = [ m.resize(new_shape) for m in M ]

print(str(time.time() - t0) + ' finished reshaping ', file=sys.stderr)
sys.stderr.flush()

MM = max(newM)

GB = (MM.data.nbytes + MM.indices.nbytes + MM.indptr.nbytes)/1e9

print(str(time.time() - t0) + ' about to save, MM has %0.3f GB' % GB, file=sys.stderr)
sys.stderr.flush()
scipy.sparse.save_npz(sys.argv[1], MM)
