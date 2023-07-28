#!/usr/bin/env python

import os
import sys
import argparse
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="a filename", default=None)
parser.add_argument("-o", "--output", help="output file", required=True)
parser.add_argument("-M", "--model", help="name of HuggingFace model such as allenai/specter, allenai/specter2, michiyasunaga/LinkBERT-large or malteos/scincl", 
                    default='allenai/specter2')
parser.add_argument("-b", "--batch_size", help="batch size for inference", 
                    default=16, type=int)
args = parser.parse_args()

# get gpu context if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModel.from_pretrained(args.model)

model.to(device)

errors=0

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

if slurm is None:
    inf = args.input
    outf = args.output
else:
    inf = args.input % int(slurm)
    outf = args.output % int(slurm)

if inf is None:
    infd = sys.stdin
else:
    infd = open(inf, 'r')

if os.path.exists(outf + '.kwc.nodes.i'):
    print(outf + ' : is already done', file=sys.stderr)
    sys.exit()

nodefile = open(outf + '.kwc.nodes.i', 'wb')
edgefile = open(outf + '.kwc.edges.f', 'wb')

def embed_string(s):
    inputs = tokenizer(s, padding=True, truncation=True, return_tensors="pt", max_length=64).to(device)
    result = model(**inputs)
    # take the first token in the batch as the embedding
    embeddings = result.last_hidden_state[:, 0, :]
    return embeddings.detach().cpu().numpy().reshape(-1).astype(np.float32)

def process_batch(sents, cs):
    batch_errors = 0
    try:
        esents = embed_string(sents)
    except Exception as e:
        print(e)
        batch_errors += len(sents)
        esents = None
    if esents:
        for esent, c in zip(esent, c):
            cited = np.array(int(fields[0]), dtype=np.int32)
            cited.tofile(nodefile)
            esent.tofile(edgefile)
    return(batch_errors)
         
sents = []
cs = []
for line in infd:
    rline = line.rstrip()
    fields = rline.split('\t')
    sents.append(' '.join(fields[1:]))
    cs.append(int(fields[0]))
    if len(sents) >= args.batch_size:
        errors += process_batch(sents, cs) 
        sents, cs = [], []
errors += process_batch(sents, cs)
print(str(errors) + ' errors', file=sys.stderr)
