import os, sys, argparse, orjson, torch, numpy as np

from tqdm import tqdm, trange

from transformers import AutoModelForMaskedLM, AutoTokenizer

def get_inputs(input_ids, vocab_size):

	x = torch.tensor(input_ids)

	repeats = x.repeat(x.shape[-1] - 2, 1)
	mask = torch.ones(x.shape[-1] - 1).diag(1)[:-2]

	masked_input = repeats.masked_fill(mask == 1, tokenizer.mask_token_id)
	labels = repeats.masked_fill(masked_input != tokenizer.mask_token_id, -100)

	return masked_input, labels

if __name__ == '__main__':

	bin_num = int(sys.argv[1])

	cap = 500

	bin_samples_dir = 'sampling/bin_samples/'

	abstracts = []
	cids = []

	with open(os.path.join(bin_samples_dir, f'{bin_num:03d}')) as input_sample:
		for line in input_sample.readlines()[:cap]:
			dat = orjson.loads(line)
			abstracts.append(dat['abstract'])
			cids.append(dat['corpusid'])

	model_name = 'bert-base-cased'

	tokenizer = AutoTokenizer.from_pretrained(model_name)
	tokenized_abstracts = tokenizer(abstracts, truncation=True, max_length=128)['input_ids']

	masked_inputs = []
	labels = []

	for inpid in tqdm(tokenized_abstracts):
		m, l = get_inputs(inpid, tokenizer.vocab_size)
		masked_inputs.append(m)
		labels.append(l)


	model = AutoModelForMaskedLM.from_pretrained(model_name)
	model = model.to('cuda:0')

	sm = torch.nn.Softmax(dim=2)

	probs = []

	for inp, label, raw_tokens in tqdm(zip(masked_inputs, labels, tokenized_abstracts), total=len(labels)):

		print(raw_tokens)
		print(inp)

		inp = inp.to('cuda:0')
		label = label.to('cuda:0')

		prob_idx = torch.zeros((inp.shape[0], inp.shape[1], tokenizer.vocab_size),dtype=bool )
		for i in range(len(raw_tokens[1:-1])):
			prob_idx[i][i+1][raw_tokens[i+1]] = True

		prob_idx = prob_idx.to('cuda:0')

		with torch.inference_mode():
			logits = model(inp, labels=label).logits
			prob = sm(logits)
			taken_probs = prob[prob_idx]
			
			probs.append(torch.log(taken_probs).cpu())

		print(probs[-1]) 
	
	print(probs)
	quit(1)

	if not os.path.exists(f'log_calculations_final/{model_name}'):
		os.makedirs(f'log_calculations_final/{model_name}')

	with open(f'log_calculations_final/{model_name}/{bin_num}_index.tsv', 'w') as f:
		for cid, abstract, tokens in zip(cids, abstracts, tokenized_abstracts):
			f.write(f'{cid}\t{abstract}\t{tokens}\n')

	torch.save(probs, f'log_calculations_final/{model_name}/{bin_num}_log_probs.pt')

	#Checks

	if len(cids) != len(abstracts):
		print('cid != abstracts')
	if len(tokenized_abstracts) != len(abstracts):
		print('tokens != abstracts')

	for inp_ids, prob in zip(tokenized_abstracts, probs):
		if len(inp_ids) != prob.shape[0] + 2:
			print('error')
		
	





	