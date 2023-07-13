# Prone Optimzation
# JSALT (Jelinek Summer Workshop on Speech and Language Technology): 

<h1>Cython Code Creation</h1>
<ol>
<li><a href="https://cython.readthedocs.io/en/latest/src/quickstart/build.html">Baseline Link</a></li>
<li><a href="https://www.peterbaumgartner.com/blog/intro-to-just-enough-cython-to-be-useful</a></li>
</ol>
Cython is a manner of compiling any Python code into its C equivalent.
It optimizes variables and other memory calls to run faster in C.
When used for Prone (ran 10 times taking the average), we were able to get several runs on average 10 seconds speedup (on a small fraction of the graph -- 10%).
The original TSVD code from Sci-Py that uses Python takes about 90 seconds on the Northeastern "short" queue CPU boxes, when using Cython-compiled Prone.py it runs in about 80 seconds (10% speed up).
<h2>Logic</h2>
In order to run Cython, you will need to:
```sh
pip install cython
python setup.py build_ext --inplace
```
This assumes that you have updated the setup.py file with your filename, please see the setup.py file for help.
That will create a binary C object (a .so file) that can then be used similar to the Python code by importing the name of your library.
For example, in this directory there is a "prone" library that can be imported.




<h2>Execution</h2>






<h2>DAX use for tiling and GPU/CPU runs</h2>

```sh
git clone https://github.com/kwchurch/JSALT_Better_Together
pip install -r requirements.txt
```

Some useful environment variables; you may need to set these up differently, depending on where you put stuff.
JSALTsrc should be assigned to the src directory in this repo.
JSALTdir should be assigned to the data from <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F%7E%2F">Globus</a>.

Some examples below depend on JSALTdir and some do not.  If you cannot download JSALTdir, try the examples that do not require that.

```sh
export JSALTdir=/work/k.church/JSALT-2023/
export JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

export specter=$JSALTdir/semantic_scholar/embeddings/specter
export specter2=$JSALTdir/semantic_scholar/embeddings/specter2
export proposed=$JSALTdir/semantic_scholar/embeddings/proposed
export scincl=$JSALTdir/semantic_scholar/embeddings/scincl
```

If you have access to the Northeastern Discovery Cluster,
you can request access to the cluster by filling out a ticket <a href="https://bit.ly/NURC-Software">here</a>,
and then you can use my settings for these environment variables.
You should also request to be added to the group: <i>nlp</i>.

<h2>Installation</h2>

```sh
git clone https://github.com/kwchurch/JSALT_Better_Together
pip install -r requirements.txt
# set environment variable JSALTsrc to the src directory in the repo.
# set environment variable JSALTdir to your local copy of the large data files.
```

<h2>Reading List (and Pre-computed Output)</h2>

See <a href="examples/similar_documents">here</a>, and especially <a href="examples/similar_documents/reading_list">this</a>.
The last example starts with papers we should all be reading, and finds some documents similar to those.


<h2>Examples</h2>


<ol>
<li>Depend on $JSALTsrc, but not $JSALTdir
   <ol>
   <li><a href="doc/semantic_scholar_API.md">Scripts for using Semantic Scholar API</a></li>
   <li><a href="doc/HuggingFace_embeddings.md">Scripts for using Models from HuggingFace</a></li>
   </ol></li>
<li>Depends on both $JSALTsrc and $JSALTdir
   <ol><li><a href="doc/find_similar_docs.md">Find similar documents</a></li>
   </ol></li>
</ol>
