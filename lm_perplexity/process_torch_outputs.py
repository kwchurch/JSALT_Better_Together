import sys, os, argparse, pandas, numpy as np, torch
from transformers import AutoTokenizer
from langdetect import detect

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--torch_dir', default='log_calculations/torch_outputs/')
	parser.add_argument('--experiment_name')
	parser.add_argument('--model_name')
	parser.add_argument('--sample_size', default=1000)
	parser.add_argument('--max_seq_len', default=128)
	parser.add_argument('--minimum_characters', default=75, help='Remove abstracts with less than 75 characters')
	parser.add_argument('--filter_nan', action='store_const', default=False, const=True)
	parser.add_argument('--nan_tolerance', type=int, default=2, help='Keep rows with at most 2 nan input ids (tokenizer dependant)')

	args = parser.parse_args()

	tokenizer = AutoTokenizer.from_pretrained(args.model_name)

	torch_outputs_dir = os.path.join(args.torch_dir, args.experiment_name, args.model_name)

	loaded_data = {}

	records = []

	all_log_probs = np.empty((100, args.sample_size, args.max_seq_len), dtype='float')
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
		padded_np_array = np.array([np.lib.pad(np.asarray(prob), (0, args.max_seq_len - len(prob)), 'constant', constant_values=np.nan) for prob in torch_outputs])
		all_log_probs[bin_num] = padded_np_array

				
	df = pandas.DataFrame.from_records(records)

	#Get abstracts which are under the minimum limit
	short_char_df = df[df['abstract'].str.len() < args.minimum_characters]

	#Remove from numpy array
	all_log_probs[short_char_df['bin'].values, short_char_df['local_id'].values] = np.nan
	df = df[df['abstract'].str.len() >= args.minimum_characters]
	

	