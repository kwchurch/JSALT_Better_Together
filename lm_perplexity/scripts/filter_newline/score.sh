#!/bin/bash

for model in bert-base-cased roberta-base allenai/scibert_scivocab_cased; do
	
	for bin in {0..99..10} 99; do

	echo ${bin} ${model}
	
	python optim_score_bert_large.py \
		--bin_num ${bin} \
		--model_name ${model} \
		--experiment_name filter_newline \
		--strip_newlines \
		--sample_size 1000 
	
	done; done
