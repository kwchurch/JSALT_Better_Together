#!/usr/bin/env python
# coding: utf-8


import joblib
import numpy as np
import os
from tqdm import tqdm
import argparse

import matplotlib.pyplot as plt
import seaborn as sns


def results_to_plot(results_folder, output_folder):
    R_acc = [] 
    R_youdens_j = []
    y_axis_labels = []
    bin_to_overall_accs = {}
    bin_to_overall_youdens_j = {}

    for file_name in tqdm(sorted(os.listdir(results_folder), key=lambda x:int(x.split('_')[0]))):
        results_file_path = os.path.join(results_folder, file_name)
        cumbin = int(file_name.split('_')[0])

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
            
    plot_forecast_heatmap(R=R_acc, metric='Accuracy', y_axis_labels=y_axis_labels,
                          output_filename=os.path.join(output_folder, f'ProNE_when_necessary_acc_heatmap.jpg'))
    plot_forecast_heatmap(R=R_youdens_j, metric='Youden\'s_J', y_axis_labels=y_axis_labels,
                          output_filename=os.path.join(output_folder, f'ProNE_when_necessary_youdensj_heatmap.jpg'))
    plot_forecast_linegraph(bin_to_overall_metric=bin_to_overall_accs, metric='Accuracy', output_filename=os.path.join(output_folder, f'ProNE_when_necessary_acc_lineplot.jpg'))
    plot_forecast_linegraph(bin_to_overall_metric=bin_to_overall_youdens_j, metric='Youden\'s J', output_filename=os.path.join(output_folder, f'ProNE_when_necessary_youdensj_lineplot.jpg'))


def plot_forecast_heatmap(R, metric, y_axis_labels, output_filename):
    plt.figure(figsize=(12,12), dpi=600)
    sns.set(font_scale = 1.1)


    ax = sns.heatmap(R, annot=False)
    ax.set_yticklabels(y_axis_labels, rotation = 0)
    ax.set_xticklabels(np.arange(0,100,3), rotation = -90)

    ax.set_title(f"{metric} of ProNE Cumulative Bin Models for 1 vs 2-4 Hop Walk Prediction per Prediciton Bin ", fontsize=14, pad=20)
    ax.set_xlabel(f"Bin {metric}", fontsize=14, labelpad=20)
    ax.set_ylabel("Max Train Bin", fontsize=14, labelpad=20)
    plt.savefig(output_filename)
    

def plot_forecast_linegraph(bin_to_overall_metric, metric, output_filename):

    plt.figure(figsize=(8,8), dpi=600)

    x_values = list(bin_to_overall_metric.keys())
    y_values = list(bin_to_overall_metric.values())

    plt.plot(x_values, y_values, marker='o', linestyle='-')

    plt.xlabel(f'{metric}')
    plt.ylabel('Max Train Bin')
    plt.title(f'{metric} of ProNE Cumulative Bin Models for 1 vs 2-4 Hop Walk Prediction', fontsize=14, pad=20)

    plt.savefig(output_filename)


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