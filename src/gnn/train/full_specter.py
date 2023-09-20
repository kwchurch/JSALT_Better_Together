import numpy 
import numpy as np 
import os, psutil
import dgl
from dgl.utils import pin_memory_inplace
import time
import argparse
ROOT_DIR = f'/work/pi_huiguan_umass_edu/sandeep/jsalt/'
HPC_DIR = "/scratch/workspace/spolisetty_umass_edu-jsalt"
import torch
from link_pred import * 


def get_embeddings(save_path):
    features = np.load(f'{save_path}/features.npy')
    # old here refers to the id in graph not in semantic scholar
    old_to_new = np.load(f'{save_path}/old_to_new.npy')
    unique_nodes = np.load(f'{save_path}/unique_nodes.npy')
    return features, torch.from_numpy(old_to_new), torch.from_numpy(unique_nodes)

def getMemory():
    process = psutil.Process()
    print(process.memory_info().rss/ (1024 **3),"Bytes")  # in bytes 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        default="mixed",
        choices=["cpu", "mixed", "puregpu"],
        help="Training mode. 'cpu' for CPU training, 'mixed' for CPU-GPU mixed training, "
        "'puregpu' for pure-GPU training.",
    )
    parser.add_argument('--embedding', type = str, choices = ["specter", "scincl"])
    parser.add_argument('--masked', action = "store_true")
    parser.add_argument('--training-mode', type = str, choices = ["train", "valid", "test"])
    parser.add_argument('--bin', type = int)
    parser.add_argument('--model-bin', type = int)
    parser.add_argument('--model', type = str , choices = ["sage", "gat"])
    parser.add_argument('--no-empty', action = "store_true")
    parser.add_argument('--normalize', action = "store_true")

    args = parser.parse_args()
    print(args)
    if not torch.cuda.is_available():
        args.mode = "cpu"
   
    ## SAVE_PATH 
    if args.training_mode == "test":
        assert(args.masked == False)
        SAVE_PATH = f"{HPC_DIR}/{args.embedding}/full_{args.bin}"
    if args.training_mode == "valid":
        assert(args.masked == True)
        SAVE_PATH = f"{HPC_DIR}/{args.embedding}/masked_{args.bin}/val"
    if args.training_mode == "train":
        if args.masked:
            SAVE_PATH = f"{HPC_DIR}/{args.embedding}/masked_{args.bin}/train"
        else:     
            SAVE_PATH = f"{HPC_DIR}/{args.embedding}/full_{args.bin}"

    ### Get Input Features 
    f, old_to_new, unique_nodes = get_embeddings(SAVE_PATH)
    num_nodes = old_to_new.shape[0]
    
    feature = torch.from_numpy(f)
    in_size = feature.shape[1]
    device = torch.device("cpu" if args.mode == "cpu" else "cuda")


    pinned_handle = pin_memory_inplace(feature)

    print(f"Training in {args.training_mode} mode.")
        ## Construct Graph 
    edge = numpy.load(f'{SAVE_PATH}/graph.npy').astype('int64')
    edge = torch.from_numpy(edge)
    assert(torch.all(edge[0,:] < old_to_new.shape[0]) and torch.all(edge[1,:] < old_to_new.shape[0]))
    g = dgl.graph(('coo', (edge[0,:], edge[1,:])),num_nodes = old_to_new.shape[0])
    g = g.remove_self_loop()
    if args.training_mode == "train":  
        ## All Edges are Training Edges   
        edge_split = {}
        edge_split['source_node'] = edge[0,:]
        edge_split['target_node'] = edge[1,:]

    if args.training_mode == "valid":
        edge_split = {}
        for style in ["trans", "induc"]:
            edge_split[style] = {}
            for text in ["HASTEXT", "HASNOTEXT"]:
                edge_split[style][text] = {}
                temp = torch.from_numpy(\
                        numpy.load(f'{SAVE_PATH}/{text}_{style}.npy').astype('int64'))
                edge_split[style][text]['source_node'] = temp[0,:]
                edge_split[style][text]['target_node'] = temp[1,:]
                print(torch.where(torch.hstack([temp[0,:],temp[1,:]]) > num_nodes), "Check")
                assert(torch.all(temp < num_nodes))
                edge_split[style][text]['target_node_neg'] = torch.randint(0,num_nodes, (temp.shape[1],1000))
    if args.training_mode == "test":
        out_nodes = np.load(f"{SAVE_PATH}/target_nodes.npy")  
    # load and preprocess dataset
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Loading Graph complete<<<<<<<<<<<<<<<<<<<<")
       
    g = g.to("cuda" if args.mode == "puregpu" else "cpu")
    device = torch.device("cpu" if args.mode == "cpu" else "cuda")
    a = time.time()

    

    g, reverse_eids = to_bidirected_with_reverse_mapping(g)
    orignal_edges = g.num_edges()
    print("Reversal stats", g.num_edges(), reverse_eids.shape)

    reverse_eids = reverse_eids.to(device)
    #edge_split = dataset.get_edge_split()
    print("Graph reversal which aids in sampling ", time.time() - a)
    # create GraphSAGE model
    in_size = feature.shape[1]
    model = SAGE(in_size, 256, args.model).to(device)
    save_path = f"{ROOT_DIR}/models/{args.model}_no_empty_{args.no_empty}_bin{args.bin}_norm{args.normalize}_{args.embedding}"
    if args.training_mode != "train":
        save_path = f"{ROOT_DIR}/models/{args.model}_no_empty_{args.no_empty}_bin{args.model_bin}_norm{args.normalize}_{args.embedding}"
        print("For inference using the latest model from", save_path)
        model.load_state_dict(torch.load(save_path))
    batch_size = 1024
    # model training
    print("Training...", device)
    if args.training_mode == "train":
        print("Training..", device)
        e = g.edges()
        wts = g.out_degrees()[e[1]]
        vals, indices = wts.sort(descending = True )
        seed_edges = indices[:6000000]
        print("percentage of selected", torch.sum(vals[:6000000])/torch.sum(vals[vals > 2]))
        # seed_edges = torch.arange(g.num_edges()).to(device)
        if args.model == "gat":
            g = dgl.add_self_loop(g)

        train(args, device, g, reverse_eids, seed_edges, model, feature, save_path, old_to_new)
        print("train complete")
    # validate/test the model
    if args.training_mode == "valid":
        print("Validation/Testing...")
        if args.model == "gat":
            g = dgl.add_self_loop(g)

        mrr_dict = evaluate(args, 
              device, g, edge_split, model, feature,  old_to_new, batch_size=1000)
        print(mrr_dict)
    if args.training_mode == "test":
        if args.model == "gat":
            g = dgl.add_self_loop(g)

        evaluate_and_save(args, device, g , out_nodes, model, feature, old_to_new, batch_size, SAVE_PATH)
