#!/usr/bin/env python

import numpy as np
import sys,json,requests,os
from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')
errors=0

# from transformers import AutoTokenizer, AutoModel
# tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
# model = AutoModel.from_pretrained('allenai/specter')

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def embeddings(papers):
    res = []
    ids = []
    for p in papers:
        if not p is None:
            j = requests.get('https://api.semanticscholar.org/graph/v1/paper/' + p + '?fields=embedding',
                             headers={"x-api-key": apikey}).json()
            if 'embedding' in j:
                if 'vector' in j['embedding']:
                    ids.append(p)
                    res.append(j['embedding']['vector'])
    return ids,np.array(res).reshape(-1,768)    

np.set_printoptions(linewidth=200, precision=3)

api='https://api.semanticscholar.org/graph/v1/paper/'
# api='https://github.com/allenai/paper-embedding-public-apis'

fields = ','.join(sys.argv[1:])
for line in sys.stdin:
    for field in line.rstrip().split('|'):
        my_id = id_ify(field)

        try: 
            j = requests.get(api + str(my_id) + '?fields=embedding,references,citations',
                             headers={"x-api-key": apikey}).json()

            embedding = np.array(j['embedding']['vector']).reshape(1,-1)

            # print('references:')
            # pprint.pprint(j['references'])

            rids,references = embeddings([p['paperId'] for p in j['references']])
            cids,citations = embeddings([p['paperId'] for p in j['citations']])

            # print('id: ' + str(my_id))
            # print('references: ' ', '.join(rids))
            # print('citations: ' ', '.join(cids))

            if len(rids) > 0:
                for rid,sim in zip(rids, cosine_similarity(embedding, references)[0]):
                    print('\t'.join([my_id, rid, str(sim), 'reference']))

            if len(cids) > 0:
                for cid,sim in zip(cids, cosine_similarity(embedding, citations)[0]):
                    print('\t'.join([my_id, cid, str(sim), 'citation']))
        except:
            errors += 1

        # print('')
        sys.stdout.flush()


print(str(errors) + ' errors', file=sys.stderr)
