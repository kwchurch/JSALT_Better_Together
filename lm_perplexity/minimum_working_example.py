import numpy as np
import torch
import os, sys, argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--bin_num', type=int)
	parser.add_argument('--log_prob_dir', default='log_calculations_final/')
	parser.add_argument('--model_name', default='allenai/scibert_scivocab_cased')
	parser.add_argument('--max_len', default=128)

	args = parser.parse_args()

	# Load log probabilites from model outputs
	# one file per bin, list of tensors of variable length
	log_probs_file = os.path.join(args.log_prob_dir, args.model_name, f'{args.bin_num}_log_probs.pt')
	log_probs = torch.load(log_probs_file)

	# Convert variable length tensors to numpy array padded with np.nan
	# Shape 10,000 x 128, contains per_subword log probabilities
	padded_np_array = np.array([np.lib.pad(np.asarray(prob), (0, args.max_len - len(prob)), 'constant', constant_values=np.nan) for prob in log_probs])

	# Sum the log probabilities to get psuedo log likelihood for each sample abstract
	# Shape 10,000,1
	ppl_per_abstract = np.nansum(padded_np_array, axis=1)

	# Calculate corpus/bin token counts (i.e. non nan values), and remove number of abstracts which sum to 0 from count
	# (Scalar) since only one bin
	token_counts = np.sum(~np.isnan(padded_np_array)) - np.sum(ppl_per_abstract == 0.0)

	#Sum PPPL to get corpus/bin sum
	bin_ppl_sum = np.sum(ppl_per_abstract)

	# Negate and divide by total tokens in bin
	bin_ppl_sum = (-1 * bin_ppl_sum) / token_counts
	
	pppl = np.exp(bin_ppl_sum)

	print(f'PPPL: {pppl:.3f}')





