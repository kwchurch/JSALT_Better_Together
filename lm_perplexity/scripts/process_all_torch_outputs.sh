#!/bin/bash

# for experiment in filter_newline; do
# 	for model in bert-base-cased bert-large-cased roberta-base allenai/scibert_scivocab_cased; do 
# 		echo ${experiment} ${model}
# 		python process_torch_outputs.py \
# 			--experiment_name ${experiment} \
# 			--model_name ${model}
# 	done; done

for experiment in multilingual; do
	for model in bert-base-multilingual-cased xlm-roberta-base; do
		echo ${experiment} ${model}
		python process_torch_outputs.py \
			--experiment_name ${experiment} \
			--model_name ${model}
	done; done