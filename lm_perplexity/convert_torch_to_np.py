import sys, os, torch, numpy as np, argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--model_name')
	parser.add_argument('--bin_num')
	parser.add_argument('--experiment_name')
	parser.add_argument('--torch_save_dir', default='log_calculations/torch_outputs/')
	parser.add_argument('--write_dir', default='log_calculations/np_probs/')
	parser.add_argument('--max_seq_len', type=int, default=128)
	parser.add_argument('--sample_size', type=int)

	args = parser.parse_args()

	
	log_dir = os.path.join(args.torch_save_dir, args.experiment_name, args.model_name)

	index = os.path.join(log_dir, f'{args.bin_num}_index.tsv')
	probs = os.path.join(log_dir, f'{args.bin_num}_log_probs.pt')

	probs = torch.load(probs)

	padded_np_array = np.array([np.lib.pad(np.asarray(prob), (0, args.max_seq_len - len(prob)), 'constant', constant_values=np.nan) for prob in probs])

	write_dir_model = os.path.join(args.write_dir, args.experiment_name, args.model_name)

	if not os.path.exists(write_dir_model):
		os.makedirs(write_dir_model)

	np.save(os.path.join(write_dir_model, f'{args.bin_num}_log_probs.npy'), padded_np_array)