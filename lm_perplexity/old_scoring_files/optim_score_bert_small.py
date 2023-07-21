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

	return masked_input, labels, attention_mask

if __name__ == '__main__':

	bin_num = int(sys.argv[1])

	cap = 50

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
	attention_masks = []

	for inpid in tqdm(tokenized_abstracts):
		m, l, a = get_inputs(inpid, tokenizer.vocab_size)
		masked_inputs.append(m)
		labels.append(l)
		attention_masks.append(a)


	model = AutoModelForMaskedLM.from_pretrained(model_name)
	model = model.to('cuda:0')

	sm = torch.nn.Softmax(dim=2)

	pidx_range = torch.arange(1,128).unsqueeze(1)
	pidx_base = torch.hstack((pidx_range, pidx_range))
	pidx_base = pidx_base.to('cuda:0')

	probs = []

	for inp, label, raw_tokens, attn_mask in tqdm(zip(masked_inputs, labels, tokenized_abstracts, attention_masks), total=len(labels)):

		# if len(raw_tokens) >= 128:
		# 	continue

		# print(raw_tokens)
		# print(inp)
		inp = inp.to('cuda:0')
		attn_mask = attn_mask.to('cuda:0')

		pidx_s = torch.tensor(raw_tokens[1:-1]).unsqueeze(1).to('cuda:0')
		pidx = torch.hstack((pidx_base[:len(pidx_s)], pidx_s))


		# prob_idx = torch.zeros((inp.shape[0], inp.shape[1], tokenizer.vocab_size),dtype=bool )
		# for i in range(len(raw_tokens[1:-1])):
		# 	prob_idx[i][i+1][raw_tokens[i+1]] = True

		# prob_idx = prob_idx.to('cuda:0')

		with torch.inference_mode():
			logits = model(inp, attention_mask=attn_mask).logits
			prob = sm(logits)
			taken_probs = prob[pidx[:,0],pidx[:,1],pidx[:,2]]
			
			probs.append(torch.log(taken_probs).cpu())
		# break
		
	
	# print(probs)

	if not os.path.exists(f'log_calculations_final/small/{model_name}'):
		os.makedirs(f'log_calculations_final/small/{model_name}')

	with open(f'log_calculations_final/small/{model_name}/{bin_num}_index.tsv', 'w') as f:
		for cid, abstract, tokens in zip(cids, abstracts, tokenized_abstracts):
			f.write(f'{cid}\t{abstract}\t{tokens}\n')

	torch.save(probs, f'log_calculations_final/small/{model_name}/{bin_num}_log_probs.pt')

	#Checks

	if len(cids) != len(abstracts):
		print('cid != abstracts')
	if len(tokenized_abstracts) != len(abstracts):
		print('tokens != abstracts')

	for inp_ids, prob in zip(tokenized_abstracts, probs):
		if len(inp_ids) != prob.shape[0] + 2:
			print('error')
		
	

"""
[101, 1109, 1160, 23690, 6126, 1678, 1487, 4248, 170, 23563, 1116, 25982, 14964, 21361, 4048, 1104, 1103, 7876, 6708, 10311, 1103, 1329, 1104, 170, 2702, 118, 2917, 24585, 119, 17781, 118, 19193, 1609, 4646, 1241, 3242, 118, 1191, 1178, 1195, 1169, 1525, 1800, 3014, 1536, 1106, 4392, 1103, 171, 7637, 20497, 4704, 1104, 1103, 9584, 1443, 8179, 119, 1130, 1861, 13585, 117, 1113, 3674, 2625, 1195, 3858, 1115, 20443, 1110, 5219, 1106, 2999, 117, 7930, 1441, 2479, 8290, 117, 1105, 8290, 1441, 7930, 119, 1109, 23483, 1106, 1107, 15174, 131, 107, 1262, 1225, 1152, 1686, 11786, 1518, 1170, 136, 107, 1538, 1129, 12172, 1193, 13672, 119, 102]
tensor([[ 103, 1109, 1160,  ...,    0,    0,    0],
        [ 101,  103, 1160,  ...,    0,    0,    0],
        [ 101, 1109,  103,  ...,    0,    0,    0],
        ...,
        [ 101, 1109, 1160,  ...,  103,    0,    0],
        [ 101, 1109, 1160,  ...,    0,  103,    0],
        [ 101, 1109, 1160,  ...,    0,    0,  103]])
  1%|█                                                                                                                                                                           | 3/500 [00:00<01:07,  7.41it/s]
[tensor([-3.5865e-01, -1.4638e+00, -5.2522e-01, -3.6107e-03, -2.3264e+00,
        -2.8651e-01, -2.3455e+00, -7.3070e-02, -2.1527e-01, -8.8721e-03,
        -4.9473e-05, -5.1500e-05, -9.7614e-03, -4.0115e+00, -4.2124e-02,
        -1.7793e-01, -7.5490e+00, -2.0592e+00, -8.5033e+00, -5.0871e-02,
        -4.0490e+00, -3.4503e-03, -2.2254e+00, -1.0169e+00, -5.9718e-04,
        -3.6894e+00, -7.6535e+00, -1.1915e-01, -6.8571e-01, -2.5460e-04,
        -1.6182e+00, -1.7811e+00, -7.7696e+00, -2.1907e-01, -5.2578e+00,
        -2.5937e+00, -8.7307e-01, -5.0565e-02, -1.1367e+00, -1.7133e+00,
        -1.8189e-01, -4.6736e+00, -7.2074e+00, -1.0300e-04, -1.7807e-03,
        -4.4015e+00, -3.1555e-02, -3.8804e-04, -9.2723e-02, -1.0567e-03,
        -2.4812e+00, -4.0730e-01, -5.4035e-01, -4.3265e+00, -1.7910e+00,
        -6.4957e+00, -2.6347e-02, -2.5250e-03, -2.5386e+00, -2.8471e+00,
        -8.9128e-03, -2.0557e-01, -3.4383e-01, -5.6836e+00, -7.9125e-03,
        -2.6561e+00, -9.5279e-02, -8.0056e+00, -2.1746e-01, -3.3742e+00,
        -1.0437e-02, -2.7846e+00, -1.5925e+00, -1.0051e+00, -1.1569e-01,
        -1.4997e+00, -3.6574e+00, -3.4979e+00, -4.3708e-02, -5.1904e+00,
        -6.5173e-01, -7.5452e+00, -2.1826e-02, -6.7008e-02, -4.8388e-01,
        -1.5273e-03, -6.7240e-02, -5.1015e-02, -1.2930e+00, -8.2956e-04,
        -3.7166e+00, -3.0291e+00, -1.1237e+00, -1.5504e-02, -5.5922e-02,
        -3.9746e-04, -1.1588e-03, -1.4038e-02, -7.4265e-04, -6.6582e-01,
        -4.1239e-03, -3.9823e+00, -1.4804e-02, -1.5965e+00, -7.2026e-02])]

"""



	