#! /bin/bash
python continue_pretraining.py \
	--experiment_name pretraining_test \
	--starting_model_name allenai/scibert_scivocab_cased \
	--adapted_model_name bins_10_to_30 \
	--bin_min 10 --bin_max 31 \
