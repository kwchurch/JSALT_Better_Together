# Better Together Team Github
# JSALT (Jelinek Summer Workshop on Speech and Language Technology): 

<h2>Useful links</h2>
<ol>
<li><a href="https://jsalt2023.univ-lemans.fr/en/better-together-text-context.html">Team Page</a></li>
<li><a href="https://northeastern.zoom.us/j/8963791015"> Zoom Link</a></li>
<li><a href="https://github.com/kwchurch/JSALT_Better_Together">Github with source code</a></li>
<li><a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F%7E%2F">large datasets from Globus</a></li>
<li><a href="slides">Slides</li>
<li><a href="https://docs.google.com/document/d/1rRRflCASHo7PFTBU6GqHK_g8twj1JgcXD8ijwpWY9m8/edit">Meeting Notes</a></li>
<li><a href="doc/Notation.md">Notation</a></li>
<li><a href="doc/deliverables.md">Deliverables</a></li>
<li><a href="examples/similar_documents/reading_list">Reading List</a></li>
<li><a href="https://docs.google.com/spreadsheets/d/1JMq-jR4M8KU119cvglUDmMwwzd60Z3vyvn3VqhPn9EY/view#gid=1450677429">SciRepEval Baselines</a></li>
<li><a href="doc/Similar_Venues.md">Similar Venues</a></li>
<li><a href="doc/whatswhere.md">What's Where</a> (doc on big files on Globus)</li>
<li><a href="http://34.204.188.58//similar.html">web service (on Amazon AWS)</a></li>
</ol>

<h2>Installation</h2>

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
