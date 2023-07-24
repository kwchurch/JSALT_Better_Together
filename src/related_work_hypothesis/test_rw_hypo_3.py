import argparse
import pandas as pd
import numpy as np
from util_prone import directory_to_config
from tqdm import tqdm
import json
from util import get_cosine
from concurrent.futures import ThreadPoolExecutor
from os import path
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="reference File", default='../related_work_hypothesis/references_files/rw_citations.jsonl')
    args = parser.parse_args()
    return args


def get_vector_prone(idx,configs):
    use_map = configs['map']
    use_emb = configs['embedding']
    try:
        paper_emb = use_emb[use_map[int(idx)]]
    except:
        print(f'failed with {int(idx)}')
    return np.array(paper_emb)


def process_citations(paper_id,vector_paper_id,citations,flag):
    result = []
    cos_list = []
    for rw_paper_id in citations:
        vector_rw = get_vector_prone(int(rw_paper_id))
        cos_prone = (get_cosine(vector_paper_id, vector_rw)).detach().numpy()
        data = {"rw":flag, "id1": paper_id, "id2": rw_paper_id, "propose": cos_prone}
        result.append(data)
        cos_list.append(cos_prone)
    avg_cos = np.mean(cos_list) if len(cos_list) > 0 else 0
    return result, round(avg_cos, 4)


def save(result, file_name):
    df = pd.DataFrame(result)
    df.to_csv(f"{file_name}.tsv", sep="\t", index=False)


def find_last_counter():
    counter = 0
    while path.exists(f"rw_results.tsv"):
        counter += 1
    return counter

def main():
    args = parse_args()
    start_counter = find_last_counter()
    prone_model = directory_to_config(dir)
    if args.input:
        result = []
        hypo = []
        counter = start_counter
        json_line_number = 0
        with open(args.input, 'r') as f:
            total_number_of_lines = sum(1 for _ in f)
        flag_2 = 1

        def process_json(json_str):
            nonlocal flag_2, counter, result, hypo
            data = json.loads(json_str)
            paper_id = data['paper_id']
            rw_citations = data['rw_citations']
            other_citations = data['other_citations']
            vector_paper_id = get_vector_prone(int(paper_id))
            rw_result, avg_rw = process_citations(paper_id, vector_paper_id, rw_citations, 1)
            other_result, avg_no_rw = process_citations(paper_id, vector_paper_id, other_citations, 0)
            result.extend(rw_result + other_result)
            datas = {"corpus_id": paper_id, "rw": avg_rw, "all": (avg_no_rw + avg_rw) / 2}
            hypo.append(datas)

            # Save the results every 1000 json_str
            if flag_2 % 100 == 0:
                save(result, "rw_results")
                counter += 1
                save(hypo, "rw_hypo")

            flag_2 = flag_2 + 1

            # Agregar un mensaje de progreso
            print(f"Processed JSON line: {json_line_number} / {total_number_of_lines}")

        with open(args.input, 'r') as f:
            with ThreadPoolExecutor() as executor:
                futures = []
                for json_str in tqdm(f, desc='Processing Json', total=total_number_of_lines):
                    if json_line_number >= start_counter * 100:
                        future = executor.submit(process_json, json_str)
                        futures.append(future)
                    json_line_number += 1

                # Esperar a que todas las tareas se completen
                for future in futures:
                    future.result()

        save(result, "rw_results")
        # Guardar las hipótesis restantes también
        save(hypo, "rw_hypo")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds.")
