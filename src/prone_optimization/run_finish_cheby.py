#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

import scipy
from scipy import sparse, linalg, special
from sklearn import preprocessing
import numpy as np
from scipy.sparse import load_npz, csr_matrix, save_npz
import os,sys,argparse,time,gc,socket

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import finish_npfloat16 as finish
import cheby_npfloat16 as cheby


if __name__=="__main__":
    print('ProNE_chebyshev: sys.argv = ' + str(sys.argv))
    t0 = time.time()
    print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (
    socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')))
    sys.stderr.flush()
    parser = argparse.ArgumentParser()
    parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", required=True)
    parser.add_argument("-U", "--U", help="input prefactorization", default=None)
    parser.add_argument("--temp_file_prefix", help="input prefactorization", default=None)
    parser.add_argument("--iteration", type=int, help="typically a number from 0 to 10", required=True)
    parser.add_argument("--mu", type=float, help="damping factor (defaults to 0.2)", default=0.2)
    parser.add_argument("--theta", type=float, help="bessel function parameter (defaults to 0.5)", default=0.5)
    parser.add_argument("-O", "--output", help="output file", required=True)
    args = parser.parse_args()
    sys.stderr.flush()
    i = args.iteration
    if(i == 0):
        Lx0, Lx1, conv, U, G = cheby.first_iter(i, args.temp_file_prefix, args.theta, t0, args.U, args.input_graph, args.mu)
        print('%0.2f sec: about to save files' % (time.time() - t0))
        cheby.save_files(args.iteration, Lx0, Lx1, conv, t0, args.temp_file_prefix)
        # this doesn't delete them from where they are stored?
        del Lx0
        del Lx1
    else:
        Lx0, Lx1, conv, G = cheby.subsequent_iteration(i, args.temp_file_prefix, args.theta, t0, args.input_graph, args.mu)
        print('%0.2f sec: about to save files' % (time.time() - t0))
        cheby.save_files(args.iteration, Lx0, Lx1, conv, t0, args.temp_file_prefix)
        del Lx0
        del Lx1
        U = np.load(args.U).astype(np.float32)
    print('Finished the chebyshev iteration in %0.2f sec' % (time.time() - t0))     
    finish.finish(G, U, t0, conv, args.output, args.iteration)
