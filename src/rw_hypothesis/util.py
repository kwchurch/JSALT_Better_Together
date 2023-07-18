
import numpy as np
import torch
from pprint import pprint
import json


def get_centroid(arr):
    centroid = np.mean(arr, axis=0)
    return centroid


def get_cosine(t1,t2):
    t1 = torch.from_numpy(t1)
    t2 = torch.from_numpy(t2)
    cos = torch.nn.CosineSimilarity(dim=0)
    output = cos(t1, t2)
    return output


def read_rw_paper(file):
    with open(file, 'r') as f:
        json_list = f.readlines()

    # Iterate over each JSON object
    for json_str in json_list:
        # Parse the JSON object
        data = json.loads(json_str)
        
        # Access the values
        paper_id = data['paper_id']
        rw_citations = data['rw_citations']
        other_citations = data['other_citations']
        
        # Print the values
        print("Paper ID:", paper_id)
        print("RW Citations:", rw_citations)
        print("Other Citations:", other_citations)
        print()


def get_vector_hf(tokenizer, model, s):
    inputs = tokenizer(s, padding=True, truncation=True, return_tensors="pt", max_length=512)
    result = model(**inputs)
    embeddings = result.last_hidden_state[:, 0, :]
    return embeddings.detach().numpy().reshape(-1).astype(np.float32)