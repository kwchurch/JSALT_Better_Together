#!/usr/bin/env python
# coding: utf-8

# For each method get Results Matrix R
## For each model trained_upto_bin_k (M_0)
### Find the optimal descision threshold with LogisticRegression on walk.aa to maximise accuracy for predicting 1 vs 2-4 hops
### For each bin collect all the walks where the larger value is in that bin (M_1)
#### Calcuate the accuracy ACC and Jouden's J of predicting 1 vs 2-4 hops for that bin 

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import joblib
import concurrent.futures
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, confusion_matrix

import argparse


def df_merge(cos_df, walk_df):

    all_df = cos_df.merge(walk_df, on=[1, 2], how='left')

    all_df.rename(columns={
        '0_x': 'cos_sim',
        1: 'id0',
        2: 'id1',
        '0_y': 'hops',
        3: 'bin0',
        4: 'bin1'
    }, inplace=True)
    all_df['bin0'] = all_df['bin0'].fillna(1337).astype(int)
    all_df['bin1'] = all_df['bin1'].fillna(1337).astype(int)
    return(all_df)


def clf_threshold_finder(train_df):
    train_df_valid_cos_sim = train_df[train_df['cos_sim'] != -1]
    x, y = np.array(train_df_valid_cos_sim['cos_sim']).reshape(-1, 1), \
           np.array([1 if y_i == 1 else 0 for y_i in train_df_valid_cos_sim['hops']])

    clf = LogisticRegression()
    clf.fit(x, y)
    implied_threshold = -clf.intercept_/clf.coef_
    
    return implied_threshold.item()



def youdens_j_score(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return sensitivity + specificity - 1


def test_acc_from_threshold(full_test_df, threshold):
    # apply threshold as class prediciton (1 vs 2-4 hops)
    full_test_df['pred'] = (full_test_df['cos_sim'] >= threshold)
    full_test_df['pred'] = full_test_df['pred'].astype(int)
    
    full_test_df['no_pred'] = full_test_df['cos_sim'] == -1

    
    count_cos_sim_minus_1 = full_test_df[full_test_df['cos_sim'] == -1].groupby(full_test_df[['bin0', 'bin1']].max(axis=1)).size().to_dict()

    # Group the DataFrame by the maximum value between 'bin0' and 'bin1'
    # Then count occurrences of cos_sim == -1 and calculate the proportion
    grouped_full_test_df = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))
    rate_cos_sim_minus_1 = grouped_full_test_df['cos_sim'].apply(lambda x: (x == -1).mean()).to_dict()
    
    full_test_df['is_one_hop'] = full_test_df['hops'] == 1
    full_test_df['is_one_hop'] = full_test_df['is_one_hop'].astype(int)
    
    full_test_df['correct'] = full_test_df['is_one_hop'] == full_test_df['pred'] 
    full_test_df['correct'] = full_test_df['correct'].astype(int)
    
    y_true = full_test_df['is_one_hop']
    y_pred = full_test_df['pred'] 
    
    youdens_j = youdens_j_score(y_true, y_pred)
    
    youdens_j_by_bin = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))\
                          .apply(lambda group: youdens_j_score(group['is_one_hop'], group['pred'])).to_dict()
    
    full_test_df['correct'] = full_test_df.apply(lambda row: 0 if row['no_pred'] else row['correct'], axis=1)
    
    
    # check if class prediciton is right
    #valid_test_df = full_test_df[full_test_df['cos_sim'] != -1].copy()
    #valid_test_df['is_one_hop'] = valid_test_df['hops'] == 1
    #valid_test_df['is_one_hop'] = valid_test_df['is_one_hop'].astype(int)
    #valid_test_df['correct'] = valid_test_df['is_one_hop'] == valid_test_df['pred']
    #valid_test_df['correct'] = valid_test_df['correct'].astype(int)
    # calculate accuracy
    acc = sum(full_test_df['correct'])/len(full_test_df)
    acc_by_bin = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))['correct'].mean().to_dict()

    return acc, acc_by_bin,youdens_j, youdens_j_by_bin,  rate_cos_sim_minus_1

    
# Your function that performs the task for each iteration of the loop
def process_data(walk_path, output_folder, walk_with_bins_df):
    cumbin = int(walk_path.split('/')[-3])
    test_dfs = sorted([os.path.join(walk_path, f) for f in os.listdir(walk_path) if f[-3] == '.' and f[-2:]!='aa'])
    test_df_list = [pd.read_csv(file, sep='\t', header=None) for file in test_dfs]
    test_df = pd.concat(test_df_list)
    

    train_df = pd.read_csv(os.path.join(walk_path, 'walk12.aa'), sep='\t', header=None) 
    train_df = df_merge(train_df, walk_with_bins_df)
    test_df = df_merge(test_df, walk_with_bins_df)
    threshold = clf_threshold_finder(train_df)
    acc, acc_by_bin, youdens_j, youdens_j_by_bin, rate_cos_sim_minus_1 = test_acc_from_threshold(test_df, threshold)
    results = {'acc':acc, 'acc_by_bin':acc_by_bin, 'youdens_j':youdens_j, 
               'youdens_j_by_bin':youdens_j_by_bin,  'rate_cos_sim_minus_1':rate_cos_sim_minus_1}
    joblib.dump(results, f'{output_folder}/{cumbin}_when_necessary_prone.pkl')

   
def main():
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description="Walk Forecasting Script")
    
    # Add arguments
    parser.add_argument("--output", "-o", type=str, default="walk_forecasting/", 
                        help="Output folder to store the walk forecasting results")
    parser.add_argument("--threads", "-t", type=int, default=4, 
                        help="simultaneous threads to use")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Get the walk_path and output_folder from the parsed arguments
    output_folder = args.output
    
    # Ensure output_folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    walk_with_bins_path = os.path.join(os.environ.get('JSALTdir'), 'semantic_scholar/eval/walk_with_bins')
    walk_with_bins_df = pd.read_csv(walk_with_bins_path, sep='\t', header=None)
    
    walk_path = os.environ.get('walkdir')
    cumbins_walks = sorted([os.path.join(walk_path, f, 'walk_pieces/when_necessary') for \
                            f in os.listdir(walk_path) if f[-3:]!='zip'])
    num_threads = args.threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_data, data, output_folder, walk_with_bins_df) for data in cumbins_walks]

        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(cumbins_walks)):
            pass

if __name__ == "__main__":
    main()