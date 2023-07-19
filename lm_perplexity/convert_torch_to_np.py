import sys, os, torch, numpy as np

if __name__ == '__main__':

	model_name = sys.argv[1]
	bin_num = sys.argv[2]
	write_dir = sys.argv[3]

	
	log_dir = os.path.join('log_calculations_final/', model_name)

	index = os.path.join(log_dir, f'{bin_num}_index.tsv')
	probs = os.path.join(log_dir, f'{bin_num}_log_probs.pt')

	probs = torch.load(probs)

	max_len = 128

	padded_np_array = np.array([np.lib.pad(np.asarray(prob), (0, max_len - len(prob)), 'constant', constant_values=np.nan) for prob in probs])

	write_dir_model = os.path.join(write_dir, model_name)
	if not os.path.exists(write_dir_model):
		os.makedirs(write_dir_model)

	np.save(os.path.join(write_dir_model, f'{bin_num}_log_probs.npy'), padded_np_array)