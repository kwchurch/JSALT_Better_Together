#!/usr/bin/env python

import numpy as np
import sys,os
from sklearn.preprocessing import normalize

inf=sys.argv[1]
outf=sys.argv[2]

x = np.load(inf)
np.save(outf, normalize(x['embeddings']))
