#!/usr/bin/env python

# ~/final/morphology/dict_to_embedding.py

# from nodevectors (prone.py)
# ~/venv/gft/lib/python3.8/site-packages/nodevectors/prone.py

from scipy.sparse import load_npz, save_npz
import sys,argparse,time

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
args = parser.parse_args()

G = load_npz(args.input_graph)
G += G.T

save_npz(args.output, G)

