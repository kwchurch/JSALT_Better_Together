import argparse

import dgl
import dgl.nn as dglnn
import torch
import torch.nn as nn
import torch.nn.functional as F
import tqdm
from dgl.dataloading import (
    as_edge_prediction_sampler,
    DataLoader,
    MultiLayerFullNeighborSampler,
    negative_sampler,
    NeighborSampler,
)
import numpy as np
from ogb.linkproppred import DglLinkPropPredDataset, Evaluator
import time
import gc
from dgl.utils import pin_memory_inplace
from dgl.utils import gather_pinned_tensor_rows


def to_bidirected_with_reverse_mapping(g):
    """Makes a graph bidirectional, and returns a mapping array ``mapping`` where ``mapping[i]``
    is the reverse edge of edge ID ``i``. Does not work with graphs that have self-loops.
    """
    print("Start computing a revesal")
    g_simple, mapping = dgl.to_simple(
        dgl.add_reverse_edges(g), return_counts="count", writeback_mapping=True
    )
    print("Reversal g_simple")
    c = g_simple.edata["count"]
    num_edges = g.num_edges()
    mapping_offset = torch.zeros(
        g_simple.num_edges() + 1, dtype=g_simple.idtype
    )
    mapping_offset[1:] = c.cumsum(0)
    print("Mapping")
    idx = mapping.argsort()
    idx_uniq = idx[mapping_offset[:-1]]
    reverse_idx = torch.where(
        idx_uniq >= num_edges, idx_uniq - num_edges, idx_uniq + num_edges
    )
    reverse_mapping = mapping[reverse_idx]
    # sanity check
    print("skipping Sanity checking")
    if True:
        src1, dst1 = g_simple.edges()
        src2, dst2 = g_simple.find_edges(reverse_mapping)
        assert torch.equal(src1, dst2)
        assert torch.equal(src2, dst1)
    return g_simple, reverse_mapping

class WrapMissingFeatures():
    def __init__(self, old_to_new, empty, feature, normalize,  no_empty):
        self.old_to_new = old_to_new
        self.empty = empty
        if no_empty:
            self.empty = torch.rand(empty.shape, device = empty.device)
        self.pinned_feature = feature 
        self.normalize = normalize
        self.normalize_layer = torch.nn.BatchNorm1d(feature.shape[1], affine=False).to(empty.device)

    def get_device_features(self, ids,):
        old_to_new = self.old_to_new
        empty  = self.empty
        pinned_features = self.pinned_feature
        ######################################
        not_found = torch.where(old_to_new[ids] == -1)[0]
        shuffle_idx = torch.arange(ids.shape[0])

        if not_found.shape[0] == 0:
            found_tensors =  gather_pinned_tensor_rows(pinned_features, old_to_new[ids])
            if self.normalize:
                return self.normalize_layer(found_tensors)
        found = torch.where(old_to_new[ids] != -1)[0]
        final_idx = torch.cat([found, not_found], dim = 0)
        _, final_idx = torch.sort(final_idx, descending = False)
        b= old_to_new[ids[found]]
        assert(torch.all(b != -1))
        if found.device == torch.device('cpu'):
            found_tensors = pinned_features[old_to_new[ids[found]]]
        else:
            found_tensors = gather_pinned_tensor_rows(pinned_features, old_to_new[ids[found]].to(torch.long))
        if self.normalize:
            found_tensors = self.normalize_layer(found_tensors) 
        not_found_tensors = torch.ones((not_found.shape[0],empty.shape[0]), device = empty.device) * empty
        final_tensor = torch.cat([found_tensors, not_found_tensors] , dim = 0)
        return final_tensor[final_idx]

class SAGE(nn.Module):
    def __init__(self, in_size, hid_size, model):
        super().__init__()
        self.model = model 
        assert(model in ["sage","gat"])

        self.layers = nn.ModuleList()
        # three-layer GraphSAGE-mean
        if model == "sage":
            self.layers.append(dglnn.SAGEConv(in_size, hid_size, "mean"))
            self.layers.append(dglnn.SAGEConv(hid_size, hid_size, "mean"))
        if model == "gat":
            num_heads = 4 
            self.layers.append(dglnn.GATConv(in_size, hid_size//4 , num_heads = num_heads))
            self.layers.append(dglnn.GATConv(hid_size, hid_size//4, num_heads = num_heads))
        #self.layers.append(dglnn.SAGEConv(hid_size, hid_size, "mean"))
        self.hid_size = hid_size
        self.empty = torch.nn.Parameter(torch.rand(in_size,))
        self.predictor = nn.Sequential(
            nn.Linear(hid_size, hid_size),
            nn.ReLU(),
         #   nn.Linear(hid_size, hid_size),
         #   nn.ReLU(),
            nn.Linear(hid_size, 1),
        )

    def forward(self, pair_graph, neg_pair_graph, blocks, x):
        h = x
        for l, (layer, block) in enumerate(zip(self.layers, blocks)):
            h = layer(block, h)
            if l != len(self.layers) - 1:
                h = F.relu(h)
            if self.model == "gat":
                h = h.flatten(1)

        pos_src, pos_dst = pair_graph.edges()
        neg_src, neg_dst = neg_pair_graph.edges()
        h_pos = self.predictor(h[pos_src] * h[pos_dst])
        h_neg = self.predictor(h[neg_src] * h[neg_dst])
        return h_pos, h_neg

    def inference(self, g, device, batch_size, wrapped_features, old_to_new):
        """Layer-wise inference algorithm to compute GNN node embeddings."""
        #feat = g.ndata["feat"]
        #sampler = MultiLayerFullNeighborSampler(1, prefetch_node_feats=["feat"])
        #sampler = NeighborSampler([10]) 
        sampler = MultiLayerFullNeighborSampler(1)
        dataloader = DataLoader(
            g,
            torch.arange(g.num_nodes()).to(device),
            sampler,
            device=device,
            batch_size=batch_size,
            shuffle=False,
            drop_last=False,
            num_workers=0,
            use_prefetch_thread=None, 
            use_uva = True
            )
        buffer_device = torch.device("cpu")
        pin_memory = buffer_device != device
         
        for l, layer in enumerate(self.layers):
            print("Trying to allocate more memory")
            y = torch.empty(
                g.num_nodes(),
                self.hid_size,
                device=buffer_device,
                pin_memory=pin_memory,
            )
            #feat = feat.to(device)
            print("Start of new Iteration")
            for it, (input_nodes, output_nodes, blocks) in tqdm.tqdm(
                enumerate(dataloader), desc="Inference"
            ):
                if l == 0:
                    x = wrapped_features.get_device_features(input_nodes)
                    #x = gather_pinned_tensor_rows(features, input_nodes) 
                else:
                    #x = hidden[input_nodes]
                    x = gather_pinned_tensor_rows(hidden, input_nodes)
                #x = feat[input_nodes.to(features.device)].to(device)
                h = layer(blocks[0], x)
                if l != len(self.layers) - 1:
                    h = F.relu(h)
                if self.model == "gat":
                    h = h.flatten(1)    
                y[output_nodes] = h.to(buffer_device)
            gc.collect()
            print("End of Iternation")
            hidden = y
        return y


def compute_mrr(
    model, evaluator, node_emb, src, dst, neg_dst, device, batch_size=512
):
    """Compute Mean Reciprocal Rank (MRR) in batches."""
    rr = torch.zeros(src.shape[0])
    print("Inference batch size is", batch_size)
    gc.collect()
    
    for start in tqdm.trange(0, src.shape[0], batch_size, desc="Evaluate"):
        end = min(start + batch_size, src.shape[0])
        all_dst = torch.cat([dst[start:end, None], neg_dst[start:end]], 1)
        h_src = node_emb[src[start:end]][:, None, :].to(device)
        h_dst = node_emb[all_dst.view(-1)].view(*all_dst.shape, -1).to(device)
        pred = model.predictor(h_src * h_dst).squeeze(-1)
        input_dict = {"y_pred_pos": pred[:, 0], "y_pred_neg": pred[:, 1:]}
        rr[start:end] = evaluator.eval(input_dict)["mrr_list"]
    return rr.mean()


def evaluate(args, device, graph, edge_split, model, feature, old_to_new, batch_size):
    model.eval()
    evaluator = Evaluator(name="ogbl-citation2")
    wrapped_feature = WrapMissingFeatures(old_to_new.to(device), model.empty, feature,\
                                args.normalize, args.no_empty)
    with torch.no_grad():
        node_emb = model.inference(graph, device, batch_size, wrapped_feature, old_to_new)
        results = []
        #for split in ["test","valid"]:
        for style in edge_split.keys():
            for keys in edge_split[style].keys():
                src = edge_split[style][keys]["source_node"].to(node_emb.device)
                dst = edge_split[style][keys]["target_node"].to(node_emb.device)
                neg_dst = edge_split[style][keys]["target_node_neg"].to(node_emb.device)
                results.append((style, keys,\
                    compute_mrr(
                        model, evaluator, node_emb, src, dst, neg_dst, device
                    )))
                print(results)
        # Duplicating results    
                #results.append(results[-1])    
    print(results)            
    return results

def evaluate_and_save(args, device, graph, nodes, model, feature, old_to_new, batch_size,  emb_path):
    with torch.no_grad():
        wrapped_feature= WrapMissingFeatures(old_to_new.to(device), model.empty, feature,\
             args.normalize, args.no_empty)
        node_emb = model.inference(graph, device, batch_size, wrapped_feature, old_to_new)
        np.save(f"{emb_path}/EMBEDDING", node_emb[nodes].numpy())
        print("embeddings generated")


def train(args, device, g, reverse_eids, seed_edges, model, features, save_path, old_to_new):
    # create sampler & dataloader
    print("Start training")
    #sampler = NeighborSampler([15, 10, 5], prefetch_node_feats=["feat"])
    sampler = NeighborSampler([15, 10])
    sampler = as_edge_prediction_sampler(
        sampler,
        exclude="reverse_id",
        reverse_eids=reverse_eids,
        negative_sampler=negative_sampler.Uniform(1),
    )
    print("Create dataloader")
    use_uva = args.mode == "mixed"
    print(g)
    dataloader = DataLoader(
        g,
        seed_edges,
        sampler,
        device=device,
        batch_size=256,
        shuffle=True,
       drop_last=False,
        num_workers=0,
        use_uva=use_uva,
    )
    print("Done with Dataloader")
    opt = torch.optim.Adam(model.parameters(), lr=0.0005)
    print("Wrap Features") 
    wrapped_feature = WrapMissingFeatures(old_to_new.to(device), model.empty, features, \
        args.normalize, args.no_empty)

    for epoch in range(7):
        model.train()
        total_loss = 0
        t1 = time.time()
        for it, (input_nodes, pair_graph, neg_pair_graph, blocks) in tqdm.tqdm(enumerate(
            dataloader
        )):
            #x = blocks[0].srcdata["feat"]
            x = wrapped_feature.get_device_features(input_nodes)
            #x = gather_pinned_tensor_rows(features, input_nodes)
            #x = features[input_nodes.to(features.device)].to(device)
            pos_score, neg_score = model(pair_graph, neg_pair_graph, blocks, x)
            score = torch.cat([pos_score, neg_score])
            pos_label = torch.ones_like(pos_score)
            neg_label = torch.zeros_like(neg_score)
            labels = torch.cat([pos_label, neg_label])
            loss = F.binary_cross_entropy_with_logits(score, labels)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total_loss += loss.item()
            if it % 1000:
                torch.save(model.state_dict(), save_path)
        print("Total loss", total_loss)
        t2 = time.time()

        torch.save(model.state_dict(), save_path)
        print("Epoch {:05d}, Time: {:.4f}| Loss {:.4f}".format(epoch,t2-t1, total_loss / (it + 1)))
    print("All training complete, returning")
