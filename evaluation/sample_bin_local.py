import argparse, scipy, os, sys, pandas, random
from collections import Counter
from tqdm import tqdm
from utils import get_all_previous_bin_ids, get_bin_ids

from joblib import Parallel, delayed

def count_ref(idx):
	references = citation_graph[idx].indices
	reference_bins = []
	if len(references) > 0:
		for ref_id in references:
			reference_bins.append(id_to_bin.get(ref_id, -1))

	return reference_bins


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--shard_id', type=int)
	parser.add_argument('--shard_size', type=int, default=10)
	parser.add_argument('--total_bins', type=int, default=100)
	parser.add_argument('--sample_size', type=int, default=-1)
	parser.add_argument('--seed', type=int, default=42)
	parser.add_argument('--subgraph_dir', type=str, default='/rc_scratch/abeb4417/jsalt/semantic_scholar/j.ortega/graphs.V2/')
	parser.add_argument('--cumgraph_dir', type=str, default='/rc_scratch/abeb4417/jsalt/semantic_scholar/j.ortega/cumgraphs.V2/')
	parser.add_argument('--citation_graph', type=str, default='/rc_scratch/abeb4417/jsalt/semantic_scholar/releases/2022-12-02/database/citations/graphs/citations.G.npz')
	parser.add_argument('--smoke_test', action='store_true', default=False)

	args = parser.parse_args()


	bins = [i for i in range(args.total_bins)]
	shards = [bins[i:i+args.shard_size] for i in range(0, args.total_bins, args.shard_size)]
	shard_ids = shards[args.shard_id]

	print(f'With {args.total_bins} total bins, \
	and a shard size of {args.shard_size}, \
	we are looking at shard {args.shard_id}, \
	which contains {shard_ids}')


	graph_file = os.path.join(args.cumgraph_dir, '015.npz') if args.smoke_test else args.citation_graph
	print('Loading citation graph')
	citation_graph = scipy.sparse.load_npz(graph_file)

	max_bin = 5 if args.smoke_test else 100
	sample_size = 500 if args.smoke_test else args.sample_size

	print('Loading previous bin ids')
	id_to_bin = get_all_previous_bin_ids(max_bin, args.subgraph_dir)

	for bin_id in shard_ids:

		records = []
				
		current_bin_ids = get_bin_ids(bin_id, args.subgraph_dir)
		reference_bin_ids = []

		errors = []
		
		c = Counter()

		random.seed(args.seed)
		random.shuffle(current_bin_ids)

		for idx in tqdm(current_bin_ids[:sample_size]):
			
			references = citation_graph[idx].indices
			if len(references) > 0:
			
				for ref_id in references:
					ref_bin_id = id_to_bin.get(ref_id, -1)
					c[ref_bin_id] += 1

					if ref_bin_id > bin_id:
						errors.append((bin_id, ref_bin_id, idx, ref_id))
						# errors.append(f'{args.bin_id}\t{ref_bin_id}\t{idx}\t{ref_id}\n')

		records.append({'bin_id' : bin_id} | {i : c[i] for i in range(-1, max_bin)})

		df = pandas.DataFrame.from_records(records)
		df.to_csv(f'bin_to_bin/bin_{bin_id}_{sample_size}_{args.seed}.tsv', sep='\t')

		errors.sort(key=lambda x : x[1])

		with open(f'bin_to_bin/errors_{bin_id}_{sample_size}_{args.seed}.tsv', 'w') as f:
			for e in errors:
				f.write(f'{e[0]}\t{e[1]}\t{e[2]}\t{e[3]}\n')