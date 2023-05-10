# HuggingFace Embeddings

```sh
echo '232040593	On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?' | 
src/text_to_embedding.py --output /tmp/foobar --model allenai/specter2
```

This will read lines (tab delimited) with a corpusId in column 1 and text in column 2;
output goes to /tmp/foobar.kwc.i and /tmp/foobar.kwc.f.
The first file is a sequence of int32 (one for each input line);
The second file is a sequence float32 (one record of K=768 for each input line).
You can process these binary files in C or with numpy.fromfile.
There is an optional --model argument which allows you to specify models from HuggingFace.
