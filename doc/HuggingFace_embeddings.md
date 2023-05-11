# HuggingFace Embeddings

There are many ways to map strings (and documents) to vectors.
One way is to use the Semantic Scholar API for embeddings:

```sh
echo 232040593 | python $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,embedding
```

Another way is to run a model from HuggingFace.  The following uses:
<a href="https://huggingface.co/allenai/specter2">https://huggingface.co/allenai/specter2</a>
to map a string (second column) to a vector.  The method above requires the input to be a document id, unlike the method
below where the second column can be an arbitrary string.

```sh
echo '232040593	On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?' | 
python $JSALTsrc/text_to_embedding.py --output /tmp/foobar --model allenai/specter2
```

This will read lines (tab delimited) with a corpusId in column 1 and text in column 2;
output goes to two output files: /tmp/foobar.kwc.i and /tmp/foobar.kwc.f.

The first output file is a sequence of int32 (one for each input line);
The second output file is a sequence float32 (one record of K=768 for each input line).

You can process these binary files in C or with numpy.fromfile.

The --model argument allows you to specify models from HuggingFace such as:
<ol>
<li><a href="https://huggingface.co/allenai/specter2">allenai/specter2</a></li>
<li><a href="https://huggingface.co/allenai/specter">allenai/specter</a></li>
<li><a href="https://huggingface.co/malteos/scincl">malteos/scincl</a></li>
<li><a href="https://huggingface.co/michiyasunaga/LinkBERT-large">michiyasunaga/LinkBERT-large</a></li>
</ol>

