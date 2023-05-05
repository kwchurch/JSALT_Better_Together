#!/usr/bin/env python

import numba
print('number of threads: ' + str(numba.core.config.NUMBA_NUM_THREADS))
