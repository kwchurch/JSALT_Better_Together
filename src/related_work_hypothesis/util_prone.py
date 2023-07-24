
import numpy as np
import os


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


def get_vector_prone(idx,configs):
    use_map = configs['map']
    use_emb = configs['embedding']
    try:
        paper_emb = use_emb[use_map[int(idx)]]
    except:
        print(f'failed with {int(idx)}')
    return np.array(paper_emb)