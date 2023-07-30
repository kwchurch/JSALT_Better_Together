from transformers import AutoModelForMaskedLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from my_datasets.pretraining_datasets import PretrainingDataset
import os, sys, random, argparse, wandb


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--bin_min', type=int)
	parser.add_argument('--bin_max', type=int)
	parser.add_argument('--skip_first_k', type=int, default=7500)
	parser.add_argument('--starting_model_name', type=str)
	parser.add_argument('--adapted_model_name', type=str, default='default_adapted')
	parser.add_argument('--experiment_name', type=str, default='default_experiment')
	parser.add_argument('--sample_size', type=int, default=10000)
	parser.add_argument('--batch_size', type=int, default=32)
	parser.add_argument('--max_seq_len', type=int, default=128)
	parser.add_argument('--bin_samples_dir', type=str, default='sampling/bin_samples/')
	parser.add_argument('--write_dir', type=str, default='log_calculations/pretraining/')
	parser.add_argument('--strip_newlines', action='store_const', const=True, default=False)
	parser.add_argument('--minimum_chars', type=int, default=75)
	parser.add_argument('--minimum_unique_chars', type=int, default=10)
	
	args = parser.parse_args()

	#Load tokenizer

	wandb.init(project=args.experiment_name)

	tokenizer = AutoTokenizer.from_pretrained(args.starting_model_name)

	# Load data into dataset
	dataset = PretrainingDataset(
		bin_min = args.bin_min,
		bin_max = args.bin_max,
		skip_first_k = args.skip_first_k,
		sample_size = args.sample_size,
		bin_samples_dir = args.bin_samples_dir,
		tokenizer = tokenizer,
		filter_newline = True,
		min_characters = args.minimum_chars,
		min_unique_characters = args.minimum_unique_chars
	)

	model = AutoModelForMaskedLM.from_pretrained(args.starting_model_name)

	output_directory = os.path.join(args.write_dir, args.experiment_name, args.starting_model_name, args.adapted_model_name)
	training_arguments = TrainingArguments(output_dir=output_directory,
										   per_device_train_batch_size= 32,
											gradient_accumulation_steps= 1,
											learning_rate= 2.0e-5,
											num_train_epochs= 20,
											evaluation_strategy= 'no',
											warmup_ratio= .01,
											logging_steps= 25,
											save_steps= 20000,
											save_total_limit= 7)

	collator = DataCollatorForLanguageModeling(tokenizer, mlm=True, mlm_probability=0.15)

	trainer = Trainer(
		model=model,
		args=training_arguments,
		train_dataset=dataset,
		data_collator=collator
	)

	trainer.train()

	model.save_pretrained(os.path.join(output_directory, 'final_model'))
	print('Model saved in: {}'.format(output_directory))


