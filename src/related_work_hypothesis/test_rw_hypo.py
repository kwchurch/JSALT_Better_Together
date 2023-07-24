
import argparse
import pandas as pd
import numpy as np
from util_prone import directory_to_config
from tqdm import tqdm
import json
from util import get_cosine



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="reference File", default='../related_work_hypothesis/references_files/rw_citations.jsonl')
    args = parser.parse_args()
    return args


def get_vector_prone(idx):
    configs = directory_to_config("/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model")
    use_map = configs['map']
    use_emb = configs['embedding']
    try:
        paper_emb = use_emb[use_map[int(idx)]]
    except:
        print(f'failed with {int(idx)}')
    return np.array(paper_emb)


def main(): 
    args = parse_args() 
 
    if args.input:
        
        result = []
        hypo = []
        with open(args.input, 'r') as f:
            json_list = f.readlines()

            # Wrap the json_list with tqdm for progress bar
            for json_str in tqdm(json_list, desc='Processing JSON'):
                data = json.loads(json_str)
                paper_id = data['paper_id']
                rw_citations = data['rw_citations']
                other_citations = data['other_citations']
                vector_paper_id = get_vector_prone(int(paper_id))

                rw_cos = []
                no_rw_cos = []
                avg_rw = 0
                avg_no_rw = 0
                if len(rw_citations) > 0:

                    # Wrap the rw_citations loop with tqdm for progress bar
                    for rw in tqdm(rw_citations, desc='Processing RW Citations', leave=False):
                        rw_paper_id = rw
                        vector_paper_id = get_vector_prone(int(rw_paper_id))
                        cos_prone = get_cosine(vector_paper_id, vector_paper_id)
                        data = {"rw": 1, "id1": paper_id, "id2": rw_paper_id, "propose": cos_prone}
                        result.append(data)
                        rw_cos.append(cos_prone)
                        
                if len(other_citations) > 0:

                    # Wrap the other_citations loop with tqdm for progress bar
                    for rw in tqdm(other_citations, desc='Processing Other Citations', leave=False):
                        rw_paper_id = rw
                        vector_paper_id = get_vector_prone(int(rw_paper_id))
                        cos_prone = get_cosine(vector_paper_id, vector_paper_id)
                        data = {"rw": 0, "id1": paper_id, "id2": rw_paper_id, "propose": cos_prone}
                        result.append(data)
                        no_rw_cos.append(cos_prone)

                if len(rw_cos) > 0:
                    avg_rw = np.mean(rw_cos)
                else:
                    avg_rw = 0

                if len(no_rw_cos) > 0:
                    avg_no_rw = np.mean(no_rw_cos)
                else:
                    avg_no_rw = 0

                datas = {"corpus_id": paper_id, "rw": avg_rw, "no_rw": avg_no_rw}
                hypo.append(datas)

        df = pd.DataFrame(result)
        df.to_csv("rw_results_1.tsv", sep="\t", index=False)

        df2 = pd.DataFrame(hypo)
        df2.to_csv("rw_hypo_1.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
