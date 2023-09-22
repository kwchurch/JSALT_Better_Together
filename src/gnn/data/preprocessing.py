MAX_CORPUS_ID = 270 * 10 ** 6
from get_graph_data import *
from get_embeddings import *
import gc 

def get_row_induced_graph(row, col,  bins, begin_bin, end_bin):
    assert(row.shape == col.shape)
    edge_num = np.where((bins[row] >= begin_bin) & (bins[row] < end_bin))[0]
    assert(np.all(row[edge_num] < MAX_CORPUS_ID))
    assert(np.all(col[edge_num] < MAX_CORPUS_ID))
    return (row[edge_num], col[edge_num])
    
def partition_coo_graph_by_select_two_edges_per_row_node(coo_rows, coo_cols):
    # coo_rows, coo_cols = get_induced_graph(coo, 2018, 2019)
    coo_local = scipy.sparse.coo_array((np.zeros(coo_rows.shape),\
         (coo_rows, coo_cols)),shape = (270 * 10 ** 6, 270 * 10 ** 6))
    csr_local = coo_local.tocsr()
    coo_rows_unique = coo_rows.copy()
    coo_rows_unique.sort()
    target_nodes = np.unique(coo_rows_unique)
    assert(csr_local.indptr.shape[0] == (270 * 10 ** 6 + 1)) 
    degree = csr_local.indptr[target_nodes + 1] - csr_local.indptr[target_nodes]
    target_nodes = target_nodes[np.where(degree > 10)]
    degree = csr_local.indptr[target_nodes + 1] - csr_local.indptr[target_nodes]
    assert(np.all(degree > 10))
    dest = []
    assert(csr_local.indices.shape[0] == coo_rows.shape[0])
    mask = np.zeros(coo_local.col.shape[0])
    for i in range(2):
        offset = (np.random.rand(degree.shape[0]) * degree).astype(np.int32)
        selected_offsets = csr_local.indptr[target_nodes] + offset
        selected_dest = csr_local.indices[selected_offsets]
        mask[selected_offsets] = True
        assert(np.all(selected_offsets < MAX_CORPUS_ID))
        dest.append(selected_dest)
    dest = np.hstack(dest)
    src  = np.hstack([target_nodes, target_nodes])
    remaining_edges = np.where(mask == 0)[0]
    remaining_dest = coo_local.col[remaining_edges]
    remaining_src = coo_local.row[remaining_edges]
    return src, dest, remaining_src, remaining_dest

def save_features(embeddings, old_to_new, unique_nodes, save_path):
    # This is another old to new. 
    # preserve order of unique nodes
    selected = np.where(old_to_new[unique_nodes] != -1)[0]
    collect = []
    batch_size = 10000
    for i in tqdm(range(0,selected.shape[0], batch_size)):
        assert(np.all(old_to_new[unique_nodes[selected[i: i + batch_size]]] != -1))
        collect.append(embeddings[old_to_new[unique_nodes[selected[i: i + batch_size]]]])
    new_feat = np.vstack(collect)    
    np.save(f'{save_path}/features', new_feat)
    del collect, new_feat
    gc.collect()
    new_old_to_new = np.ones(unique_nodes.shape[0], dtype = int) * -1    
    new_old_to_new[selected] = np.arange(selected.shape[0])
    np.save(f"{save_path}/unique_nodes", unique_nodes)
    np.save(f"{save_path}/old_to_new", new_old_to_new)
    

def remapping(rows, cols):
    unq_nodes = np.unique([rows,cols])
    mapping = np.zeros(np.max(unq_nodes) + 1, dtype = np.int32)
    mapping[unq_nodes] = np.arange(unq_nodes.shape[0])
    return mapping[rows], mapping[cols], unq_nodes, mapping

def remapping_with_extra(rows, cols, other_nodes):
    unq_nodes = np.unique(np.hstack([rows, cols, other_nodes]))
    mapping = np.zeros(np.max(unq_nodes) + 1, dtype = np.int32)
    mapping[unq_nodes] = np.arange(unq_nodes.shape[0])
    return mapping[rows], mapping[cols], unq_nodes, mapping 


def partition_edges_with_and_without_text(old_to_new, row, col, has_text):
    if has_text:
        select = old_to_new[row] != -1
    else: 
        select = old_to_new[row] == -1 
    return np.vstack([row[select], col[select]])

def create_bin_masked(bin_number, embedding_type):
    ## Get graph, bin_mapping 
    id2bins = get_id2bins()
    embeddings, old_to_new = get_embeddings_and_map_globus(embedding_type)
    rows, cols = get_full_graph_in_coo()
    TRAIN_BIN_START = bin_number
    TRAIN_BIN_END = bin_number + 8
    TRANS_BIN_END = bin_number + 9
    INDUC_BIN_END = bin_number + 10

    ###### Select edges for all kinds of graphs
    collect = {}
    train_row, train_col = get_row_induced_graph(rows, cols,  id2bins, TRAIN_BIN_START, TRAIN_BIN_END)
    trans_row, trans_col = get_row_induced_graph(rows, cols,  id2bins, TRAIN_BIN_END, TRANS_BIN_END)
    test_row_trans, test_col_trans, remaining_row_trans, remaining_col_trans = \
        partition_coo_graph_by_select_two_edges_per_row_node(trans_row, trans_col)
    val_row, val_col = get_row_induced_graph(rows, cols, id2bins, TRANS_BIN_END, INDUC_BIN_END)
    test_row_ind, test_col_ind, remaining_row_ind, remaining_col_ind = \
        partition_coo_graph_by_select_two_edges_per_row_node(val_row, val_col)
    collect["trans"] = test_row_trans, test_col_trans
    collect["induc"] = test_row_ind, test_col_ind
    
    ###### Create training graph 
    os.makedirs(f"{HPC_DIR}/{embedding_type}", exist_ok = True)
    SAVE_PATH = f"{HPC_DIR}/{embedding_type}/masked_{bin_number}/train"
    os.makedirs(SAVE_PATH, exist_ok = True)
    train_rows = np.hstack([train_row, remaining_row_trans])
    train_cols = np.hstack([train_col, remaining_col_trans])
    map_rows, map_cols, unq_nodes, mapping = remapping(train_rows, train_cols)
    np.save(f"{SAVE_PATH}/unique_nodes", unq_nodes)
    train_graph = np.vstack([map_rows, map_cols])
    np.save(f"{SAVE_PATH}/graph", train_graph)
    save_features(embeddings, old_to_new, unq_nodes, SAVE_PATH)

    ###### Create Val Graph               
    SAVE_PATH = f"{HPC_DIR}/{embedding_type}/masked_{bin_number}/val"
    os.makedirs(SAVE_PATH, exist_ok = True)
    
    val_rows = np.hstack([train_row, remaining_row_trans, remaining_row_ind])
    val_cols = np.hstack([train_col, remaining_col_trans, remaining_col_ind])
    map_rows, map_cols, unq_nodes, mapping  = remapping_with_extra(val_rows, val_cols, np.hstack([trans_row, trans_col, val_row, val_col]))
    val_graph = np.vstack([map_rows, map_cols])
    np.save(f"{SAVE_PATH}/graph", val_graph)
    np.save(f"{SAVE_PATH}/unique_nodes", unq_nodes)
    save_features(embeddings, old_to_new, unq_nodes, SAVE_PATH)

    #### Partition Test Edges
    old_to_new = old_to_new[unq_nodes]
    local_remap = mapping 
    # local_remap = np.zeros(np.max(unq_nodes) + 1, np.int64)
    # local_remap[unq_nodes] = np.arange(unq_nodes.shape[0])
    final = {}
    for has_text in [True,False]:
        for mode in ["trans", "induc"]:
            if has_text:
                text_str = "HASTEXT"
            else:
                text_str = "HASNOTEXT"    
            np.save(f"{SAVE_PATH}/{text_str}_{mode}", partition_edges_with_and_without_text\
                            (old_to_new, local_remap[collect[mode][0]], local_remap[collect[mode][1]], has_text))
            

def create_bin(bin_number, embedding_type):
    ##  Since there is no maksing all edges are used during training.
    ### Select vertices that fall with in the bin 
    os.makedirs(f"{HPC_DIR}/{embedding_type}", exist_ok = True)
    SAVE_PATH = f"{HPC_DIR}/{embedding_type}/full_{bin_number}"
    os.makedirs(SAVE_PATH, exist_ok = True)
    
    embeddings, old_to_new = get_embeddings_and_map_globus(embedding_type)
    
    id2bins = get_id2bins()
    rows, cols = get_full_graph_in_coo()
    ### Construct the induced graph 
    BIN_START = bin_number 
    BIN_END = bin_number + 10
    train_row, train_col = get_row_induced_graph(rows, cols,  id2bins, BIN_START, BIN_END)
    ### To do preserve out nodes. 
    map_rows, map_cols, unq_nodes, mapping  = remapping(train_row, train_col)
    graph = np.vstack([map_rows, map_cols])
    np.save(f"{SAVE_PATH}/graph", graph)
    np.save(f"{SAVE_PATH}/unique_nodes", unq_nodes)
    target_nodes = np.unique(map_rows)
    np.save(f"{SAVE_PATH}/target_nodes", target_nodes)
    # mapping = np.zeros(np.max(unq_nodes) + 1)
    # mapping[unq_nodes] = np.arange(unq_nodes.shape[0])
    # Use this to do the final saving
    np.save(f"{SAVE_PATH}/original_target", unq_nodes[target_nodes])
    save_features(embeddings, old_to_new, unq_nodes, SAVE_PATH)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='preprocessing',
                    description='Creates binned partitions of graph')
    parser.add_argument('--is-masked',  action = 'store_true')
    parser.add_argument('--bin', type = int)
    parser.add_argument('--embedding-type', type = str, help = "specter or scincl")
    args = parser.parse_args()
    print(args)
    assert(args.embedding_type in ["specter", "scincl"])
    if args.is_masked:
        create_bin_masked(args.bin, args.embedding_type)
    else:
        create_bin(args.bin, args.embedding_type)
    print("Preprecessing exited cleanly")
