#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib
import os
import requests
import json

from collections import defaultdict, namedtuple
import urllib.request

import numpy as np
import pandas as pd

from tqdm import tqdm


# ## Get dataset

# In[ ]:


urllib.request.urlretrieve('https://bert-gcn-for-paper-citation.s3.ap-northeast-2.amazonaws.com/PeerRead/full_context_PeerRead.csv',
                           'full_context_PeerRead.csv')


# In[ ]:


df = pd.read_csv('full_context_PeerRead.csv')


# ## Resolve arXiv ids to Sem Scho Corpus IDs

# In[ ]:


PeerRead_to_SemanticScholar_Ids = defaultdict(lambda: [None, None])


# In[ ]:


def get_paper_by_ids(ids):
    r = requests.post(
        'https://api.semanticscholar.org/graph/v1/paper/batch',
        params={'fields': 'referenceCount,citationCount,title,corpusId'},
        json={"ids": ids}
    )
    
    assert len(r.json()) == len(ids)
    
    semanticScholarIDs = [x["corpusId"] if isinstance(x, dict) else None for x in r.json()]

    return(semanticScholarIDs)


# In[ ]:


# Map source papers to Corpus Ids
for i in tqdm(range(0, len(df), 500), total=len(df)//500+1):

    ids = ['ARXIV:'+x.replace('v1', '') for x in df['source_id'].iloc[i:i+500].tolist()]

    semanticScholarIDs = get_paper_by_ids(ids)
    for j in range(0, len(ids), 1):
        PeerRead_to_SemanticScholar_Ids[i+j][0] = semanticScholarIDs[j]


# In[ ]:


# Map target papers to Corpus Ids
for i in tqdm(range(0, len(df), 500), total=len(df)//500+1):

    ids = ['ARXIV:'+x.replace('v1', '') for x in df['target_id'].iloc[i:i+500].tolist()]

    semanticScholarIDs = get_paper_by_ids(ids)
    for j in range(0, len(ids), 1):
        PeerRead_to_SemanticScholar_Ids[i+j][1] = semanticScholarIDs[j]


# In[ ]:


# Add to df
srcSemanticScholarIds = [x[0] for x in PeerRead_to_SemanticScholar_Ids.values()]
tgtSemanticScholarIds = [x[1] for x in PeerRead_to_SemanticScholar_Ids.values()]

df['source_semscho_id'] = srcSemanticScholarIds
df['target_semscho_id'] = tgtSemanticScholarIds


# ## Search any unmapped papers by title

# In[ ]:


missedsrc_idx_to_name = {}
for idx, x in df[['source_title', 'source_semscho_id']].iterrows():
    if isinstance(x['source_semscho_id'], float) and np.isnan(x['source_semscho_id']):
        missedsrc_idx_to_name[idx] = x['source_title']
    
        
missedtgt_idx_to_name = {}

for idx, x in df[['target_title', 'target_semscho_id']].iterrows():
    if isinstance(x['target_semscho_id'], float) and np.isnan(x['target_semscho_id']):
        missedtgt_idx_to_name[idx] = x['target_title']


# In[ ]:


unique_missed_src = set(missedsrc_idx_to_name.values())
unique_missed_tgt = set(missedtgt_idx_to_name.values())
unique_missed_all = sorted(list(unique_missed_src.union(unique_missed_tgt)))
missed_name_to_semid = {}


# In[ ]:


def get_paper_by_name(paper_name):
    url = 'https://api.semanticscholar.org/graph/v1/paper/search?query='
    q_name = paper_name.replace('-', ' ')
    fields = q_name.rstrip().split('\t')
    suffix = '\t' + '\t'.join(fields)
    cmd = url + urllib.parse.quote(fields[0]) + '&limit=1'
    j = requests.get(cmd).json()
    return(j)
    
for name in tqdm([name for name in unique_missed_all if name not in missed_name_to_semid]):
    if name in missed_name_to_semid:
        continue
    
    while True:
        j = get_paper_by_name(name)
        
        if 'data' in j and j['data']:
            missed_name_to_semid[name] = j['data'][0]['paperId']
            break
            
        elif 'code' in j and j['code'] == '429':
            pass
        
        else:
            print(f'Failed to find Sem Scho mapping for {name}')
            break


# ## Sem Scho name search gives us ids, but we need CorpusIDs

# In[ ]:


semhashes_to_resolve = list(missed_name_to_semid.values())
semhashs_to_resolve_to_semids = {}

for i in tqdm(range(0, len(semhashes_to_resolve), 100), total=len(semhashes_to_resolve)//100+1):

    ids = [x for x in semhashes_to_resolve[i:i+100]]
    
    semanticScholarIDs = get_paper_by_ids(ids)
    for j in range(0, len(ids), 1):
        semhashs_to_resolve_to_semids[ids[j]] = semanticScholarIDs[j]


# In[ ]:


for idx in missedsrc_idx_to_name:
    df.iloc[idx, df.columns.get_loc('source_semscho_id')] = semhashs_to_resolve_to_semids[missed_name_to_semid[missedsrc_idx_to_name[idx]]]

for idx in missedtgt_idx_to_name:
    df.iloc[idx, df.columns.get_loc('target_semscho_id')] = semhashs_to_resolve_to_semids[missed_name_to_semid[missedtgt_idx_to_name[idx]]]


# In[ ]:


df = df.astype({'source_year': 'int32', 'source_semscho_id': 'int32', 'target_semscho_id': 'int32'})


# In[ ]:


assert ~df.isnull().values.any()


# ## Now run experiment

# In[ ]:


# Helpers from https://github.com/kwchurch/JSALT_Better_Together/blob/main/src/create_rotation_matrix.py

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return int(fd.read().split('\t')[0])

def map_from_dir(dir):
    fn = dir + '/map.old_to_new.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def embedding_from_dir(dir, K):
    fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : map_from_dir(dir),
             'embedding' : embedding_from_dir(dir, K)}


# ## Set paths to embeddings

# In[ ]:


specter = '/data2/jsalt2023/data/semantic_scholar/embeddings/specter'
proposed = '/data2/jsalt2023/data/semantic_scholar/embeddings/proposed'


# In[ ]:


inputs = specter, proposed

configs = [directory_to_config(d) for d in inputs]

map0 = configs[0]['map']
emb0 = configs[0]['embedding']

map1 = configs[1]['map']
emb1 = configs[1]['embedding']


# In[ ]:


def flatten(l):
    return [item for sublist in l for item in sublist]


sample = namedtuple('sample', 'src tgt')
# build a named_tuple of idx:[src, tgt]
def sem_scho_ids_to_dataset(src_to_tgt_sem_scho_ids):
    dataset = {}
    for i, (src, tgt) in enumerate(src_to_tgt_sem_scho_ids.items()):
        dataset[i] = sample(src, tgt)
    return(dataset)

small_index = namedtuple('small_index', 'index idx_to_semscho_id')
# build a small index which contains all target semscho embs normed and a mapping from the semscho_id to the index
def build_small_index(sem_sco_ids, map_, emb_):
    semscho_ids_mapped = {i:map_[i] for i in sem_sco_ids if i < len(map_)}
    semscho_ids_failed = [i for i in sem_sco_ids if i >= len(map_)]
    
    semscho_ids_to_local = {i:l for l,i in enumerate(semscho_ids_mapped.keys())}
    local_to_semscho_ids = {l:i for i,l in semscho_ids_to_local.items()}

    all_embs = [emb_[map_[local_to_semscho_ids[i]]] for i in range(len(local_to_semscho_ids))]
    all_embs_normed = np.vstack([e/np.linalg.norm(e) for e in all_embs])
    
    return small_index(all_embs_normed, local_to_semscho_ids)
    


# ## From https://arxiv.org/pdf/1903.06464.pdf , test set is >= 2017 publication date

# In[ ]:


test_df = df[df['source_year']>=2017]
src_to_tgt_sem_scho_ids = dict(zip(test_df.source_semscho_id, test_df.target_semscho_id))


# In[ ]:


for method, use_map, use_emb in (('specter', map0, emb0), ('proposed', map1, emb1)):
    dataset = sem_scho_ids_to_dataset(src_to_tgt_sem_scho_ids)
    all_tgts = [s.tgt for s in dataset.values()]
    smaller_index = build_small_index(all_tgts, use_map, use_emb)
    
    count = 0
    top_1_score = 0
    top_5_score = 0
    top_10_score = 0

    for idx, s in dataset.items():
        try:
            src_emb = use_emb[use_map[s.src]]
            src_emb_normed = src_emb/np.linalg.norm(src_emb)
            search = np.inner(smaller_index.index, src_emb_normed)
            search_top_10 = np.argpartition(search, -10)[-10:]
            search_top_10_sorted = search_top_10[np.argsort(search[search_top_10])][::-1]
            search_top_10_sorted_mapped = [smaller_index.idx_to_semscho_id[i] for i in search_top_10_sorted]

            top_1_name = df[df['target_semscho_id']==search_top_10_sorted_mapped[0]].iloc[0]['target_title']
            y_name =  df[df['target_semscho_id']==s.tgt].iloc[0]['target_title']

            top_1_score += s.tgt in search_top_10_sorted_mapped[:1]
            top_5_score += s.tgt in search_top_10_sorted_mapped[:5]
            top_10_score += s.tgt in search_top_10_sorted_mapped[:10]

            count += 1
        except:
            print('failed with id:', sample.src)
    print(f'With method {method}:')
    print(f'R@1: {round(top_1_score/count, 3)}')
    print(f'R@5: {round(top_5_score/count, 3)}')
    print(f'R@10: {round(top_10_score/count, 3)}')
    print()

