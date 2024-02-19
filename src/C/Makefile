files=freq_row_piece freq_row check_order XY_to_bigrams gram_matrix \
	uniq_bigrams_by_hashing substream substream_records hist_bigrams bincount_bigrams split_binary_records check_bigrams extract_row lookup_bigram lookup_lbigram \
	cocitations floats_to_random_bytes floats_to_random_bytes_stats \
	index_random_bytes print_random_bytes_index print_floats_index calibrate_random_bytes_index invert_permutation \
	near near_with_floats faster_near_with_floats near_without_floats calibrate_random_bytes cbind_bytes \
	find_lines find_lines_nonnumeric aref summarize_index authors2matrix index_lines common_prefix char_hist score_with_floats \
	brute_force_with_floats idx_to_pairs pairs_to_cos find_in_sorted_lines score_pairs select_vectors id_to_floats create_years_vector venn filter_edges BFS \
	x_to_y vector_near_with_floats XY_data_to_bigrams bigrams_to_XY_data killroy generate_pairs_from_idx filter_records sum_bigrams sum_lbigrams nbest_bigrams authors_to_authors \
	print_bigrams unprint_bigrams sort_bigrams uniq_bigrams uniq_bigrams_by_hashing \
	print_lbigrams unprint_lbigrams sort_lbigrams uniq_lbigrams uniq_lbigrams_by_hashing center_floats invert_landmarks new_invert_landmarks

# random_bigrams 

all: ${files}

clean: 
	rm ${files}; rm *.o

util.o: util.c util.h
	cc -c util.c

freq_row_piece: freq_row_piece.c util.o
	cc -g -o freq_row_piece freq_row_piece.c util.o

freq_row: freq_row.c util.o
	cc -o freq_row freq_row.c util.o

check_order: check_order.c util.o
	cc -o check_order check_order.c util.o

XY_to_bigrams: XY_to_bigrams.c util.o
	cc -o XY_to_bigrams XY_to_bigrams.c util.o

gram_matrix: gram_matrix.c util.o
	cc -o gram_matrix gram_matrix.c util.o

substream: substream.c
	cc -o substream substream.c

substream_records: substream_records.c util.o
	cc -o substream_records substream_records.c util.o

hist_bigrams: hist_bigrams.c util.o
	cc -o hist_bigrams hist_bigrams.c util.o

bincount_bigrams: bincount_bigrams.c util.o
	cc -o bincount_bigrams bincount_bigrams.c util.o

check_bigrams: check_bigrams.c util.o
	cc -o check_bigrams check_bigrams.c util.o

split_binary_records: split_binary_records.c util.o
	cc -o split_binary_records split_binary_records.c util.o

extract_row: extract_row.c util.o
	cc -o extract_row extract_row.c util.o

lookup_bigram: lookup_bigram.c util.o
	cc -o lookup_bigram lookup_bigram.c util.o

lookup_lbigram: lookup_lbigram.c util.o
	cc -o lookup_lbigram lookup_lbigram.c util.o

random_bigrams: random_bigrams.c util.o
	cc -o random_bigrams random_bigrams.c util.o # -lssl -lcrypto

cocitations: cocitations.c util.o
	cc -o cocitations cocitations.c util.o

floats_to_random_bytes: floats_to_random_bytes.c util.o
	cc -o floats_to_random_bytes floats_to_random_bytes.c util.o -lm # -lssl -lcrypto

floats_to_random_bytes_stats: floats_to_random_bytes_stats.c util.o
	cc -o floats_to_random_bytes_stats floats_to_random_bytes_stats.c util.o -lm # -lssl -lcrypto

index_random_bytes: index_random_bytes.c util.o
	cc -o index_random_bytes index_random_bytes.c util.o

print_random_bytes_index: print_random_bytes_index.c util.o
	cc -o print_random_bytes_index print_random_bytes_index.c util.o

print_floats_index: print_floats_index.c util.o
	cc -o print_floats_index print_floats_index.c util.o -lm

calibrate_random_bytes_index: calibrate_random_bytes_index.c util.o
	cc -o calibrate_random_bytes_index calibrate_random_bytes_index.c util.o -lm

calibrate_random_bytes: calibrate_random_bytes.c util.o
	cc -o calibrate_random_bytes calibrate_random_bytes.c util.o -lm

invert_permutation: invert_permutation.c util.o
	cc -o invert_permutation invert_permutation.c util.o

near: near.c util.o
	cc -o near near.c util.o

near_with_floats: near_with_floats.c util.o
	cc -o near_with_floats near_with_floats.c util.o -lm

faster_near_with_floats: faster_near_with_floats.c util.o
	cc -o faster_near_with_floats faster_near_with_floats.c util.o -lm

near_without_floats: near_without_floats.c util.o
	cc -o near_without_floats near_without_floats.c util.o -lm

vector_near_with_floats: vector_near_with_floats.c util.o
	cc -o vector_near_with_floats vector_near_with_floats.c util.o -lm

score_with_floats: score_with_floats.c util.o
	cc -o score_with_floats score_with_floats.c util.o -lm

cbind_bytes: cbind_bytes.c util.o
	cc -o cbind_bytes cbind_bytes.c util.o

find_lines: find_lines.c util.o
	cc -o find_lines find_lines.c util.o

find_lines_nonnumeric: find_lines_nonnumeric.c util.o
	cc -o find_lines_nonnumeric find_lines_nonnumeric.c util.o

aref: aref.c util.o
	cc -o aref aref.c util.o

summarize_index: summarize_index.c util.o
	cc -o summarize_index summarize_index.c util.o -lm

authors2matrix: authors2matrix.c util.o
	cc -o authors2matrix authors2matrix.c util.o

index_lines: index_lines.c util.o
	cc -o index_lines index_lines.c util.o

common_prefix: common_prefix.c
	cc -o common_prefix common_prefix.c

char_hist: char_hist.c
	cc -o char_hist char_hist.c

brute_force_with_floats: brute_force_with_floats.c util.o
	cc -o brute_force_with_floats brute_force_with_floats.c util.o -lm

idx_to_pairs: idx_to_pairs.c util.o
	cc -o idx_to_pairs idx_to_pairs.c util.o

pairs_to_cos: pairs_to_cos.c util.o
	cc -o pairs_to_cos pairs_to_cos.c util.o -lm

id_to_floats: id_to_floats.c util.o
	cc -o id_to_floats id_to_floats.c util.o -lm

score_pairs: score_pairs.c util.o
	cc -o score_pairs score_pairs.c util.o -lm

find_in_sorted_lines: find_in_sorted_lines.c util.o
	cc -o find_in_sorted_lines find_in_sorted_lines.c util.o

select_vectors: select_vectors.c util.o
	cc -o select_vectors select_vectors.c util.o

create_years_vector: create_years_vector.c 
	cc -o create_years_vector create_years_vector.c

venn: venn.c util.o
	cc -o venn venn.c util.o

filter_edges: filter_edges.c util.o
	cc -o filter_edges filter_edges.c util.o

BFS: BFS.c util.o
	cc -o BFS BFS.c util.o

x_to_y: x_to_y.c
	cc -o x_to_y x_to_y.c

XY_data_to_bigrams: XY_data_to_bigrams.c util.o
	cc -o XY_data_to_bigrams XY_data_to_bigrams.c util.o

bigrams_to_XY_data: bigrams_to_XY_data.c util.o
	cc -o bigrams_to_XY_data bigrams_to_XY_data.c util.o

killroy: killroy.c util.o
	cc -o killroy killroy.c util.o -lm

generate_pairs_from_idx: generate_pairs_from_idx.c util.o
	cc -o generate_pairs_from_idx generate_pairs_from_idx.c util.o

filter_records: filter_records.c util.o
	cc -o filter_records filter_records.c util.o

sum_bigrams: sum_bigrams.c util.o
	cc -o sum_bigrams sum_bigrams.c util.o

sum_lbigrams: sum_lbigrams.c util.o
	cc -o sum_lbigrams sum_lbigrams.c util.o

nbest_bigrams: nbest_bigrams.c util.o
	cc -o nbest_bigrams nbest_bigrams.c util.o

authors_to_authors: authors_to_authors.c util.o
	cc -o authors_to_authors authors_to_authors.c util.o

print_bigrams: print_bigrams.c util.o
	cc -o print_bigrams print_bigrams.c util.o

unprint_bigrams: unprint_bigrams.c util.o
	cc -o unprint_bigrams unprint_bigrams.c util.o

sort_bigrams: sort_bigrams.c util.o
	cc -o sort_bigrams sort_bigrams.c util.o

uniq_bigrams: uniq_bigrams.c util.o
	cc -o uniq_bigrams uniq_bigrams.c util.o

uniq_bigrams_by_hashing: uniq_bigrams_by_hashing.c util.o
	cc -o uniq_bigrams_by_hashing uniq_bigrams_by_hashing.c util.o

print_lbigrams: print_lbigrams.c util.o
	cc -o print_lbigrams print_lbigrams.c util.o

unprint_lbigrams: unprint_lbigrams.c util.o
	cc -o unprint_lbigrams unprint_lbigrams.c util.o

sort_lbigrams: sort_lbigrams.c util.o
	cc -o sort_lbigrams sort_lbigrams.c util.o

uniq_lbigrams: uniq_lbigrams.c util.o
	cc -o uniq_lbigrams uniq_lbigrams.c util.o

uniq_lbigrams_by_hashing: uniq_lbigrams_by_hashing.c util.o
	cc -o uniq_lbigrams_by_hashing uniq_lbigrams_by_hashing.c util.o

center_floats: center_floats.c util.o
	cc -o center_floats center_floats.c util.o -lm

invert_landmarks: invert_landmarks.c util.o
	cc -o invert_landmarks invert_landmarks.c util.o

new_invert_landmarks: new_invert_landmarks.c util.o
	cc -o new_invert_landmarks new_invert_landmarks.c util.o
