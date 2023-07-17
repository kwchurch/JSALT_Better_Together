#!/usr/bin/env python
# coding: utf-8

# In[21]:


import urllib
import os
import requests
import json

from collections import defaultdict, namedtuple
import urllib.request

import numpy as np
import pandas as pd
import joblib

from tqdm import tqdm


# ## Now run experiment

# In[22]:


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

# In[23]:


d = '/data3/jsalt2023/semantic_scholar/embeddings/proposed'

config = directory_to_config(d)

map0 = config['map']
emb0 = config['embedding']


# In[24]:


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
    


# In[25]:


idx2emb = {}


# In[26]:


for semscho_corpusidx in [3051291,3]:
    try:
        paper_emb = emb0[map0[semscho_corpusidx]]
        idx2emb[semscho_corpusidx] = np.array(paper_emb)
    except:
        print(f'failed with {semscho_corpusidx}')


# In[27]:


joblib.dump(idx2emb, 'output_embeddings')


# In[ ]:


idx2emb = joblib.load('output_embeddings')

