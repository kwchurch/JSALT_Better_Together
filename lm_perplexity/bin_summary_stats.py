import sys, os, numpy as np


if __name__ == '__main__':

	np_array_dir = 'log_calculations_final/np_probs/large/'

	model_name = sys.argv[1]
	sample_size = int(sys.argv[2])

	read_dir = os.path.join(np_array_dir, model_name)

	bins = range(100)

	filter_rows_with_nan = False
	row_nan_tolerance = 2 #Keep rows with at most tolerance number of nans

	all_sums = np.empty((100, sample_size), dtype='float')
	all_sums[:] = np.nan

	token_counts = np.zeros((100), dtype='int32')

	for bin_num in bins:

		bin_file = os.path.join(read_dir, f'{bin_num}_log_probs.npy')

		if not os.path.exists(bin_file):
			print(f'Bin:{bin_num:3d}')
			continue

		log_probs = np.load(bin_file)

		if filter_rows_with_nan:
			print(f'Filtering rows with nan out. Starting shape: {log_probs.shape}')
			log_probs = log_probs[~(np.sum(np.isnan(log_probs), axis=1) > row_nan_tolerance), :]
			print(f'End shape: {log_probs.shape}')

		sum_log_probs = np.nansum(log_probs, axis=1)
		sum_log_probs = np.pad(sum_log_probs, (0, sample_size - sum_log_probs.shape[0]), constant_values=np.nan)

		all_sums[bin_num] = sum_log_probs

		token_counts[bin_num] = np.sum(~np.isnan(log_probs))
		
		print(f'Bin:{bin_num:3d}\tSize:{len(sum_log_probs):5d}')


	plot_dir = 'log_calculations_final/plots/large/'
	plot_model_dir = os.path.join(plot_dir, model_name)

	if not os.path.exists(plot_model_dir):
		os.makedirs(plot_model_dir)


	np.save(os.path.join(plot_model_dir, f'lpsz.npy'), all_sums)
	np.save(os.path.join(plot_model_dir, f'token_counts.npy'), token_counts)


	#Do PPPL calculation

	# all_sums = all_sums[:83,:]
	# token_counts = token_counts[:83]

	num_zero_sums = np.sum(all_sums == 0.0, axis=1)
	token_counts = token_counts - num_zero_sums

	all_sums[all_sums == 0.0] = np.nan

	bin_sums = np.nansum(all_sums, axis=1) * -1
	exp_avg = np.exp(bin_sums / token_counts)

	np.save(os.path.join(plot_model_dir, f'pppl.npy'), exp_avg)
