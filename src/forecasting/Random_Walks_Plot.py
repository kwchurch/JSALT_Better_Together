#!/usr/bin/env python
# coding: utf-8


import joblib
import numpy as np
import os
from tqdm import tqdm
import argparse
import pandas as pd
from copy import deepcopy
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import seaborn as sns


def results_to_plot(results_folder, output_folder):
    R_acc = [] 
    R_youdens_j = []
    y_axis_labels = []
    bin_to_overall_accs = {}
    bin_to_overall_youdens_j = {}

    print(os.listdir(results_folder))
    for file_name in tqdm(sorted(os.listdir(results_folder), key=lambda x:int(x.split('_')[0]))):
        
        results_file_path = os.path.join(results_folder, file_name)
        cumbin = int(file_name.split('_')[0])
        if cumbin in {30, 31}:
            continue

        try:
            r = joblib.load(results_file_path)

            acc_values = [r['acc_by_bin'][i] for i in range(0,100)]
            R_acc.append(acc_values)

            j_values = [max(r['youdens_j_by_bin'][i],0) for i in range(0,100)]
            R_youdens_j.append(j_values)

            y_axis_labels.append(cumbin)


            bin_to_overall_accs[cumbin] = r['acc']
            bin_to_overall_youdens_j[cumbin] = r['youdens_j']
        

        except:
            print(f'failed with {file}')
    
    
    df = pd.DataFrame(R_acc)
    
    df.to_csv(os.path.join(output_folder, f'acc_preds_prone_when_necessary.tsv'), sep='\t')
    
    plot_forecast_from_cumbins(bin_to_overall_metric=R_acc, y_axis_labels=y_axis_labels, 
                               metric='Accuracy',
                               first_plot_filename=os.path.join(output_folder, f'ProNE_when_necessary_acc_forecast.jpg'),
                               second_plot_filename=os.path.join(output_folder, f'ProNE_when_necessary_cumbin_effects.jpg'),
                               min_forecast_steps=5)
    
    plot_forecast_heatmap(R=R_acc, metric='Accuracy', y_axis_labels=y_axis_labels,
                          output_filename=os.path.join(output_folder, f'ProNE_when_necessary_acc_heatmap.jpg'))
    plot_forecast_heatmap(R=R_youdens_j, metric='Youden\'s_J', y_axis_labels=y_axis_labels,
                          output_filename=os.path.join(output_folder, f'ProNE_when_necessary_youdensj_heatmap.jpg'))
    plot_forecast_linegraph(bin_to_overall_metric=bin_to_overall_accs, metric='Accuracy', output_filename=os.path.join(output_folder, f'ProNE_when_necessary_acc_lineplot.jpg'))
    plot_forecast_linegraph(bin_to_overall_metric=bin_to_overall_youdens_j, metric='Youden\'s J', output_filename=os.path.join(output_folder, f'ProNE_when_necessary_youdensj_lineplot.jpg'))
    
    


def plot_forecast_heatmap(R, metric, y_axis_labels, output_filename):
    plt.figure(figsize=(8,8), dpi=300)
    sns.set(font_scale = 1.4)
    
    min_metric_val = np.min(R)
    
    R_diag = []
    for row_idx, r_row in enumerate(R):
        new_row = deepcopy(r_row)
        new_row[y_axis_labels[row_idx]] = min_metric_val
        R_diag.append(new_row)
        
    percentile_80 = np.percentile(R_diag, 98)

    # Create the heatmap with adjusted color scaling
    #ax = sns.heatmap(R_diag, annot=False, cmap='viridis', vmin=0, vmax=vmax_value)

    ax = sns.heatmap(R_diag, annot=False, cmap='viridis', vmax=percentile_80, robust=True)

    y_ticks = plt.yticks()[0]
    
    yticklabels = [y_axis_labels[int(round(i))] for i in y_ticks]
    ax.set_yticklabels(yticklabels, rotation = 0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    ax.set_title(f"{metric} of ProNE Bins for 1 vs 2-4 Hop Walk Prediction", fontsize=14, pad=20)
    ax.set_xlabel(f"Evaluation Bin", fontsize=14, labelpad=20)
    ax.set_ylabel("Max Train Bin", fontsize=14, labelpad=20)
    plt.savefig(output_filename)
    

def plot_forecast_linegraph(bin_to_overall_metric, metric, output_filename):

    plt.figure(figsize=(30, 8), dpi=300)

    x_values = list(bin_to_overall_metric.keys())
    y_values = list(bin_to_overall_metric.values())

    plt.plot(x_values, y_values, marker='o', linestyle='-')

    plt.ylabel(f'{metric}')
    plt.xlabel('Max Train Bin')
    plt.title(f'{metric} of ProNE Cumulative Bin Models for 1 vs 2-4 Hop Walk Prediction', fontsize=14, pad=20)

    # Set all x-values as ticks
    plt.xticks(x_values, rotation=90)
    # Add a grid for every x-tick
    plt.grid(axis='x', linestyle='--')

    plt.savefig(output_filename)

import matplotlib.pyplot as plt
from collections import defaultdict

def plot_forecast_from_cumbins(bin_to_overall_metric, y_axis_labels, metric, min_forecast_steps=5, first_plot_filename=None, second_plot_filename=None):
    bins_out = defaultdict(list)
    cumbins = []
    trainlen_out_accs = defaultdict(list)

    # Iterate through y_axis_labels and bin_to_overall_metric
    for cumbin, row in zip(y_axis_labels, bin_to_overall_metric):
        if cumbin + min_forecast_steps > 100:
            continue
        cumbins.append(cumbin)
        # Calculate forecasts and training lengths
        for forecast in range(cumbin + 1, 100):
            bins_out[forecast - cumbin].append(row[forecast])
            trainlen_out_accs[cumbin] = [row[idx] for idx in range(len(row)) if cumbin < idx < 99]

    data_for_boxplot = [bins_out[key] for key in bins_out]

    # Create the first box plot
    plt.figure(figsize=(8, 4), dpi=600)
    plt.boxplot(data_for_boxplot, labels=bins_out.keys())

    # Add labels and title for the first plot
    plt.ylabel(f'Forecast {metric}')
    plt.xlabel('Num Bins Forecasting Forward')
    plt.title(f'Performance Forecasting Range Averaged Across all Cumbins vs {metric}')
    plt.xticks(range(1, len(bins_out.keys()) + 1, 3), list(bins_out.keys())[::3], rotation=90)
    plt.savefig(first_plot_filename)

    # Create the second box plot
    data_for_boxplot = [trainlen_out_accs[key] for key in trainlen_out_accs]
    plt.clf()
    plt.figure(figsize=(8, 4), dpi=600)
    plt.boxplot(data_for_boxplot, labels=trainlen_out_accs.keys())

    # Add labels and title for the second plot
    plt.ylabel(f'Forecast {metric}')
    plt.xlabel('Num Training Bins')
    plt.title(f'Num Training Bins vs Forecast {metric}')
    plt.xticks(range(1, len(trainlen_out_accs.keys()) + 1, 3), list(trainlen_out_accs.keys())[::3], rotation=90)
    plt.savefig(second_plot_filename)

# Example usage:
# plot_forecast_from_cumbins(bin_to_overall_metric, y_axis_labels, 'Accuracy', 'forecast_plot.png', min_forecast_steps=5, second_plot_filename='training_plot.png')

def main():
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description="Walk Forecasting Plots")
    
    # Add arguments
    parser.add_argument("--input", "-i", type=str, default="walk_forecasting/", 
                        help="Input folder to load the walk forecasting results from")
    parser.add_argument("--output", "-o", type=str, default="walk_forecasting_plots/", 
                        help="output folder to save forecasting plots")
    
    args = parser.parse_args()

    output_folder = args.output
    # Ensure output_folder exists
    os.makedirs(output_folder, exist_ok=True)

    results_to_plot(args.input, args.output)

if __name__ == "__main__":
    main()