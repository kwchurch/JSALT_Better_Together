#!/bin/bash


for bin in {0..99..10} 99; do

	echo ${bin} ${model}
	
	python optim_score_bert_large.py \
	--bin_num ${bin} \
	--model_name allenai/scibert_scivocab_cased \
	--experiment_name every_5_5000 \
	--strip_newlines \
	--sample_size 5000 \
	--local_experiment_name pretraining_test \
	--local_model_name bins_10_to_30 \
	--use_local_model
done;

for bin in {5..99..10}; do

	echo ${bin} ${model}
	
	python optim_score_bert_large.py \
	--bin_num ${bin} \
	--model_name allenai/scibert_scivocab_cased \
	--experiment_name every_5_5000 \
	--strip_newlines \
	--sample_size 5000 \
	--local_experiment_name pretraining_test \
	--local_model_name bins_10_to_30 \
	--use_local_model
done;
