#!/usr/bin/env python

import sys
import numpy as np

p = np.random.choice(int(sys.argv[1]), size=int(sys.argv[2]), replace=False)
p.tofile(sys.argv[3])


