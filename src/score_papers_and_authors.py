#!/usr/bin/env python

# input: authors
# output: papers 

import numpy as np
import sys,json,requests,os,argparse
from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
parser.add_argument("--papers", help="comma separated ids", required=True)
parser.add_argument("--authors", help="comma separated ids", required=True)
parser.add_argument("--embeddings_per_author", type=int, help="defaults to 10 ", default=10)
args = parser.parse_args()

def get_paper_embedding(p):
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/CorpusId:' + str(p) + '/?fields=embedding'
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if 'embedding' in j:
        return j['embedding']['vector']


def papers_and_embeddings(papers, embeddings):
    papers2 = [ p for p,e in zip(papers,embeddings) if not e is None]
    embeddings2 = [ e for c,e in zip(papers,embeddings) if not e is None]
    return papers2, embeddings2
    
def get_author_embeddings(a, nbest):
    cmd = 'https://api.semanticscholar.org/graph/v1/author/' + str(a) + '/?fields=name,papers,papers.citationCount,papers.externalIds'
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    candidates = sorted([ (p['externalIds']['CorpusId'], p['citationCount']) for p in j['papers'] if 'externalIds' in p], key= lambda pair: pair[1], reverse=True)
    if len(candidates) > nbest:
        candidates = candidates[0:nbest]

    C = [p for p,citations in candidates]

    embeddings = [get_paper_embedding(p) for p in C]
    return papers_and_embeddings(C,embeddings)

P = args.papers.split(',')
E = [get_paper_embedding(p) for p in P]

P2,E2 = papers_and_embeddings(P,E)

A = []
AE = []

for a in args.authors.split(','):
    pairs = get_author_embeddings(a, args.embeddings_per_author)
    A += pairs[0]
    AE += pairs[1]

# scores = cosine_similarity(np.array(E2), np.array(AE))
scores = cosine_similarity(np.array(AE))

for i,pi in enumerate(A):
    for j,pj in enumerate(A):
        if i < j:
            print('\t'.join(map(str, [pi, pj, scores[i,j]])))

