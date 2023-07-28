
# Related Work Hypothesis 

## Introduction

This repository contains Python scripts to explore the Related Work Hypothesis using text embeddings. The hypothesis is evaluated using two different models: Specter2 and Prone. The scripts read text data from two files, namely References File and Compare File, and perform vector clustering and comparison tasks. Additionally, the scripts provide visualizations to aid in understanding the comparison results.

# Índice

1. [Test Related Work References Hypothesis only 1 paper - Low-resource paper by Rodolfo](#test-related-work-references-hypothesis-only-1-paper---low-resource-paper-by-rodolfo)
2. [Test Related Work References Hypothesis using Martins File - over 400k papers](#test-related-work-references-hypothesis-using-martins-file---over-400k-papers)
3. [Evaluating Related Work References Hypothesis using Martins File](#evaluating-related-work-references-hypothesis-using-martins-file)
4. [Paper Prediction Model](#paper-prediction-model)
5. [Get Vectors from Prone Model using Title or ID](#get-vectors-from-prone-model-using-title-or-id)



## Test Related Work References Hypothesis only 1 paper - Low-resource paper by Rodolfo

This script allows you to perform vector clustering and comparison using different models for text embeddings. It supports two models: Specter2 and Prone. The script reads text data from two files, namely References File and Compare File, and performs the following tasks:

1. Vector Clustering:

The script clusters the vectors from the References File into different groups using K-means clustering.
The number of clusters can be specified as an argument to the script.


2. Vector Comparison:

For each model and reference type, the script calculates the centroid vector of the clustered vectors.
The script then compares the centroid vector with vectors from the Compare File using cosine similarity.
The results are sorted based on cosine similarity scores and saved in separate dataframes for each model and reference type.

3. Visualization:

The script creates a 2D scatter plot for each model and reference type to visualize the cosine similarity scores for comparison.
Additionally, the script uses t-SNE to reduce the dimensionality of the vectors to 3D and creates an interactive 3D plot for visualization.



### Example usage:

```sh
python rw_recommendation_case_1.py -r "path/to/all_references"  -w "path/to/related_work_references" -c "path/to/paper_to_compare"
```
 
### Description 
 
To run the script from the command line, use the following arguments: 

- -r or --ref: Path to the References File. The default path is ../related_work_hypothesis/references_files/all_ref.txt.
- -c or --compare: Path to the Compare File. The default path is ../related_work_hypothesis/references_files/db_test.txt.

Note: The script supports two additional arguments, -w and -c, to specify the path to the Related Work References File. The default path for the Related Work References File is ../related_work_hypothesis/references_files/related_work_ref.txt.


### Output 

The script generates the following output:

1. Cluster Visualization:

A scatter plot with the clustered vectors colored based on the cluster labels.
The plot is saved as cluster_cites.png.

2. Cosine Similarity Comparison:

A line plot showing the cosine similarity scores for each model and reference type.
The plot is saved as <model>_comparacion_cosine.png, where <model> is the name of the model (Specter2 or Prone).

3. 3D Visualization:

An interactive 3D plot showing the reduced-dimensional vectors for each model and reference type.
The plot is saved as grafico_3d.png.


## Test Related Work References Hypothesis using Martins File - over 400k papers


### Example usage:

```sh
python rw_recommendation_case_2.py -i <path_to_references_file> -m <path_to_model_directory>
```

### Description

- -i or --input (Positional Argument):

Description: This argument represents the path to the input JSONL file containing references to be processed.
Default Value: ../related_work_hypothesis/references_files/rw_citations.jsonl
Purpose: The code reads the data from this file, which should contain information about research papers, their related work citations, and other citations.

- -m or --model (Positional Argument):

Description: This argument represents the path to the directory containing the pre-trained models.
Default Value: /mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model
Purpose: The code uses this directory to locate the pre-trained models required for calculating vector representations of research papers.
The script will process the citations for each paper, calculate similarity metrics, and generate the output.


### Output

The script will generate a TSV file named rw_hypo.tsv, which contains the calculated similarity metrics for each paper in the input file. The columns in the TSV file are as follows:

- corpus_id: The ID of the research paper.
- cos_rw: Cosine similarity between the research paper and its related works.
- cos_all: Average cosine similarity between the research paper and all citations.
- det_rw: Euclidean distance between the research paper and its related works.
- det_all: Euclidean distance between the research paper and all citations.

### Note

- The script processes the citations in batches to handle large input files efficiently.
- You can specify the input file path and the model directory path using command-line arguments.
- The prone_model directory should be obtained separately, as it contains the pre-trained models necessary for calculating vector representations.


## Evaluating Related Work References Hypothesis using Martins File

This repository contains Python code that analyzes the results of the Related Work Hypothesis experiment. The code reads data from TSV files, filters and processes it, and generates pie charts to visualize the findings.



### Example usage:

```sh
python evaluating_rw_case_2.py -f <path_to_rw_hypo.tsv>
```

### Description

The script supports the following command-line arguments:

- -f, --files: The path to the directory containing the TSV files. If not provided, the default path is used: /mnt/c/Rodolfo/Desarrollo/JSALT_2023/JSALT_Better_Together/src/related_work_hypothesis/results/.


### Output

The script generates a pie chart titled "Is it better to use related work references than all references?" The chart displays the percentage of cases where 'cos_rw' is greater than 'cos_all', excluding rows where 'cos_rw' and 'cos_all' are 0.

### Note

The provided code assumes that the input TSV files follow a specific format with columns like 'det_rw', 'det_all', 'cos_rw', and 'cos_all'. Please ensure that your TSV files have the required columns for the code to work correctly.

Modify the graph() function and uncomment the line #graph(df_filtered,'Percentage of comparisons |F(d) - F\'(d)| (excluding rw=0 and all=0)','det_rw','det_all') to visualize the percentage of comparisons for the 'det_rw' and 'det_all' columns.


## Paper Prediction Model

This code is a Python script used for predicting vectors and testing cosine similarity between two sets of vectors. It employs machine learning techniques, specifically deep neural networks, implemented using TensorFlow and Keras libraries. The script reads data from text files containing vectors, preprocesses the data, trains two different models, and evaluates their performance.

### Example usage:

```sh
python paper_prediction_model.py -i <path_to_vectors_model>
```

The script reads the vector data from text files located in the specified folder (or the default path) and preprocesses the data.

Two different models are trained with the processed data:

1. Model 1: Concatenates two sets of vectors and trains a deep neural network on them.
2. Model 2: Trains a deep neural network using only one set of vectors.
3. After training, the script evaluates the cosine similarity between the predicted and actual vectors for a single example.
4. The training process is visualized by plotting the mean squared error (MSE) for both training and validation data during each epoch.


### Description

- -i, --input: The path to the folder containing the vector data files. If not provided, the default path will be used.

### Output

The script will output the following information:

1. The total number of papers: The total number of papers represented by the vector data.
2. Model 1's training process and validation loss graph: The graph showing the MSE improvement during training for Model 1.
3. Model 2's training process and validation loss graph: The graph showing the MSE improvement during training for Model 2.
4. Cosine similarity between predicted and actual vectors: The similarity measure between the predicted and actual vectors for a single example.
5. The trained models will be saved in the files all_modelo.h5 (Model 1) and rw_modelo.h5 (Model 2).

### Note

This README provides a general overview of the code and its usage. For detailed technical explanations and further customization, please refer to the comments within the code and consult the relevant libraries' documentation.


## Get Vectors from Prone Model using Title or ID

### Example usage:

```sh
python idx_to_vector_prone.py -i corpus_id -o "path/to/vectors" -m "path/to/prone"
python idx_to_vector_prone.py -t "Paper Title" -o "path/to/vectors" -m "path/to/prone"
python idx_to_vector_prone.py -I paper_ids.txt -o "path/to/vectors" -m "path/to/prone"
python idx_to_vector_prone.py -T paper_titles.txt -o "path/to/vectors" -m "path/to/prone"
```

### Description 
 

Command Line Arguments

The script can be executed from the command line using the following arguments:

- -i, --idx: Semantic Scholar paper_id for obtaining the embedding of a specific paper index.
- -t, --title: Paper title for obtaining the embedding of a specific paper.
- -I, --idxs: Path to a file containing a list of Semantic Scholar paper_ids for obtaining embeddings in batch.
- -T, --titles: Path to a file containing a list of paper titles for obtaining embeddings in batch.
- -o, --output: Output path for saving the embeddings (default: /mnt/c/Rodolfo/Desarrollo/JSALT_2023/vectors_prone).
- -m, --model: Path to the Prone model (default: /mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model).


### Output

The embeddings will be saved as joblib files in the specified output path. For single paper embeddings, the file will be named [paper_id]_prone.jbl, and for batch embeddings, the file will be named idxs_prone.jbl for indices and titles_prone.jbl for titles.

### Note

Ensure that you have the required Python packages installed before running the script.
The script utilizes the Prone model, which should be located at the specified model path.
For using the script with Semantic Scholar API, make sure to set the environment variable containing your API key.