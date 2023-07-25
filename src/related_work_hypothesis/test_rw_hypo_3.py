
import argparse
import pandas as pd
from util_prone import directory_to_config, get_vector_prone
from tqdm import tqdm
import json
from util import get_centroid
import numpy as np



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="reference File", default='../related_work_hypothesis/references_files/rw_citations.jsonl')
    args = parser.parse_args()
    return args


def process_citations(citations,model):
    vectors = []
    for rw_paper_id in citations:
        vector_rw = get_vector_prone(int(rw_paper_id),model)
        vectors.append(vector_rw)
    new_vector = get_centroid(vectors)
    return new_vector


def save(result, file_name):
    df = pd.DataFrame(result)
    df.to_csv(file_name+".tsv", sep="\t", index=False)


def process_json(json_str, prone_model):
    data = json.loads(json_str)
    paper_id = data['paper_id']
    rw_citations = data['rw_citations']
    other_citations = data['other_citations']
    if len(rw_citations) == 0 or len(other_citations) == 0:
        return 0

    vector_paper_id = get_vector_prone(int(paper_id), prone_model)
    new_vector_rw = process_citations(rw_citations, prone_model)
    new_vector_nrw = process_citations(other_citations, prone_model)
    result = {"corpus_id": paper_id, "V_prone": list(vector_paper_id), "V_rw": list(new_vector_rw), "V_nrw": list(new_vector_nrw)}
    return result


def process_json_batch(json_batch, prone_model):
    hypos = []
    for json_str in tqdm(json_batch, desc='Processing Json'):
        hypo = process_json(json_str, prone_model)
        if hypo and hypo != 0:
            hypos.append(hypo)
    return hypos


def main():
    args = parse_args()
    prone_model = directory_to_config("/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model")

    if args.input:
        batch_size = 1000

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
            if (batch_num) % 1 == 0:
                print("Guardando")
                save(hypos, f"regression_batch{batch_num+1}")
                hypos = []

        # Save final results after processing all batches
        save(hypos, "regression_batch")


if __name__ == "__main__":
    main()
