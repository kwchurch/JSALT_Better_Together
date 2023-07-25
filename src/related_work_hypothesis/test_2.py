import pandas as pd
import os
import argparse
import numpy as np
from keras.models import load_model
import ast
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="reference File", default='/mnt/c/Rodolfo/Desarrollo/JSALT_2023/JSALT_Better_Together/src/related_work_hypothesis/results/')
    args = parser.parse_args()
    return args


def process_batch(batch_data, df_2, model):
    results = []
    for _, row in batch_data.iterrows():
        matching_row = df_2[df_2["corpus_id"] == row["corpus_id"]].iloc[0]
        df_x = pd.DataFrame([matching_row["V_rw"]])
        df_y = pd.DataFrame([matching_row["V_nrw"]])
        df_z = pd.DataFrame([matching_row["V"]])

        merged_df = pd.concat([df_x, df_y], axis=1)
        single_example = merged_df.iloc[0].values
        salida = df_z.iloc[0].values
        df_single_example = pd.DataFrame([single_example])
        predicted_output = model.predict(df_single_example)
        predic = predicted_output[0]
        similarity = cosine_similarity(salida.reshape(1, -1), predic.reshape(1, -1))

        data = {
            "corpus_id": row['corpus_id'],
            "cos(v,rw)": row['cos_rw'],
            "cos(v,all)": row['cos_all'],
            "cos(V,p_all)": similarity[0]
        }
        results.append(data)

    return pd.DataFrame(results)


def main():
    args = parse_args()
    FILEPATH = os.path.dirname(args.input)
    raw_dirs = set([d for d in os.listdir(FILEPATH)])
    # Lista para almacenar los DataFrames de cada archivo
    dataframes = []
    for archivo in raw_dirs:
        df = pd.read_csv(FILEPATH+"/"+archivo, sep='\t')
        dataframes.append(df)

    df = pd.concat(dataframes)
    df.reset_index(drop=True, inplace=True)

    df_filtered2 = df[df['cos_rw'] > 0]
    df_filtered2 = df_filtered2[df_filtered2['cos_all'] > 0]


    model = load_model('all_modelo.h5')
    results = []
    
    FILEPATH_2 = os.path.dirname("/mnt/c/Rodolfo/Desarrollo/JSALT_2023/JSALT_Better_Together/src/related_work_hypothesis/predicting_vectors/")
    raw_dirs = set([d for d in os.listdir(FILEPATH_2)])

    z = []
    

    for archivo in raw_dirs:
        with open(FILEPATH_2+"/"+archivo, "r") as file:
            for line in file:
                if line.find("V") == -1:
                    line = line.replace("\n","")
                    line = line.replace("'","")
                    data = {"corpus_id":line.split("\t")[0], "V": ast.literal_eval(line.split("\t")[1]), "V_rw":ast.literal_eval(line.split("\t")[2]),"V_nrw":ast.literal_eval(line.split("\t")[3])}
                    z.append(data)

    df_2 = pd.DataFrame(z)


    print("Total of paper: ", len(df_filtered2))


    '''
    batch_size = 100
    num_batches = int(np.ceil(len(df_filtered2) / batch_size))

    # Define the number of batches after which to save the results
    save_results_after_batches = 5
    results = []

    for batch_idx in tqdm(range(num_batches), desc="Processing batches", unit="batch"):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, len(df_filtered2))
        batch_data = df_filtered2.iloc[start_idx:end_idx]

        batch_results = process_batch(batch_data, df_2, model)
        results.append(batch_results)

        if (batch_idx + 1) % save_results_after_batches == 0:
            # Concatenate all batch results and save to file
            df_x = pd.concat(results, ignore_index=True)
            df_x.to_csv(f"results_predict_batch_{batch_idx+1}.tsv", sep="\t", index=False)

            # Clear the results list to save memory
            results = []

    # Save the remaining results after processing all batches
    if results:
        df_x = pd.concat(results, ignore_index=True)
        df_x.to_csv(f"results_predict_batch_{num_batches}.tsv", sep="\t", index=False)
    '''


if __name__ == "__main__":
    main()
