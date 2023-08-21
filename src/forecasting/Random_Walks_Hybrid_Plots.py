import argparse
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_file_data(file_path):
    r = joblib.load(file_path)
    d = {k:v for k,v in r['acc_by_bin'].items() if k<=100}
    return d
    

def plot_data_and_moving_average(df_prone, df_specter1, df_prone_specter1, try_bin, output_folder):
    plt.figure(figsize=(8, 4), dpi=600)
    
    # Calculate the 5-point moving average for 'y'
    window_size = 5
    df_prone['moving_average'] = df_prone['y'].rolling(window=window_size, center=True, min_periods=1).mean()
    df_specter1['moving_average'] = df_specter1['y'].rolling(window=window_size, center=True, min_periods=1).mean()
    df_prone_specter1['moving_average'] = df_prone_specter1['y'].rolling(window=window_size, center=True, min_periods=1).mean()

    # Plot the original data and the moving average
    plt.plot(df_prone['x'], df_prone['moving_average'], label=f'ProNE Moving Average', linestyle='-', color='blue')
    plt.plot(df_specter1['x'], df_specter1['moving_average'], label=f'Specter1 Moving Average', linestyle='-', color='green')
    plt.plot(df_prone_specter1['x'], df_prone_specter1['moving_average'], label=f'ProNE+Specter1 Moving Average', linestyle='-', color='red')

    plt.axvline(x=try_bin + 0.5, linestyle='--', label=f'Train-Test Cutoff={try_bin}', color='black')
    plt.xlabel('Evaluation Bin')
    plt.ylabel('Accuracy')
    plt.title(f'Forecast Accuracy of Bin {str(try_bin).zfill(3)} ProNE for 1 vs 2-4 Hop Walk Prediction')
    plt.legend()
    plt.grid(True)
    y_min = min(min(l) for l in [df_prone['moving_average'], df_specter1['moving_average'], df_prone_specter1['moving_average']])
    y_max = max(max(l) for l in [df_prone['moving_average'], df_specter1['moving_average'], df_prone_specter1['moving_average']])

    plt.ylim(y_min-0.05, y_max+0.05)
    plt.savefig(os.path.join(output_folder, f'forecast_models_test_train_split_at_{try_bin}.png'))

def main(args):
    # Ensure output_folder exists
    os.makedirs(args.output, exist_ok=True)
    
    try_bins = range(0, 100)
    
    for try_bin in try_bins:
        try:
            file_prone_only_path = f'{args.prone_input}/{try_bin}_when_necessary_prone.pkl'
            file_prone_specter1_path = f'{args.prone_and_specter_input}/{try_bin}_when_necessary_prone.pkl'
            file_specter1_only_path = f'{args.specter_input}/{0}_when_necessary_prone.pkl'

            bin_to_acc_prone = load_file_data(file_prone_only_path)
            bin_to_acc_prone_specter1 = load_file_data(file_prone_specter1_path)
            bin_to_acc_specter1 = load_file_data(file_specter1_only_path)

            data_prone = {'x': list(bin_to_acc_prone.keys()), 'y': list(bin_to_acc_prone.values())}
            df_prone = pd.DataFrame(data_prone)

            data_specter1 = {'x': list(bin_to_acc_specter1.keys()), 'y': list(bin_to_acc_specter1.values())}
            df_specter1 = pd.DataFrame(data_specter1)

            data_prone_specter1 = {'x': list(bin_to_acc_prone_specter1.keys()), 'y': list(bin_to_acc_prone_specter1.values())}
            df_prone_specter1 = pd.DataFrame(data_prone_specter1)

            plot_data_and_moving_average(df_prone, df_specter1, df_prone_specter1, try_bin, args.output)
        except Exception as e:
            print(e)
            print(f'Skipping for bin {try_bin}')
            
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create forecast accuracy plots.")
    parser.add_argument("--output", "-o", type=str, default="walk_forecasting_plots/", 
                        help="output folder to save forecasting plots")
    parser.add_argument("--specter_input", "-s", type=str, required=True, help="Input folder containing data files.")    
    parser.add_argument("--prone_input", "-p", type=str, required=True, help="Input folder containing data files.")
    parser.add_argument("--prone_and_specter_input", "-ps", type=str, required=True, help="Input folder containing data files.")


    args = parser.parse_args()
    main(args)
