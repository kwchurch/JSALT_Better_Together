# Related Work Hypothesis 
 
 
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



## Test Related Work References Hypothesis only 1 paper (Low-resource paper by Rodolfo)

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


## Test Related Work References Hypothesis using Martin's File (over 400k papers)


### Example usage:

```sh
python rw_recommendation_case_2.py -i <path_to_references_file> -m <path_to_model_directory>
```

### Description

- -i or --input (Positional Argument):

Description: This argument represents the path to the input JSONL file containing references to be processed.
Default Value: ../related_work_hypothesis/references_files/rw_citations.jsonl
Purpose: The code reads the data from this file, which should contain information about research papers, their related work citations, and other citations.
-m or --model (Positional Argument):

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




