#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

from scipy.sparse import load_npz, save_npz
import sys,argparse,time,os,socket

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
args = parser.parse_args()

G = load_npz(args.input_graph)
G += G.T

save_npz(args.output, G)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()

