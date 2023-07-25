import sys, os, argparse, pandas, numpy as np, torch, logging
from transformers import AutoTokenizer
from langdetect import detect
from tqdm import tqdm

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--torch_dir', default='log_calculations/torch_outputs/')
	parser.add_argument('--output_dir', default='log_calculations/unifed_outputs/')
	parser.add_argument('--experiment_name')
	parser.add_argument('--experiment_name_addon', default='')
	parser.add_argument('--model_name')
	parser.add_argument('--sample_size', default=None)
	parser.add_argument('--max_seq_len', default=128)
	parser.add_argument('--minimum_characters', default=75, help='Remove abstracts with less than [minimum_characters] characters')
	parser.add_argument('--max_padding_tokens', default=2, help='Remove abstracts with more than [max_padding_tokens] [PAD] tokens')
	parser.add_argument('--minimum_unique_characters', default=20, help='Remove abstracts with less than [minimum_unique_characters] unique characters')
	parser.add_argument('--skip_lang_detect', action='store_const', const=True, default=False)
	parser.add_argument('--do_not_overwrite', action='store_const', const=True, default=False)

	args = parser.parse_args()

	# Setup logging

	ename_addon = '_' + args.experiment_name_addon if len(args.experiment_name_addon) > 0 else ''
	write_dir = os.path.join(args.output_dir, args.experiment_name, ename_addon, args.model_name)

	if not os.path.exists(write_dir):
		os.makedirs(write_dir)
	elif args.do_not_overwrite:
		print('Directory exists, exiting.')
		quit(1)

	logging.root.handlers = []
	# noinspection PyArgumentList
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s [%(levelname)s] %(message)s",
		handlers=[
			logging.FileHandler("{}/{}.log".format(write_dir, f'process_torch_outputs')),
			logging.StreamHandler()
		]
	)

	logging.info(args)

	tokenizer = AutoTokenizer.from_pretrained(args.model_name)

	torch_outputs_dir = os.path.join(args.torch_dir, args.experiment_name, args.model_name)

	loaded_data = {}

	records = []

	if not args.sample_size:
		for bin_num in range(100):
			index_file = os.path.join(torch_outputs_dir, f'{bin_num}_index.tsv')
			if not os.path.isfile(index_file):
				continue
			torch_outputs = torch.load(os.path.join(torch_outputs_dir, f'{bin_num}_log_probs.pt'))
			sample_size = len(torch_outputs)
			break
	else:
		sample_size = args.sample_size
	logging.info(f'Detected sample size: {sample_size}')

	all_log_probs = np.empty((100, sample_size, args.max_seq_len), dtype='float')
	all_log_probs[:] = np.nan

	for bin_num in range(100):

		index_file = os.path.join(torch_outputs_dir, f'{bin_num}_index.tsv')
		if not os.path.isfile(index_file):
			continue

		with open(index_file, 'r') as f:
			for i, line in enumerate(f):
				splits = line.strip().split('\t')
				records.append(
					{'bin' : bin_num,
					'local_id' : i,
					'corpusid' : splits[0],
					'abstract' : splits[1],
					'tokens' : splits[2]
					}
				)
		
		torch_outputs = torch.load(os.path.join(torch_outputs_dir, f'{bin_num}_log_probs.pt'))
		assert len(torch_outputs) == i+1

		padded_np_array = np.array([np.lib.pad(np.asarray(prob), (0, args.max_seq_len - len(prob)), 'constant', constant_values=np.nan) for prob in torch_outputs])
		all_log_probs[bin_num] = padded_np_array

	tqdm.pandas()
	df = pandas.DataFrame.from_records(records)

	#Find and remove abstracts which are under the minimum character limit, and nan out corresponding values in np array
	short_char_df = df[df['abstract'].str.len() < args.minimum_characters]
	all_log_probs[short_char_df['bin'].values, short_char_df['local_id'].values] = np.nan
	df = df[df['abstract'].str.len() >= args.minimum_characters]

	logging.info('Removed following abstracts due to minimum character limit:')
	logging.info(short_char_df)

	# Find and remove abstracts with less than 20 unique characters, and nan out corresponding values in np array
	df['num_unique_tokens'] = df['abstract'].apply(lambda x : len(set(x)))
	low_unique_chars_df = df[df['num_unique_tokens'] <= args.minimum_unique_characters]
	all_log_probs[low_unique_chars_df['bin'].values, low_unique_chars_df['local_id'].values] = np.nan
	df = df[df['num_unique_tokens'] > args.minimum_unique_characters]

	logging.info('Removed following abstracts due to low number of unique characters:')
	logging.info(low_unique_chars_df)

	df['num_total_tokens'] = df['tokens'].str.count(',') + 1
	df['num_unk_tokens'] = df['tokens'].str.count(', ' + str(tokenizer.unk_token_id) + ',')

	# Find and remove abstracts with too many pad tokens, and nan out corresponding values in np array
	high_pad_count_df = df[df['num_total_tokens'] <= (args.max_seq_len - args.max_padding_tokens)]
	all_log_probs[high_pad_count_df['bin'].values, high_pad_count_df['local_id'].values] = np.nan
	df = df[df['num_total_tokens'] > (args.max_seq_len - args.max_padding_tokens)]

	logging.info('Removed following abstracts due to too many pad tokens:')
	logging.info(high_pad_count_df)

	if not args.skip_lang_detect:
		logging.info('Detecting language')
		df['langdetect'] = df['abstract'].progress_apply(lambda x : detect(x))


	#### Start PPPL Calculation ####

	#Get token counts per bin
	bin_token_counts = np.sum(~np.isnan(all_log_probs.reshape((100, -1))), axis=-1) # (100,)

	# Calculate PLL for each abstract
	pll = np.nansum(all_log_probs, axis=2)
	bin_pll_sum = np.nansum(pll, axis=1) * -1
	pppl = np.exp(bin_pll_sum / bin_token_counts)

	print(all_log_probs.shape)
	#Save Outputs
	# np.save(os.path.join(write_dir, f'pppl.npy'), pppl)
	# np.save(os.path.join(write_dir, f'token_counts.npy'), bin_token_counts)
	# np.save(os.path.join(write_dir, f'filtered_log_probs.npy'), all_log_probs)
	# df.to_csv(os.path.join(write_dir, f'filtered_df.csv'))
	



	

	

	