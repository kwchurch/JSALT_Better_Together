#!/usr/bin/env python

import numpy as np
import sys,json,requests,os
from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
model = AutoModel.from_pretrained('allenai/specter')

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

for line in sys.stdin:
    my_id = id_ify(line.rstrip())

    j = requests.get('https://api.semanticscholar.org/graph/v1/paper/' + my_id + '?fields=title,abstract,embedding',
                     headers={"x-api-key": apikey}).json()
    print(my_id)
    if not 'title' in j:
        print('CANNOT FIND TITLE: ' + str(j))
    else:
        print('TITLE: ' + (j['title'] or ''))
        print('ABSTRACT: ' + (j['abstract'] or ''))

    if 'embedding' in j:
        embeddings_from_api = np.array(j['embedding']['vector']).reshape(1,-1)
        
        title_abs = [j['title'] + tokenizer.sep_token + (j.get('abstract') or '')]
        inputs = tokenizer(title_abs, padding=True, truncation=True, return_tensors="pt", max_length=512)
        result = model(**inputs)
        embeddings_from_model = result.last_hidden_state[:, 0, :].detach().numpy()

        print('EMBEDDING_MODEL: ' + str(j['embedding']['model']))
        print('SCORE: ' + str(cosine_similarity(embeddings_from_api, embeddings_from_model)[0][0]))

    else:
        print('DID NOT FIND EMBEDDING')
    
    print('')
    sys.stdout.flush()


