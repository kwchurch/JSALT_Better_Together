#! /bin/bash
python continue_pretraining.py \
	--experiment_name pretraining_test \
	--starting_model_name allenai/scibert_scivocab_cased \
	--adapted_model_name bins_70_to_90 \
	--bin_min 70 --bin_max 90 \
