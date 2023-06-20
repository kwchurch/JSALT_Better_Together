# Exercises

<h2>Paper Id to Properties</h2>

See <a href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/doc/semantic_scholar_API.md">instructions for using Semantic Scholar API</a>.
<p>
Write a function that uses this API to input a list of paper ids and outputs a json object each id with:
<ol>
<li>title</li>
<li>abstract</li>
<li>ExternalIds</li>
<li>embedding</li>
<li>references</li>
<li>citations</li>
<li>bibtex entries</li>
</ol>

Run your function on the ``DeepWalk'' paper.

<h2>Text to Vectors</h2>
See <a href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/doc/HuggingFace_embeddings.md">instructions for using models on HuggingFace to convert text to vectors</a>.
<p>
Write a function that inputs ids and a model on HuggingFace and outputs embeddings.  The function should get the title and abstract and use that as input to the HuggingFace model.
<p>
Run the model on the ``DeepWalk'' paper and each of the papers that that paper references.
<p>
Do this for four models, <i>f</i>:
<ol>
<li><a href="https://huggingface.co/allenai/specter2">allenai/specter2</a></li>
<li><a href="https://huggingface.co/allenai/specter">allenai/specter</a></li>
<li><a href="https://huggingface.co/malteos/scincl">malteos/scincl</a></li>
<li><a href="https://huggingface.co/michiyasunaga/LinkBERT-base">michiyasunaga/LinkBERT-base</a></li>
</ol>

We will refer to vectors of d as f(d).  We will add subscripts to f as appropriate to make
it clear which model we are using for f.

<h2>Plotting Vectors</h2>

For the vectors computed above, project them down to two dimensions and plot them as a scatter plot.

<h2>Citing Sentences</h2>

Pull citing sentences for Turing's paper with this:

```sh
echo 73712 | $JSALTsrc/fetch_from_semantic_scholar_api.py --citations --limit 1000 --fields contexts
```

For more information on Turing's paper:

```sh
echo 73712 | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields externalIds,title,authors,citationStyles,url
```

Count frequency of <a
href="https://plato.stanford.edu/entries/turing-machine/">Turing
Machines</a> and <a
href="https://en.wikipedia.org/wiki/Halting_problem">Halting
Problem</a> in these contexts.  How often do these terms appear in
Turing's original paper?

Create vectors for these contexts.  Use kmeans to create a few centroids for these vectors.

<h2>Download the scidocs_cite evaluation</h2>

Hint: <a href="https://pypi.org/project/datasets/">pip install datasets</a>

```python
ds = datasets.load_dataset('allenai/scirepeval_test', 'scidocs_cite')
```

There are 29928 rows in the test set like this:

```python
ds['test'][0:3]
# {'query_id': '78495383450e02c5fe817e408726134b3084905d', 'cand_id': '632589828c8b9fca2c3a59e97451fde8fa7d188d', 'score': 1}
```

See discussion of <i>Direct Citations</i> in <a
href="https://arxiv.org/pdf/2004.07180.pdf">Specter paper</a>.  Use
the API above to verify that the scores are 1 if (and only if)
query_id cites cand_id.


<h2>Replicate the centroid approximation plot</h2>

<ol>
<li>For as many documents, <i>d</i>, in <i>scidocs_cite</i> as you can afford to use,
use the methods, <i>f</i>, above to estimate vectors: <i>f(d)</i>.</li>
<li>Estimate vectors for each of the references of <i>d</i>.</li>
<li>Let dhat be the centroid of the vectors for the references of d.
<li>Compute cosines: cos(d, dhat)</li>
<li>Do this for the four models above</li>
<li>Plot boxplots of cos(d, dhat), for each of the four models</li>
</ol>

<h2>Challenge!</h2>

Download zip file: <a href="https://drive.google.com/file/d/1tVJAjRGiOhI3NSIAxGzwqOSNodl7KjGJ/view?usp=sharing">here</a>.
<p>
This is the SciDocs cite task.  Baselines are <a href="https://docs.google.com/spreadsheets/d/1JMq-jR4M8KU119cvglUDmMwwzd60Z3vyvn3VqhPn9EY/view#gid=1450677429">here</a>.
<p>
Hint: most baselines focus on text (titles and abstracts).  The zip file contains embeddings from both Specter and proposed (ProNE) methods.  The proposed method is based on links in citation graph.  It is likely that some ensemble will do better than either by itself.
<p>
Note: baselines refer to several methods on HuggingFace including Specter, Specter2 and SciNCL.  Specter2 and SciNCL are improvements on Specter.
<p>
Good  luck!

