import sys, os, numpy as np, argparse


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--model_name')
	parser.add_argument('--experiment_name')
	parser.add_argument('--experiment_name_addon', default='')
	parser.add_argument('--np_dir', default='log_calculations/np_probs/')
	parser.add_argument('--write_dir', default='log_calculations/outputs/')
	parser.add_argument('--filter_nan', action='store_const', const=True, default=False)
	parser.add_argument('--nan_tolerance', type=int, default=2, help='Keep rows with only at most [nan_tolerance] number of nans/padded tokens up to max_seq_len')
	parser.add_argument('--sample_size', type=int)

	args = parser.parse_args()

	read_dir = os.path.join(args.np_dir, args.experiment_name, args.model_name)

	bins = range(100)

	all_sums = np.empty((100, args.sample_size), dtype='float')
	all_sums[:] = np.nan

	token_counts = np.zeros((100), dtype='int32')

	for bin_num in bins:

		bin_file = os.path.join(read_dir, f'{bin_num}_log_probs.npy')

		if not os.path.exists(bin_file):
			print(f'Bin:{bin_num:3d}')
			continue

		log_probs = np.load(bin_file)

		if args.filter_nan:
			print(f'Filtering rows with nan out. Starting shape: {log_probs.shape}')
			log_probs = log_probs[~(np.sum(np.isnan(log_probs), axis=1) > args.nan_tolerance), :]
			print(f'End shape: {log_probs.shape}')

		sum_log_probs = np.nansum(log_probs, axis=1)
		sum_log_probs = np.pad(sum_log_probs, (0, args.sample_size - sum_log_probs.shape[0]), constant_values=np.nan)

		all_sums[bin_num] = sum_log_probs

		token_counts[bin_num] = np.sum(~np.isnan(log_probs))
		
		print(f'Bin:{bin_num:3d}\tSize:{len(sum_log_probs):5d}')

	connector = '_' if len(args.experiment_name_addon) > 0 else ''
	experiment_name = args.experiment_name + connector + args.experiment_name_addon
	plot_model_dir = os.path.join(args.write_dir, experiment_name, args.model_name)

	if not os.path.exists(plot_model_dir):
		os.makedirs(plot_model_dir)


	np.save(os.path.join(plot_model_dir, f'lpsz.npy'), all_sums)
	np.save(os.path.join(plot_model_dir, f'token_counts.npy'), token_counts)


	#Do PPPL calculation

	num_zero_sums = np.sum(all_sums == 0.0, axis=1)
	token_counts = token_counts - num_zero_sums

	all_sums[all_sums == 0.0] = np.nan

	bin_sums = np.nansum(all_sums, axis=1) * -1
	exp_avg = np.exp(bin_sums / token_counts)

	np.save(os.path.join(plot_model_dir, f'pppl.npy'), exp_avg)
