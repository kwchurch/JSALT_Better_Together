# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt



def graph(df_filtered,title,col1,col2):
    # Count how many times 'rw' is greater than 'all' and vice versa
    rw_greater_than_all_count = (df_filtered[col1] < df_filtered[col2]).sum()
    all_greater_than_rw_count = (df_filtered[col2] < df_filtered[col1]).sum()

    # Create a list with values and labels for the charts
    values = [rw_greater_than_all_count, all_greater_than_rw_count]
    labels = ['All References',  'Related Work References']

    # Create the pie chart
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.show()


def main():

    FILEPATH = os.path.dirname("/mnt/c/Rodolfo/Desarrollo/JSALT_2023/JSALT_Better_Together/src/related_work_hypothesis/results/")
    raw_dirs = set([d for d in os.listdir(FILEPATH)])


    # Lista para almacenar los DataFrames de cada archivo
    dataframes = []

    # Leer cada archivo TSV y almacenar el DataFrame en la lista 'dataframes'
    for archivo in raw_dirs:
        df = pd.read_csv(FILEPATH+"/"+archivo, sep='\t')
        dataframes.append(df)

    df = pd.concat(dataframes)

    # Opcional: Resetear el índice del DataFrame resultante
    df.reset_index(drop=True, inplace=True)

    print("Total of paper processed: ",len(df))

    df_filtered = df[df['det_rw'] > 0]
    df_filtered = df_filtered[df_filtered['det_all'] > 0]

    df_filtered2 = df[df['cos_rw'] > 0]
    df_filtered2 = df_filtered2[df_filtered2['cos_all'] > 0]

    #graph(df_filtered,'Percentage of comparisons |F(d) - F\'(d)| (excluding rw=0 and all=0)','det_rw','det_all')
    graph(df_filtered2,'Is it better to use related work references than all references?','cos_rw','cos_all')


if __name__ == "__main__":
    main()