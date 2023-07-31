import torch, orjson, regex as re, os, sys
from transformers import AutoTokenizer
from torch.utils.data import Dataset
from tqdm import trange


class PretrainingDataset(Dataset):

	def __init__(self, bin_min, bin_max, skip_first_k, sample_size, bin_samples_dir, tokenizer, filter_newline, min_characters, min_unique_characters, pretokenize=True):
		
		self.bin_min = bin_min
		self.bin_max = bin_max
		self.bin_samples_dir = bin_samples_dir
		self.sample_size = sample_size
		self.tokenizer = tokenizer

		self.data = []
		self.cids = []

		whitespace_pat = re.compile(r'[\n|\t|\s]+')
		
		for bin_num in trange(bin_min, bin_max):
			with open(os.path.join(self.bin_samples_dir, f'{bin_num:03d}')) as input_sample:
				bin_data = []
				for i, line in enumerate(input_sample):

					if i < skip_first_k:
						continue
					

					if len(bin_data) >= self.sample_size:
						self.data.extend(bin_data)
						break

					dat = orjson.loads(line)
					abstract = dat['abstract']


					abstract = re.sub(whitespace_pat, ' ', abstract)
					if i == skip_first_k:
						print(abstract)
					if len(abstract) < min_characters or len(set(abstract)) < min_unique_characters:
						continue

					self.cids.append(dat['corpusid'])
					bin_data.append(abstract)

		print(f'Loaded {len(self.data)} examples.')

		if pretokenize:
			self.tokenized_data = self.tokenizer(text = self.data, padding='max_length', max_length=128, truncation=True, return_tensors='pt')
		else:
			self.tokenized_data = []

	def __len__(self):
		return len(self.data)

	def __getitem__(self, idx):
		return {
			'input_ids' : self.tokenized_data['input_ids'][idx],
			'token_type_ids' : self.tokenized_data['token_type_ids'][idx],
			'attention_mask' : self.tokenized_data['attention_mask'][idx]
		}
	
