#!/bin/sh

gram_matrix $1 | uniq_bigrams_by_hashing > gram.$$
sort_bigrams gram.$$ | uniq_bigrams 
