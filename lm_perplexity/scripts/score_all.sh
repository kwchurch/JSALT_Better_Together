#!/bin/bash

for model in roberta-base xlm-roberta-base bert-base-multilingual-cased bert-large-cased; do 

	for bin in {0..99..5} 99; do

		echo ${bin} ${model}
		
		python optim_score_bert_large.py \
		--bin_num ${bin} \
		--model_name ${model} \
		--experiment_name every_5_5000 \
		--strip_newlines \
		--sample_size 5000 
	done; done
