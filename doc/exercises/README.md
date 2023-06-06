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

<h2>Download the scidocs_cite evaluation</h2>

Hint: <a href="https://pypi.org/project/datasets/">pip install datasets</a>

```python
ds = datasets.load_dataset('allenai/scirepeval_test', 'scidocs_cite')
```

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


