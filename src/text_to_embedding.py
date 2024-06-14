#!/usr/bin/env python

from transformers import AutoTokenizer, AutoModel
import sys,os,argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="a filename", default=None)
parser.add_argument("-o", "--output", help="output file", required=True)
parser.add_argument("-M", "--model", help="name of HuggingFace model such as allenai/specter, allenai/specter2, michiyasunaga/LinkBERT-large or malteos/scincl", 
                    default='allenai/specter2')
args = parser.parse_args()

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModel.from_pretrained(args.model)

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
    inputs = tokenizer(s, padding=True, truncation=True, return_tensors="pt", max_length=512)
    result = model(**inputs)
    # take the first token in the batch as the embedding
    embeddings = result.last_hidden_state[:, 0, :]
    return embeddings.detach().numpy().reshape(-1).astype(np.float32)

for line in infd:
    rline = line.rstrip()
    fields = rline.split('\t')
    # if len(fields) < 2: continue
    try:
        e = embed_string(' '.join(fields[1:]))
        cited = np.array(int(fields[0]), dtype=np.int32)
        cited.tofile(nodefile)
        e.tofile(edgefile)
    except:
        errors = errors+1

print(str(errors) + ' errors', file=sys.stderr)
