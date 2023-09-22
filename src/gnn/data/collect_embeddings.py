# collect embeddings for globus 
import numpy as np
import tqdm
import argparse
path = ""
HPC_DIR="/scratch/workspace/spolisetty_umass_edu-jsalt"
ROOT_DIR = "/work/pi_huiguan_umass_edu/sandeep/jsalt"
import gc
def collect( embedding, bin_max,  ):
    
    embedding_stack = []
    new_to_old_stack = []
    for bin_number in tqdm.tqdm(range(0,bin_max,10)):
        embedding_stack.append(np.load(f"{HPC_DIR}/{embedding}/full_{bin_number}/EMBEDDING.npy"))
        new_to_old_stack.append(np.load(f"{HPC_DIR}/{embedding}/full_{bin_number}/original_target.npy"))
    
    embeddings = np.vstack(embedding_stack).astype('float32')
    del embedding_stack
    gc.collect()
                                ### Add correctness measures                             
    with open(f"{ROOT_DIR}/gnn/{embedding}/embeddings.f",'wb') as fp:
        fp.write(embeddings.tobytes('c'))
    check_sum = np.sum(np.memmap(f"{ROOT_DIR}/gnn/{embedding}/embeddings.f", dtype = np.float32)[:10])
    correct_sum = np.sum(embeddings[0,:10])
    #print("Check ", check_sum, correct_sum)
                                
    new_to_old = np.hstack(new_to_old_stack).astype('int32')
    print(new_to_old.shape)
    with open(f"{ROOT_DIR}/gnn/{embedding}/new_to_old.int", "wb") as fp:
        fp.write(new_to_old.tobytes('c'))
    old_to_new = np.ones(270 *10 ** 6, dtype = np.int32) * -1
    old_to_new[new_to_old] = np.arange(new_to_old.shape[0])
    with open(f"{ROOT_DIR}/gnn/{embedding}/old_to_new.int", "wb") as fp:                            
        fp.write(old_to_new.tobytes('c'))
                                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='collect',
                    description='Collects all embeddings locally')
    parser.add_argument('--embedding',  type = str)
    parser.add_argument('--bin', type = int)
    args =parser.parse_args()
    print(args)
    collect(args.embedding, args.bin)
