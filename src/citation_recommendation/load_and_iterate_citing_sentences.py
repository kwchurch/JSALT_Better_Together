#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os

from tqdm import tqdm


# ### Set file path - assumes a subfolder e.g. citing_sentences/pieces/[0-9]{3}

# In[ ]:


#os.environ['citing_sentences'] = '/data3/jsalt2023/semantic_scholar/releases/2022-12-02/database/citations/citing_sentences/pieces/000'



# ### Helper functions

# In[ ]:


def get_embedding_list(path):
    dir_list = os.listdir(path)
    embedding_list = [e.split('.')[0] for e in dir_list if e.split('.')[0]+'.kwc.edges.f' in dir_list
                                                        and e.split('.')[0]+'.kwc.nodes.i' in dir_list]
    embedding_list = list(sorted(set(embedding_list)))
    return(embedding_list)


def citation_embedding_from_dir(fn, K):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')


# In[ ]:


def load_citing_sentence_maps(path):
    embeding_list = get_embedding_list(path)
    memory_map_list = []
    for embeddings_id in tqdm(embeding_list):
        nmap = np.memmap(os.path.join(path, embeddings_id+'.kwc.nodes.i'), 
                    dtype=np.int32, shape=(int(8000)), mode='r')
        cembs = citation_embedding_from_dir(os.path.join(path, embeddings_id+'.kwc.edges.f'), 
                                           768)
        
        #assert nmap.shape[0] == cembs.shape[0], f'error loading {os.path.join(path, embeddings_id)}'
        memory_map_list.append((nmap, cembs))
    return(memory_map_list)


# In[ ]:


citing_sentences = os.environ.get('citing_sentences')


# In[ ]:


mmaps = load_citing_sentence_maps(citing_sentences)


# ### Define iterator for mmaps chunks

# In[ ]:


def chunks(specter_citing_sentences, n):
    offset = 0
    
    for i in range(len(specter_citing_sentences)):
        for j in range(0, specter_citing_sentences[i][0].shape[0], n):
            
            this_array_yeild_nmap = specter_citing_sentences[i][0][offset+j:offset+j + n]
            this_array_yeild_cembs = specter_citing_sentences[i][1][offset+j:offset+j + n]
            
            if this_array_yeild_nmap.shape[0] < n and i < len(specter_citing_sentences) - 1:
                
                
                next_array_yeild_nmap = specter_citing_sentences[i+1][0][0:n-this_array_yeild_nmap.shape[0]]
                next_array_yeild_cembs = specter_citing_sentences[i+1][1][0:n-this_array_yeild_cembs.shape[0]]
                
                offset = n-next_array_yeild_nmap.shape[0]
                yield (np.concatenate((this_array_yeild_nmap, next_array_yeild_nmap), axis=0),
                       np.concatenate((this_array_yeild_cembs, next_array_yeild_cembs), axis=0)) 
                
                
            else:
                offset = 0
                yield (this_array_yeild_nmap,  this_array_yeild_cembs)


# In[ ]:


iterator = chunks(mmaps, 1024)


# In[ ]:


next(iterator)


# In[ ]:


## Load text, not needed
text_path = os.environ.get('embedding_text_path')
f = open(embedding_text_path, 'r', encoding='utf8')
rl = f.readlines()
lines_to_semscho_corpusids = {}
ids = []
texts = []
for l in  rl:
    ids.append(l.split('\t')[0])
    texts.append(l.split('\t')[1])
df = pd.DataFrame(data=zip(ids, texts))
    


# In[ ]:




