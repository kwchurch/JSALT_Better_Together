#!/usr/bin/env python

import numpy as np
import sys,argparse,time,json
# import gensim,sys,argparse,time
# from gensim.models import KeyedVectors
# from sklearn.metrics.pairwise import cosine_similarity

t0 = time.time()

parser = argparse.ArgumentParser()
# default='/mnt/big/kwc/morphology/embedding_comparisons/annoys.txt'
parser.add_argument("-i", "--input", help="a filename", default=None)
parser.add_argument("-o", "--output", help="a filename", default=None)
# parser.add_argument("-M", "--embedding", help="a filename", required=True)
# parser.add_argument("-N", "--topn", type=int, help="topn [defaults = 10]", default=10)
# parser.add_argument("-q", "--query_mode", help="binary_vectors|vectors|terms|pairs|self|pairwise_terms [default = vectors]", default='vectors')
# parser.add_argument("-r", "--random", type=int, help="number of outputs to compute (only for query_mode of self) [default = -1 (use all)]", default=-1)
# parser.add_argument("-m", "--map_node_names", help="map node names", default=None)
# parser.add_argument("-p", "--prefix", help="prefix before each node name", default=None)
args = parser.parse_args()

from transformers import AutoTokenizer, AutoModel

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
model = AutoModel.from_pretrained('allenai/specter')

# papers = [{'title': 'BERT', 'abstract': 'We introduce a new language representation model called BERT'},
#          {'title': 'Attention is all you need', 'abstract': ' The dominant sequence transduction models are based on complex recurrent or convolutional neural networks'}]

if args.input.endswith('.json'):
    with open(args.input, 'r') as fd:
        papers = json.loads(fd.read())
else:
    papers = []
    with open(args.input, 'r') as fd:
        for line in fd:
            fields = line.strip().split('\t')
            if len(fields) >= 2:
                title,abstract = fields[0:2]
                papers.append({"title" : title, "abstract" : abstract})

# import pdb
# pdb.set_trace()

# concatenate title and abstract
title_abs = [d['title'] + tokenizer.sep_token + (d.get('abstract') or '') for d in papers]
# preprocess the input
inputs = tokenizer(title_abs, padding=True, truncation=True, return_tensors="pt", max_length=512)
result = model(**inputs)
# take the first token in the batch as the embedding
embeddings = result.last_hidden_state[:, 0, :].detach().numpy()

np.save(args.output, embeddings)


