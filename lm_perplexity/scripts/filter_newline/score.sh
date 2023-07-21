#!/bin/bash

for model in bert-base-cased roberta-base allenai/scibert_scivocab_cased; do
	
	for bin in {0..99..5} 99; do

	python optim_score_bert_large.py \
		--bin_num ${bin} \
		--model_name ${model} \
		--experiment_name filter_newline \
		--sample_size 1000 
	done; done
