# Related Work Hypothesis 
 
 
## Get Vectors from Prone Model using Title or Id

### Example usage:

```sh
python script.py -i corpus_id -o "path/to/vectors" -m "path/to/prone"
python script.py -t "Paper Title" -o "path/to/vectors" -m "path/to/prone"
python script.py -I paper_ids.txt -o "path/to/vectors" -m "path/to/prone"
python script.py -T paper_titles.txt -o "path/to/vectors" -m "path/to/prone"
```


### Usage 
 
Run the script from the command line with the following arguments: 
 
-  -i  or  --idx : Semantic Scholar paper_id 
-  -t  or  --title : Paper Title 
-  -I  or  --idxs : List of Semantic Scholar paper_ids 
-  -T  or  --titles : List of Paper Titles 
-  -o  or  --output : Output path (default: '/mnt/c/Rodolfo/Desarrollo/JSALT_2023/vectors_prone') 
-  -m  or  --model : Model path (default: '/mnt/c/Rodolfo/Desarrollo/JSALT_2023/prone_model') 



 

 
Enjoy using this script!