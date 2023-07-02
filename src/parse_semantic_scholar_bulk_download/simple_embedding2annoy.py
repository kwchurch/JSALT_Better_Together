#!/usr/bin/env python

import numpy as np
import gensim
import sys,time

binary=False

t0 = time.time()

for f in sys.argv[1:]:
    if f == '--binary':
        binary=True
        continue
    C=gensim.models.KeyedVectors.load_word2vec_format(f, binary=binary)
    C.save(f + '.annoy')
    print(str(time.time() - t0) + ': finished ' + f, file=sys.stderr)



