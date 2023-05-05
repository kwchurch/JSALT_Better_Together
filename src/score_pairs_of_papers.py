#!/usr/bin/env python

# input: authors
# output: papers 

import numpy as np
import sys,json,requests,os,argparse
from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
# parser.add_argument("--papers", help="comma separated ids", required=True)
# parser.add_argument("--authors", help="comma separated ids", required=True)
# parser.add_argument("--embeddings_per_author", type=int, help="defaults to 10 ", default=10)
args = parser.parse_args()

def id_ify(s):
    if len(s) == 40:
        return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def get_paper_embedding(p):
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + str(p) + '/?fields=embedding'
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if 'embedding' in j:
        return j['embedding']['vector']


for line in sys.stdin:
    rline = line.rstrip()
    fields = rline.split()
    if len(fields) >= 2:
        p1,p2 = fields[0:2]
        e1 = get_paper_embedding(id_ify(p1))
        e2 = get_paper_embedding(id_ify(p2))
        if e1 is None or e2 is None:
            print('NA\t' + rline)
        else:
            e1 = np.array(e1).reshape(1,-1)
            e2 = np.array(e2).reshape(1,-1)
            print(str(cosine_similarity(e1,e2)[0][0]) + '\t' + rline)

        
        
        
