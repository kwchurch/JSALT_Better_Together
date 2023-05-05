#!/usr/bin/env python

import numpy as np
import sys,time

t0 = time.time()

for line in sys.stdin:
    fields = np.fromstring(line, sep=' ')
    if len(fields) < 3: continue
    # word = fields[0]
    vlen = np.linalg.norm(fields[1:])
    if vlen > 1e-10: 
        print(line.rstrip())
        # print(str(int(word)) + '\t' + str(vlen))

print(str(time.time() - t0) + ' done', file=sys.stderr)
