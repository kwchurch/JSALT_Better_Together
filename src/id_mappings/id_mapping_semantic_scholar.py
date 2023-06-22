#!/usr/bin/env python
# coding: utf-8

# ## ID Mappings
# 
# Code to map IDs to SemScho IDs in a sqlite3 db
# 
# Requires $SEMSCHO bash variable to be set and pointing to globus_sync/semantic_scholar

# In[ ]:


import json
import gzip
import os
from multiprocessing.pool import ThreadPool
import pandas as pd
from tqdm import tqdm
import sqlite3


# ### dump files

# In[ ]:


def dump_from_x_to_y(file_path, k, n, length, dump_loc):
    # dump lines from k/n to k+1/n
    
    start = k * length // n
    end = (k + 1) * length // n

    with open(dump_loc+'/'+file_path.split('/')[-1]+'dumped'+f'_{k+1}_of_{n}'+'.txt', 'w', encoding='utf-8') as out_file:
        with gzip.open(file_path, 'rt') as in_file:

            for line_num, line in enumerate(in_file):
                if line_num < start:
                    continue
                elif line_num >= end:
                    break
                else:
                    datum = json.loads(line)
                    all_ids =  datum['externalids']
                    all_ids = {k:v for k,v in all_ids.items() if v}
                    all_maps = [(k.upper()+':'+v, all_ids['CorpusId']) for k,v in all_ids.items() if k != 'CorpusId']

                    for k,v in all_maps:
                        out_file.write(k+'<@@@>'+v+'\n')


# In[ ]:


#os.environ['SEMSCHO'] = '/data3/jsalt2023/semantic_scholar/'


# In[ ]:


path = os.path.join(os.environ.get('SEMSCHO'), 'releases/2023-05-09/database/papers/')
tmp_txt_path = os.path.join(os.environ.get('SEMSCHO'), 'p.vickers/tmp/')
os.makedirs(tmp_txt_path, exist_ok=True) 

# Get sorted list of paths CORE .json.xz files
files = [f for f in os.listdir(path) if f.endswith('.gz')]
files.sort(key=lambda x: x.split('.')[0])
files = [os.path.join(path, f) for f in files]
files = sorted(files)

for file in tqdm(files[1:]):
    dump_from_x_to_y(file, 0, 1, int(10e10), tmp_txt_path)


# ### now load into sqlite database

# In[ ]:


# Get sorted list of paths CORE .json.xz files
files = [f for f in os.listdir(tmp_txt_path) if f.endswith('.txt')]
files.sort(key=lambda x: x.split('.')[0])
files = [os.path.join(tmp_txt_path, f) for f in files]
files = sorted(files)


# In[ ]:


get_ipython().system('rm /data3/jsalt2023/semantic_scholar/p.vickers/id_mappings/*')


# In[ ]:


db_path


# In[ ]:


db_path = os.path.join(os.environ.get('SEMSCHO'), 'p.vickers/id_mappings')
os.makedirs(db_path, exist_ok=True) 


db = sqlite3.connect(os.path.join(db_path, 'semscho_map.sql'))

db.execute('''CREATE TABLE SEMSCHOIDS
         (NONSEMSCHOID TEXT      NOT NULL,
         SEMSCHOID           INT    NOT NULL);
          ''')
c = db.cursor()


# In[ ]:


for file in tqdm(files):
    df = pd.read_csv(file, sep='<@@@>', header=None, engine='python')
    c.executemany('INSERT INTO SEMSCHOIDS VALUES (?, ?)', (df.dropna().values))


# In[ ]:


db.commit()


# In[ ]:


db.execute("CREATE INDEX nonsemschoid_hash_index ON SEMSCHOIDS(NONSEMSCHOID)")


# In[ ]:


db.commit()
db.close()


# ###  resolve IDs with multiple threads

# In[81]:


class semscho_id_resolver():
    def __init__(self, db_path=''):
        self.db_path = db_path

    def __getitem__(self, query_id):
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA synchronous = OFF')
        cursor = conn.execute("SELECT SEMSCHOID from SEMSCHOIDS WHERE NONSEMSCHOID == (?)", (query_id,))
        for row in cursor:
            if row:
                return row[0]
            else:
                return None


# In[82]:


def get_paper_by_ids(ids, prefix=''):
    ids_prefixed = [prefix+str(i) for i in ids]    
    pool = ThreadPool(processes=os.cpu_count()*4)
    semanticScholarIDs = pool.map(resolver.__getitem__, ids_prefixed)
    return(semanticScholarIDs)


# In[83]:


resolver = semscho_id_resolver(os.path.join(db_path, 'semscho_map.sql'))


# In[84]:


get_paper_by_ids([2078170666, 2590133163, 1990210098], prefix='MAG:')

