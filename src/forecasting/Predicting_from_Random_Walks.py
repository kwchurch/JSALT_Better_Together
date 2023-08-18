#!/usr/bin/env python
# coding: utf-8


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
    prior_class_1 = sum(y)/len(y)
    clf = LogisticRegression()
    clf.fit(x, y)
    implied_threshold = -clf.intercept_/clf.coef_
    
    return implied_threshold.item(), prior_class_1

def youdens_j_score(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return sensitivity + specificity - 1

FORECAST_BINS = 2 
def test_acc_from_threshold(full_test_df, threshold, prior_class_1_prob, test_train_split_bin, specterv1_test_df, 
                            specterv1_threshold, fallback_method):
    # ProNE: apply threshold as class prediciton (1 vs 2-4 hops)
    full_test_df['pred'] = (full_test_df['cos_sim'] >= threshold)
    full_test_df['pred'] = full_test_df['pred'].astype(int)
    
    # Specter: apply threshold as class prediciton (1 vs 2-4 hops)
    specterv1_test_df['pred'] = (specterv1_test_df['cos_sim'] >= specterv1_threshold)
    specterv1_test_df['pred'] = specterv1_test_df['pred'].astype(int)
    
    
    # Fallback for missing values
    full_test_df['no_data'] = full_test_df['cos_sim'] == -1
    
    if fallback_method == 'specter1':
        # Replace values in 'pred' column with 'specterv1' where 'no_data' is True, otherwise keep the existing 'pred' values
        full_test_df['pred'] = np.where(full_test_df['no_data'], specterv1_test_df['pred'], full_test_df['pred'])

    elif fallback_method == 'guess':
        # Replace values in 'pred' column with 'prior_guess' where 'no_data' is stil True, otherwise keep the existing 'pred' values  
        full_test_df['prior_guess'] = np.random.binomial(1, prior_class_1_prob, size=len(full_test_df))
        full_test_df['pred'] = np.where(full_test_df['no_data'], full_test_df['prior_guess'], full_test_df['pred'])

    else:
        print(f'fallback method {fallback_method} is invalid, exiting...')
        raise NotImplementedError
    

    # Group the DataFrame by the maximum value between 'bin0' and 'bin1'
    # Then count occurrences of cos_sim == -1 and calculate the proportion
    grouped_full_test_df = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))
    rate_cos_sim_minus_1 = grouped_full_test_df['cos_sim'].apply(lambda x: (x == -1).mean()).to_dict()
    
    full_test_df['is_one_hop'] = full_test_df['hops'] == 1
    full_test_df['is_one_hop'] = full_test_df['is_one_hop'].astype(int)
    
    specterv1_test_df['is_one_hop'] = specterv1_test_df['hops'] == 1
    specterv1_test_df['is_one_hop'] = specterv1_test_df['is_one_hop'].astype(int)
    
    full_test_df['correct'] = full_test_df['is_one_hop'] == full_test_df['pred'] 
    full_test_df['correct'] = full_test_df['correct'].astype(int)
    
    specterv1_test_df['correct'] = specterv1_test_df['is_one_hop'] == specterv1_test_df['pred'] 
    specterv1_test_df['correct'] = specterv1_test_df['correct'].astype(int)
    
    y_true = full_test_df['is_one_hop']
    y_pred = full_test_df['pred'] 
    
    youdens_j = youdens_j_score(y_true, y_pred)
    
    youdens_j_by_bin = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))\
                          .apply(lambda group: youdens_j_score(group['is_one_hop'], group['pred'])).to_dict()
        
    # calculate accuracy
    acc_specter = sum(specterv1_test_df['correct'])/len(specterv1_test_df)
    acc = sum(full_test_df['correct'])/len(full_test_df)
        
    acc_by_bin = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))['correct'].mean().to_dict()
    size_by_bin = full_test_df.groupby(full_test_df[['bin0', 'bin1']].max(axis=1))['correct'].size().to_dict()
    
    # Calculate the maximum of bin0 and bin1
    max_bin0_bin1 = full_test_df[['bin0', 'bin1']].max(axis=1)

    # Filter the full_test_df based on the condition
    filtered_df = full_test_df[(max_bin0_bin1 > test_train_split_bin) & (max_bin0_bin1 <= 100)]
    
    acc_forecast = sum(filtered_df['correct'])/len(filtered_df)
    youdens_j_forecast = youdens_j_score(filtered_df['is_one_hop'].tolist(), filtered_df['pred'].tolist())
    
    return acc_forecast, acc_by_bin, youdens_j_forecast, youdens_j_by_bin,  rate_cos_sim_minus_1


def is_tuple_in_keep_ids(row, keep_ids):
    return (row['id0'], row['id1']) in keep_ids

    
def process_data(walk_path, output_folder, walk_with_bins_df, specterv1_test_df, specterv1_threshold, keep_ids_df, fallback_method):
    cumbin = int(walk_path.split('/')[-3])
    if os.path.isfile(f'{output_folder}/{cumbin}_when_necessary_prone.pkl'):
        print(f'{output_folder}/{cumbin}_when_necessary_prone.pkl exists, skipping...')
        return True
    test_dfs = sorted([os.path.join(walk_path, f) for f in os.listdir(walk_path) if f[-3] == '.' and f[-2:]!='aa'])
    test_df_list = [pd.read_csv(file, sep='\t', header=None) for file in test_dfs]
    test_df = pd.concat(test_df_list)
    test_df = df_merge(test_df, walk_with_bins_df)

    test_df = test_df.drop_duplicates(subset=['id0', 'id1'], keep='first')

    # Perform an inner merge between 'test_df' and 'keep_ids_df'
    test_df = test_df.merge(keep_ids_df, on=['id0', 'id1'], how='inner')
    

    train_df = pd.read_csv(os.path.join(walk_path, 'walk12.aa'), sep='\t', header=None) 
    train_df = df_merge(train_df, walk_with_bins_df)
    threshold, prior_class_1_prob = clf_threshold_finder(train_df)
    acc, acc_by_bin, youdens_j, youdens_j_by_bin, rate_cos_sim_minus_1 = test_acc_from_threshold(test_df, threshold, 
                                                                                                 prior_class_1_prob, cumbin,
                                                                                                 specterv1_test_df, 
                                                                                                 specterv1_threshold,
                                                                                                 fallback_method)
    results = {'acc':acc, 'acc_by_bin':acc_by_bin, 'youdens_j':youdens_j, 
               'youdens_j_by_bin':youdens_j_by_bin,  'rate_cos_sim_minus_1':rate_cos_sim_minus_1}
    joblib.dump(results, f'{output_folder}/{cumbin}_when_necessary_prone.pkl')

# Function to create a tuple from [id0, id1]
def create_tuple(row):
    return tuple(row)


# Function to remove rows until the 'is_one_hop' ratio is 0.3
def filter_by_ratio(group):
    target_ratio = 0.3
    current_ratio = group['is_one_hop'].mean()
    drop_amount = max(len(group) // 1000, 1)  # Adjust the drop amount as needed
    if current_ratio > target_ratio:
        # If the initial ratio is greater than the target, start by dropping is_one_hop=True rows
        while current_ratio > target_ratio:
            rows_to_remove = group[group['is_one_hop'] == True].tail(drop_amount)
            if not rows_to_remove.empty:
                group = group.drop(rows_to_remove.index)
                current_ratio = group['is_one_hop'].mean()
            else:
                # If no more rows can be removed, exit the loop
                break
    else:
        # If the initial ratio is smaller than the target, start by dropping is_one_hop=False rows
        while current_ratio < target_ratio:
            rows_to_remove = group[group['is_one_hop'] == False].tail(drop_amount)
            if not rows_to_remove.empty:
                group = group.drop(rows_to_remove.index)
                current_ratio = group['is_one_hop'].mean()
            else:
                # If no more rows can be removed, exit the loop
                break
    
    return group
    
def get_test_ids(test_df):
    test_df = test_df.drop_duplicates(subset=['id0', 'id1'], keep='first')
    test_df['is_one_hop'] = test_df['hops'] == 1
    grouped_test_df = test_df.groupby(test_df[['bin0', 'bin1']].max(axis=1))
    balanced_test_df = pd.concat([filter_by_ratio(group) for _, group in tqdm(grouped_test_df)])

    # Apply the function to create a new column containing tuples
    balanced_test_df['id_tuple'] = balanced_test_df[['id0', 'id1']].apply(create_tuple, axis=1)

    # Convert the 'id_tuple' column to a set
    id_tuple_set = set(balanced_test_df['id_tuple'])

    # Display the resulting set of tuples
    return id_tuple_set
    
def main():
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description="Walk Forecasting Script")
    
    # Add arguments
    parser.add_argument("--output", "-o", type=str, default="walk_forecasting/", 
                        help="Output folder to store the walk forecasting results")
    parser.add_argument("--method", "-m", type=str, default="guess", 
                        help="Fallback method when Prone has no values for one or more papers. Options: guess, specter1")
    parser.add_argument("--threads", "-t", type=int, default=1, 
                        help="Simultaneous threads to use")
    
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

    
    ## set up specterv1 model
    specterv1_walk_path = os.path.join(os.environ.get('JSALTdir'), 'semantic_scholar/p.vickers/specter/walk_pieces/when_necessary')
    specterv1_test_dfs = sorted([os.path.join(specterv1_walk_path, f) for f in os.listdir(specterv1_walk_path) if f[-3] == '.' and f[-2:]!='aa'])
    specterv1_test_df_list = [pd.read_csv(file, sep='\t', header=None) for file in specterv1_test_dfs]
    specterv1_test_df = pd.concat(specterv1_test_df_list)
    specterv1_test_df = df_merge(specterv1_test_df, walk_with_bins_df)
    specterv1_test_df = specterv1_test_df.drop_duplicates(subset=['id0', 'id1'], keep='first')

    specterv1_train_df = pd.read_csv(os.path.join(specterv1_walk_path, 'walk12.aa'), sep='\t', header=None) 
    specterv1_train_df = df_merge(specterv1_train_df, walk_with_bins_df)
    specterv1_threshold, _ = clf_threshold_finder(specterv1_train_df)

    id_tuple_set = get_test_ids(specterv1_test_df)
    
    keep_ids_df = pd.DataFrame(list(id_tuple_set), columns=['id0', 'id1'])

    # Perform an inner merge between 'test_df' and 'keep_ids_df'
    specterv1_test_df = specterv1_test_df.merge(keep_ids_df, on=['id0', 'id1'], how='inner')

    num_threads = args.threads

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_data, walk_path, 
                                   output_folder, walk_with_bins_df, 
                                   specterv1_test_df, specterv1_threshold, 
                                   keep_ids_df, args.method) for walk_path in cumbins_walks]

        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(cumbins_walks)):
            pass

if __name__ == "__main__":
    main()