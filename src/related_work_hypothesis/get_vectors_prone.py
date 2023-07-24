
import numpy as np
import os
import joblib
import argparse
from util_prone import directory_to_config
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--idx", help="Semantic Scholar paper_id")
    parser.add_argument("-t", "--title", help="Paper Title")
    parser.add_argument("-I", "--idxs", help="Semantic Scholar paper_id list")
    parser.add_argument("-T", "--titles", help="Paper Title list")
    parser.add_argument("-o", "--output", help="output path", default='/mnt/c/Rodolfo/Desarrollo/JSALT_2023/vectors_prone')
    parser.add_argument("-m", "--model", help="model path", default='/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model')
    args = parser.parse_args()
    return args


def get_idx_title(title):
    title = title.replace(" ","%20")
    api_key = os.environ.get('Us7RqgayhnaQkEKiEnbGH8EBneX5Jud14Mq3Uzpe')
    base_url = 'https://api.semanticscholar.org/graph/v1/'
    headers = {"x-api-key": api_key}
    final_url = base_url + f"paper/search?query=" + title +"&limit=1"
    response = requests.get(final_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        paper_id = data['data'][0]['paperId']
        final_url = base_url + "paper/" + str(paper_id) +"?fields=externalIds&limit=1"
        response = requests.get(final_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            idx = data['externalIds']['CorpusId']
            return int(idx)
        else:
            print("Request Error:", response.status_code)
    else:
        print("Request Error:", response.status_code)
    return None


def main(): 
    args = parse_args() 
    print("Loading model configurations...") 
    configs = directory_to_config(args.model) 
    use_map = configs['map'] 
    use_emb = configs['embedding'] 
    print("Configurations loaded.") 
     
    if args.idx: 
        print("Processing index...") 
        idx2vec = {} 
        try: 
            idx = int(args.idx) 
            print(f"Getting embedding for index {idx}...") 
            paper_emb = use_emb[use_map[idx]] 
            idx2vec[idx] = np.array(paper_emb)
            print(np.array(paper_emb))
            print("Saving embedding...") 
            joblib.dump(idx2vec, os.path.join(args.output, str(idx) + "_prone.jbl")) 
            print("Embedding saved.") 
        except: 
            print(f'Error: could not process index {int(idx)}.') 
 
    elif args.title: 
        print("Processing title...") 
        title2vec = {} 
        title = args.title.replace("\n","") 
        print(f"Getting index for title {title}...") 
        idx = get_idx_title(title) 
        try: 
            print(f"Getting embedding for index {idx}...") 
            paper_emb = use_emb[use_map[idx]] 
            title2vec[idx] = np.array(paper_emb) 
            print("Saving embedding...") 
            joblib.dump(title2vec, os.path.join(args.output, str(idx) + "_prone.jbl")) 
            print("Embedding saved.") 
        except: 
            print(f'Error: could not process title {title}.') 
 
    elif args.idxs: 
        print("Processing list of indices...") 
        with open(args.idxs, 'r') as file: 
            lines = file.readlines() 
        idxs2vec = {} 
        for line in lines: 
            line = line.strip() 
            idx = line.replace("\n","") 
            idx = int(idx) 
            try: 
                print(f"Getting embedding for index {idx}...") 
                paper_emb = use_emb[use_map[idx]] 
                idxs2vec[idx] = np.array(paper_emb) 
            except: 
                print(f'Error: could not process index {idx}.') 
        print("Saving embeddings...") 
        joblib.dump(idxs2vec, os.path.join(args.output, "idxs_prone.jbl")) 
        print("Embeddings saved.") 
 
    if args.titles: 
        print("Processing list of titles...") 
        with open(args.titles, 'r') as file: 
            lines = file.readlines() 
        titles2vec = {} 
        for line in lines: 
            line = line.strip() 
            title = line.replace("\n","") 
            print(f"Getting index for title {title}...") 
            idx = get_idx_title(title) 
            try: 
                print(f"Getting embedding for index {idx}...") 
                paper_emb = use_emb[use_map[idx]] 
                titles2vec[idx] = np.array(paper_emb) 
            except: 
                print(f'Error: could not process title {title}.') 
        print("Saving embeddings...") 
        joblib.dump(titles2vec, os.path.join(args.output, "titles_prone.jbl")) 
        print("Embeddings saved.") 
 
    print("Process completed.")


if __name__ == "__main__":
    main()