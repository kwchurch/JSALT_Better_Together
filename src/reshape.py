#!/usr/bin/env python

import sys
import numpy as np

x = np.loadtxt(sys.stdin, dtype=str)
y = x.reshape(int(sys.argv[1]), int(sys.argv[2]))
np.savetxt(sys.stdout, y.T, fmt='%s')
