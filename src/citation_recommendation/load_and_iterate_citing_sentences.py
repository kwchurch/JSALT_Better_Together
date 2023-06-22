#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from collections import defaultdict, namedtuple

import numpy as np
import pandas as pd

from tqdm import tqdm


# In[ ]:


#os.environ['citing_sentences'] = '/data3/jsalt2023/semantic_scholar/releases/2022-12-02/database/citations/citing_sentences/pieces'


# In[ ]:


# This should be GLOBUS_DOWNLOAD_PATH/semantic_scholar/releases/2022-12-02/database/citations/citing_sentences/pieces
citing_sentences = os.environ.get('citing_sentences')

semscho_corpus_ids_to_find = [205376417, 4854301, 9198465, 4310181, 467287]


# ### Helper functions

# In[ ]:


# Get list of all embeddings in subfolders
def get_embedding_list(path):
    embedding_list = []
    
    piece_folder_list = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    for piece_folder in piece_folder_list:
        piece_subfolder_list = os.listdir(os.path.join(path, piece_folder))
        subfolder_embedding_list = [e.split('.')[0] for e in piece_subfolder_list \
                                    if e.split('.')[0]+'.kwc.edges.f' in piece_subfolder_list
                                    and e.split('.')[0]+'.kwc.nodes.i' in piece_subfolder_list
                                    and 'citing_sentences' not in e]
                                                            
        embedding_list.extend([(piece_folder, p) for p in sorted(set(subfolder_embedding_list))])
    return embedding_list

# Load memory-mapped corpus_ids
def citation_embedding_from_dir(fn, K):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

# Load memory-mapped embeddings
def load_citing_sentence_maps(path, K):
    embeding_list = get_embedding_list(path)
    for piece_folder, embeddings_id in embeding_list:
        nmap = np.memmap(os.path.join(path, piece_folder, embeddings_id+'.kwc.nodes.i'), 
                         dtype=np.int32, shape=(int(8000)), mode='r')
        cembs = citation_embedding_from_dir(os.path.join(path, piece_folder, embeddings_id+'.kwc.edges.f'), 
                                           K)
        sent_ids = [os.path.join(piece_folder, embeddings_id)+'_'+str(idx) for idx in range(8000)]
        
        #assert nmap.shape[0] == cembs.shape[0], f'error loading {os.path.join(path, embeddings_id)}'
        yield (nmap, cembs, sent_ids)


# In[ ]:


Result = namedtuple("Result", "emb text")

def get_text_from_path_and_ids(path, use_ids):
    use_ids_to_text = {}
    # only load text file if we have ids to retrieve
    if use_ids:
        with open(path, 'r', encoding='utf-8') as fp:
            for i, line in enumerate(fp):
                if i in set(use_ids):
                    use_ids_to_text['/'.join(path.split('/')[-2:])+'_'+str(i)] = line
    return(use_ids_to_text)

def build_citing_sentence_embedding_text_dict(semscho_corpus_ids_to_find, embedding_iterator, length=0):
    '''
    returns a dict mapping semantic scholar corpus ids to sentence embeddings and text
    inputs:
    semscho_corpus_ids_to_find : list of semantic scholar corpus ids to find
    embedding_iterator : iterator which yields semantic scholar corpus ids and matched citing sentence embeddings
    '''
    semscho_corpus_ids_to_cs_embs = defaultdict(list)
    for corpus_ids, embs, text_id in tqdm(embedding_iterator, total=length):
        use_ids = [(idx, corpid) for idx, corpid in enumerate(corpus_ids) if corpid in semscho_corpus_ids_to_find]

        use_ids_to_text = get_text_from_path_and_ids(os.path.join(citing_sentences,
                                                                  text_id[0].split('/')[0],
                                                                  text_id[0].split('/')[1].split('_')[0]),
                                                     [idx for idx, corpid in use_ids])
        
        for idx, corpid in use_ids:
            semscho_corpus_ids_to_cs_embs[corpid].append(Result(np.array(embs[idx]), use_ids_to_text[text_id[idx]]))
        
    return dict(semscho_corpus_ids_to_cs_embs)


# In[ ]:


mmaps = load_citing_sentence_maps(citing_sentences, K=768)


# In[ ]:


semscho_corpus_ids_to_embs_text = build_citing_sentence_embedding_text_dict(semscho_corpus_ids_to_find=semscho_corpus_ids_to_find,
                                                                            embedding_iterator=mmaps,
                                                                            length=0)

