#!/usr/bin/env python

import sys
import numpy as np

p = np.random.permutation(int(sys.argv[1]))
p.tofile(sys.argv[2])
