import os, sys, argparse, orjson, torch, numpy as np

from tqdm import tqdm, trange

from transformers import AutoModelForMaskedLM, AutoTokenizer

def get_inputs(input_ids, vocab_size, max_len=128):

	x = torch.tensor(input_ids + [tokenizer.pad_token_id] * (128 - len(input_ids)))
	attention_mask = torch.tensor([1] * len(input_ids) + [0] * (128 - len(input_ids)))
	attention_mask = attention_mask.repeat(attention_mask.shape[-1], 1)

	repeats = x.repeat(x.shape[-1], 1)
	mask = torch.ones(x.shape[-1]).diag(0)

	masked_input = repeats.masked_fill(mask == 1, tokenizer.mask_token_id)
	labels = repeats.masked_fill(masked_input != tokenizer.mask_token_id, -100)

	return x, masked_input, labels, attention_mask

if __name__ == '__main__':

	bin_num = int(sys.argv[1])

	cap = 500
	batch_size = 32

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
	padded_inputs = []
	labels = []
	attention_masks = []
	lengths = []

	for inpid in tqdm(tokenized_abstracts):
		padded_input, m, l, a = get_inputs(inpid, tokenizer.vocab_size)
		padded_inputs.append(padded_input)
		masked_inputs.append(m)
		labels.append(l)
		attention_masks.append(a)
		lengths.append(len(inpid))


	model = AutoModelForMaskedLM.from_pretrained(model_name)
	model = model.to('cuda:0')

	sm = torch.nn.Softmax(dim=2)

	num_batches = 128 // batch_size

	pidx_seq_range = torch.arange(0,128).unsqueeze(1)
	pidx_batch_range = torch.arange(0,batch_size).repeat(num_batches).unsqueeze(1)


	pidx_base = torch.hstack((pidx_batch_range, pidx_seq_range))
	pidx_base = pidx_base.to('cuda:0')

	probs = []

	for inp, label, raw_tokens, attn_mask, length, padded_input in tqdm(zip(masked_inputs, labels, tokenized_abstracts, attention_masks, lengths, padded_inputs), total=len(labels)):

		inp = inp.to('cuda:0')
		attn_mask = attn_mask.to('cuda:0')

		pidx_s = padded_input.unsqueeze(1).to('cuda:0')
		pidx = torch.hstack((pidx_base[:len(pidx_s)], pidx_s))

		inp_batches = inp.split(batch_size, dim=0)
		pidx_batches = pidx.split(batch_size, dim=0)
		am_batches = attn_mask.split(batch_size, dim=0)

		batch_probs = []

		for bidx in range(num_batches):
			with torch.inference_mode():
				logits = model(inp_batches[bidx], attention_mask=am_batches[bidx]).logits
				prob = sm(logits)
				taken_probs = prob[pidx_batches[bidx][:,0],pidx_batches[bidx][:,1],pidx_batches[bidx][:,2]]
				
				batch_probs.append(torch.log(taken_probs).cpu())

		probs.append(torch.cat(batch_probs)[1:length-1])

	if not os.path.exists(f'log_calculations_final/large/{model_name}'):
		os.makedirs(f'log_calculations_final/large/{model_name}')

	with open(f'log_calculations_final/large/{model_name}/{bin_num}_index.tsv', 'w') as f:
		for cid, abstract, tokens in zip(cids, abstracts, tokenized_abstracts):
			f.write(f'{cid}\t{abstract}\t{tokens}\n')

	torch.save(probs, f'log_calculations_final/large/{model_name}/{bin_num}_log_probs.pt')

	#Checks

	if len(cids) != len(abstracts):
		print('cid != abstracts')
	if len(tokenized_abstracts) != len(abstracts):
		print('tokens != abstracts')

	for inp_ids, prob in zip(tokenized_abstracts, probs):
		if len(inp_ids) != prob.shape[0] + 2:
			print('error')
		
	