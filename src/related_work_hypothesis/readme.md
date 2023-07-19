# Related Work Hypothesis 
 
 
## Get Vectors from Prone Model using Title or ID

### Example usage:

```sh
python script.py -i corpus_id -o "path/to/vectors" -m "path/to/prone"
python script.py -t "Paper Title" -o "path/to/vectors" -m "path/to/prone"
python script.py -I paper_ids.txt -o "path/to/vectors" -m "path/to/prone"
python script.py -T paper_titles.txt -o "path/to/vectors" -m "path/to/prone"
```

### Description 
 
Run the script from the command line with the following arguments: 
 
-  -i  or  --idx : Semantic Scholar paper_id 
-  -t  or  --title : Paper Title 
-  -I  or  --idxs : List of Semantic Scholar paper_ids 
-  -T  or  --titles : List of Paper Titles 
-  -o  or  --output : Output path (default: '/mnt/c/Rodolfo/Desarrollo/JSALT_2023/vectors_prone') 
-  -m  or  --model : Model path (default: '/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model') 



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