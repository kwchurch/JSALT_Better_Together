#!/usr/bin/env python

from transformers import AutoTokenizer, AutoModel
import sys,json,gzip,os,argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="a filename", default='citations.piece.%03d.gz')
parser.add_argument("-o", "--output", help="output file", default='citations.piece.%03d')
args = parser.parse_args()

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
model = AutoModel.from_pretrained('allenai/specter')


errors=0

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

if slurm is None:
    inf = args.input
    outf = args.output
else:
    inf = args.input % int(slurm)
    outf = args.output % int(slurm)

# if outf == '-':
#     out_fd = sys.stdout
# else:
#     out_fd = open(outf, 'w')

nodefile = open(outf + '.kwc.nodes.i', 'wb')
edgefile = open(outf + '.kwc.edges.f', 'wb')

def embed_string(s):
    inputs = tokenizer(s, padding=True, truncation=True, return_tensors="pt", max_length=512)
    result = model(**inputs)
    # take the first token in the batch as the embedding
    embeddings = result.last_hidden_state[:, 0, :]
    return embeddings.detach().numpy().reshape(-1).astype(np.float32)
    
# print('hindex\tpapercount\tcitationcount\tauthorid\tname', file=out_fd)

with gzip.open(inf) as in_fd:
    for line in in_fd:
        rline = line.rstrip()
        j = json.loads(rline)
        if not 'contexts' in j or not 'citedcorpusid' in j: continue

        contexts = j['contexts']
        cited  = j['citedcorpusid']

        if contexts is None or cited is None: continue

        cited = np.array(cited, dtype=np.int32)

        for c in contexts:
            cited.tofile(nodefile)
            e = embed_string(c)
            e.tofile(edgefile)


