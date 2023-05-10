# Scripts for Semantic Scholar API

The Semantic Scholar API is <a href="https://www.semanticscholar.org/product/api">here</a>.
The following scripts use that to:
<ol>
<li>Input paper ids; output useful fields (as json)</li>
<li>Input paper ids; output references and citations (as tsv)</li>
</ol>


Some examples of usage

```sh
echo 232040593 | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
# {'paperId': '6d9727f1f058614cada3fe296eeebd8ec4fc512a', '
#              externalIds': {'DBLP': 'conf/fat/BenderGMS21', 'DOI': '10.1145/3442188.3445922', 'CorpusId': 232040593},
#              'title': 'On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜'}}`
```

There are many ways to specify paper ids.  All of these produce the same results:
```sh
echo 9558665 | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
echo 9e2caa39ac534744a180972a30a320ad0ae41ea3 | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
echo 'ACL:J90-1003' | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
echo 'MAG:3031337294' | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
echo 'DOI:10.3115/981623.981633' | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
```

The argument to --fields can make use of the following:
<ol>
<li>title</li>
<li>abstract</li>
<li>authors</li>
<li>externalIds (Semantic Scholar receives data from 7 sources: MAG (182M papers), DOI (114M papers), PubMed (35M), DBLP (6M), PubMedCentral (5M), ArXiv (2M), ACL (80k) </li>
<li>citationCount</li>
<li>referenceCount</li>
<li>citations (list of (up to 1000) papers)</li>
<li>references (list of (up to 1000) papers)</li>
<li>embedding (vector of 768 floats from Specter 1, a BERT-like model; this vector encodes titles and abstracts)</li>
<li>venue</li>
<li>fieldsOfStudy</li>
<li>s2fieldsOfStudy</li>
<li>openAccessPdf (URL to pdf versions of paper)</li>
<li>tldr (too long; didn't read -- summaries, often based on abstracts</li>
</ol>

<p>

The following will output up to 1000 lines, one for each reference.
It will also output up to 1000 lines, one for each citation.  The
first line is a summary with the count of references and citations
(which may exceed 1000).  Subsequent lines start with either
"reference" or "citation".  The next two ids are the corpusId for the
query and the reference/citation.  The last two columns are the number
of citations and the title of the paper.

```sh
echo 232040593 | src/fetch_references_and_citations.py | head
query	156 references	1113 citations	On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜
reference	232040593	243950006	2	The Five Hundred Year Rebellion: Indigenous Movements and the Decolonization of History in Bolivia
reference	232040593	243615599	57	The Argonauts
reference	232040593	231573431	674	Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity
reference	232040593	230435736	400	The Pile: An 800GB Dataset of Diverse Text for Language Modeling
reference	232040593	229156229	515	Extracting Training Data from Large Language Models
reference	232040593	225040574	843	mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer
reference	232040593	220265858	392	GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
reference	232040593	220265500	193	Large image datasets: A pyrrhic win for computer vision?
reference	232040593	219530686	90	Detecting Emergent Intersectional Biases: Contextualized Word Embeddings Contain a Distribution of Human-like Biases
```

