import argparse
from tqdm import tqdm
import numpy as np
import scipy
import os

from utils import *

def get_embeddings_and_map_globus(embedding_type):
    if embedding_type == "LinkBERT":
        hidden_shape = 1024
    if embedding_type == "specter" or embedding_type == "scincl":
        hidden_shape = 768
    # Because all coversion is already done !!    
    f = np.memmap(f'{HPC_DIR}/embedding/{embedding_type}/embedding.f.16', dtype = np.float16)
    f = f.reshape(int(f.shape[0]/hidden_shape), hidden_shape)
    old_to_new_map = np.memmap(f'{HPC_DIR}/embedding/{embedding_type}/map.old_to_new.i',\
            dtype = np.int32, mode = 'r')
    expanded_old_to_new = np.ones(270 * 10 ** 6, dtype = np.int32) * -1
    expanded_old_to_new[:old_to_new_map.shape[0]] = old_to_new_map
    del old_to_new_map
    return f, expanded_old_to_new


def extract_features_and_saveto_file(unique_nodes, map_old_to_new, embeddings, save_file):
    batch_size = (40960)
    temp = []
    import tqdm
    new_mapping = map_old_to_new[unique_nodes]
    print("Extract features", unique_nodes.shape, unique_nodes.shape[0] * embeddings.shape[1] * 4 / 1024 ** 3, "GB")
    for i in tqdm.tqdm(range(0, unique_nodes.shape[0], batch_size)):
        temp.append(embeddings[new_mapping[i:i + batch_size], :])
    features = np.vstack(temp)
    np.save(save_file, features)


def get_corpus_to_years_globus():
    years = np.load(f'{ROOT_DIR}/corpusId_to_year.npy')
    return years

from transformers import AutoTokenizer, AutoModel
def get_embeddings_from_hugging_face(model, abstract, title, seperator ):
    if model == "specter":
        MODELNAME = 'allenai/specter'
    if model == "scincl":
        MODELNAME = "malteos/scincl"
    tokenizer = AutoTokenizer.from_pretrained(MODELNAME)
    model = AutoModel.from_pretrained(MODELNAME)
    ##title_abs = [d['title'] + ' ' + (d.get('abstract') or '') for d in papers]
    title_abs = [title + ' ' + abstract]
    inputs = tokenizer(title_abs, padding=True, truncation=True, return_tensors="pt", max_length=512)
    result = model(**inputs)
    embeddings = result.last_hidden_state[:, 0, :].detach().numpy()
    return embeddings




def convert_embeddings_to_float16(EMBEDDING_TYPE):
    embedding, old_to_new = get_embeddings_and_map_globus(EMBEDDING_TYPE)
    assert(embedding.shape[0] == np.max(old_to_new) + 1)
    assert(embedding.dtype == np.float32)
    batch_size = 100000
    from tqdm import tqdm
    import gc
    import psutil
    out = np.memmap(f'{ROOT_DIR}/embedding/{EMBEDDING_TYPE}/embedding.f.16', \
                        shape =  embedding.shape, dtype = np.float16, mode = 'w+')
    for i in tqdm(range(0,embedding.shape[0], batch_size)):
        end = min(i + batch_size, embedding.shape[0])
        out[i: end, :]  = embedding[i: end, :].astype(np.float16)
        process = psutil.Process()
        print(process.memory_info().rss/ (1024 ** 3), "GB")

    assert(out.dtype == np.float16)
    print("All Write sucessfull to float 16", EMBEDDING_TYPE)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--embedding-name", type = str)
    args = parser.parse_args()
    print(args)
    EMBEDDING_TYPE = args.embedding_name
    print(EMBEDDING_TYPE)
    convert_embeddings_to_float16(EMBEDDING_TYPE)
