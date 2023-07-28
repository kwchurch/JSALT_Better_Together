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

1. -i, --idx: Semantic Scholar paper_id for obtaining the embedding of a specific paper index.
2. -t, --title: Paper title for obtaining the embedding of a specific paper.
3. -I, --idxs: Path to a file containing a list of Semantic Scholar paper_ids for obtaining embeddings in batch.
4. -T, --titles: Path to a file containing a list of paper titles for obtaining embeddings in batch.
5. -o, --output: Output path for saving the embeddings (default: /mnt/c/Rodolfo/Desarrollo/JSALT_2023/vectors_prone).
6. -m, --model: Path to the Prone model (default: /mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model).



### Output

The embeddings will be saved as joblib files in the specified output path. For single paper embeddings, the file will be named [paper_id]_prone.jbl, and for batch embeddings, the file will be named idxs_prone.jbl for indices and titles_prone.jbl for titles.

### Note

Ensure that you have the required Python packages installed before running the script.
The script utilizes the Prone model, which should be located at the specified model path.
For using the script with Semantic Scholar API, make sure to set the environment variable containing your API key.



## Test Related Work References Hypothesis only 1 paper (Low-resource paper by Rodolfo)

### Example usage:

```sh
python test_papers_recommendation.py -r "path/to/all_references"  -w "path/to/related_work_references" -c "path/to/paper_to_compare"
```
 
### Description 
 
To run the script from the command line, use the following arguments: 

- -r or --ref: a text file containing all the references of a paper. 
- -w or --related: a text file containing the references of related work for a paper. 
- -c or --compare: compares the similarity of all the papers.


Enjoy using this script!