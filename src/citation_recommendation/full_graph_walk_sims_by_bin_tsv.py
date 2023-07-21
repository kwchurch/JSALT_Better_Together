import pandas as pd
from collections import defaultdict
from random import random
from tqdm import tqdm
import joblib
import numpy as np
from numpy.linalg import norm
import os

walk_path = os.path.join(os.environ.get('JSALTdir'), 'semantic_scholar/eval/walk_with_bins')

df = pd.read_csv(walk_path, sep='\t', header=None)

a1_hop_filter = df[0] == 1

a1_hop_df = df[a1_hop_filter]

a2_to_4_hop_df = df[~a1_hop_filter]

def get_emb_sims(id0, id1):
    a = emb0[map0[id0]] 
    b = emb0[map0[id1]]
    cos_sim = np.dot(a, b)/(norm(a)*norm(b))
    return cos_sim

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


# added by kwc
proposed = os.environ.get('proposed')

inputs = [proposed]

configs = [directory_to_config(d) for d in inputs]

map0 = configs[0]['map']
emb0 = configs[0]['embedding']


def get_sims_by_bin(walk_df, agg='min'):
        i = 0
        bin_to_sim = defaultdict(list)
        for _, row in tqdm(walk_df.iterrows(), total=len(walk_df)):
            try:
                id0, id1, bin0, bin1 = int(row[1]), int(row[2]), int(row[3]), int(row[4])
                if agg == 'min':
                    bin_agg = min(bin0, bin1)
                elif agg == 'mean':
                    bin_agg = round((bin0+bin1)/2)
                elif agg == 'max':
                    bin_agg = min(bin0, bin1)
                else:
                    raise AggNotImplementedError
                if bin_agg in [10,30,50,70,90]:
                    sim = get_emb_sims(id0, id1)
                    bin_to_sim[bin_agg].append([id0, id1, sim])
                    i += 1
            except Exception as e:
                bin_to_sim[bin_agg].append([id0, id1, -2])
        return(bin_to_sim)
	
a1_hop_sims = get_sims_by_bin(a1_hop_df, agg='min')
to_tsv = []
for bin_id in a1_hop_sims:
    for sample in a1_hop_sims[bin_id]:
        print(sample, bin_id)
        to_tsv.append(sample+[bin_id])
df = pd.DataFrame(to_tsv, columns = ['id0', 'id1', 'cos_sim', 'min_bin'])
df.to_csv('binned_1_hop_sims.tsv', sep='\t')


