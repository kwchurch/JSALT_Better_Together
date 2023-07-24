
import argparse
import pandas as pd
import numpy as np
from util_prone import directory_to_config, get_vector_prone
from tqdm import tqdm
import json
from util import get_cosine, get_centroid
from concurrent.futures import ProcessPoolExecutor
import os



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="reference File", default='../related_work_hypothesis/references_files/rw_citations.jsonl')
    args = parser.parse_args()
    return args


def process_citations(vector_paper_id,citations,model):
    cos_list = []
    vectors = []
    for rw_paper_id in citations:
        vector_rw = get_vector_prone(int(rw_paper_id),model)
        cos_prone = (get_cosine(vector_paper_id, vector_rw)).detach().numpy()
        cos_list.append(cos_prone)
        vectors.append(vector_rw)
    avg_cos = np.mean(cos_list) if len(cos_list) > 0 else 0
    new_vector = get_centroid(vectors)
    return new_vector, avg_cos


def save(result, file_name):
    df = pd.DataFrame(result)
    df.to_csv(file_name+".tsv", sep="\t", index=False)


def get_deter(v1,v2):
    v3 = v1 - v2
    return np.linalg.norm(v3)

def process_json(json_str, prone_model):
    data = json.loads(json_str)
    paper_id = data['paper_id']
    rw_citations = data['rw_citations']
    other_citations = data['other_citations']
    if len(rw_citations) == 0 or len(other_citations) == 0:
        return {"corpus_id": paper_id, "cos_rw": 0, "cos_all": 0, 
              "det_rw": 0, "det_all": 0}

    
    vector_paper_id = get_vector_prone(int(paper_id), prone_model)
    new_vector_rw, avg_rw = process_citations(vector_paper_id, rw_citations, prone_model)
    new_vector_all, avg_no_rw = process_citations(vector_paper_id, other_citations, prone_model)
    det_rw = get_deter(vector_paper_id,new_vector_rw)
    new_vector_all_2 = get_centroid([new_vector_rw,new_vector_all])
    det_all = get_deter(vector_paper_id,new_vector_all_2)
    result = {"corpus_id": paper_id, "cos_rw": avg_rw, "cos_all": ((avg_no_rw + avg_rw) / 2), 
              "det_rw": det_rw, "det_all": det_all}
    return result


def process_json_batch(json_batch, prone_model):
    hypos = []
    for json_str in tqdm(json_batch, desc='Processing Json'):
        hypo = process_json(json_str, prone_model)
        if hypo:
            hypos.append(hypo)
    return hypos


def main():
    args = parse_args()
    prone_model = directory_to_config("/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model")

    if args.input:
        batch_size = 500

        with open(args.input, 'r') as f:
            json_lines = list(f)

        total_number_of_lines = len(json_lines)
        num_batches = (total_number_of_lines + batch_size - 1) // batch_size

        hypos = []
        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, total_number_of_lines)
            json_batch = json_lines[start_idx:end_idx]
            batch_hypos = process_json_batch(json_batch, prone_model)
            hypos.extend(batch_hypos)

            # Save results every 100 batches
            if (batch_num) % 10 == 0:
                print("Guardando")
                save(hypos, f"rw_hypo_batch{batch_num+1}")
                hypos = []

        # Save final results after processing all batches
        save(hypos, "rw_hypo")


if __name__ == "__main__":
    main()
