# Scripts for Semantic Scholar API

<b>NOTE</b>: Many of the programs below support the environment variable, SPECTER_API_KEY.
This can be set to a secret, which is important for heavy usage.  Ask me for the secret, if
you are interested.
<p>
The Semantic Scholar API is <a href="https://www.semanticscholar.org/product/api">here</a>.
The following scripts use that to:
<ol>
<li>Input paper ids; output useful fields (as json)</li>
<li>Input paper ids; output references and citations (as tsv)</li>
</ol>

<h2>Fetch Titles</h2>


```sh
echo 'DeepWalk' | python $JSALTsrc/fetch_from_title.py
# 3 matches:	DeepWalk
fff114cbba4f3ba900f33da574283e3de7f26c83	DeepWalk: online learning of social representations	DeepWalk
689c72d2374b22ebca6ac7b588d84bc87f3b3109	DeepWalking: Enabling Smartphone-Based Walking Speed Estimation Using Deep Learning	DeepWalk
f6bdc38fd4665a25f79dc37a462045a07c79a639	DeepWalk: Omnidirectional Bipedal Gait by Deep Reinforcement Learning	DeepWalk
```

<h2>Fetch from Semantic Scholar API</h2>
Some examples of usage

```sh
echo 232040593 | python $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
# {'paperId': '6d9727f1f058614cada3fe296eeebd8ec4fc512a', '
#              externalIds': {'DBLP': 'conf/fat/BenderGMS21', 'DOI': '10.1145/3442188.3445922', 'CorpusId': 232040593},
#              'title': 'On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜'}}`
```

There are many ways to specify paper ids.  All of these produce the same results:
```sh
echo 9558665 | python $JSALTsrc/fetch_from_semantic_scholar_api.py --fields title,externalIds
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

In addition to ad hoc requests, Semantic Scholar also supports bulk downloads, where
you can download many of these same fields for all papers in the system.  They provide
snapshots (releases) every few weeks.
<p>
There is also support for querying by authors:

```sh
echo 2244184 | python $JSALTsrc/fetch_from_semantic_scholar_api.py --API author --fields name,externalIds,hIndex,paperCount,citationCount | head
# {'authorId': '2244184', 'externalIds': {'DBLP': ['K. H. Church',
#   'Kenneth Church', 'Kenneth Church 0001', 'Kenneth W. Church',
#   'Kenneth Ward Church'], 'ORCID': '0000-0001-8378-6069'}, 'name':
#   'Kenneth Ward Church', 'paperCount': 225, 'citationCount': 18694,
#   'hIndex': 52}

# Output a list of papers with titles and citations
echo 2244184 | python $JSALTsrc/fetch_from_semantic_scholar_api.py --API author --fields name,externalIds,hIndex,paperCount,citationCount,papers.title,papers.citationCount
```

Generate a list of papers for an author, sorted by citations:

```sh
echo 2244184 |python $JSALTsrc/fetch_papers_from_authors.py | awk 'NR >  1' | sort -k4 -nr -t'	' | head
```

<h2>References and Citations</h2>

The following will output up to 1000 lines, one for each reference.
It will also output up to 1000 lines, one for each citation.  The
first line is a summary with the count of references and citations
(which may exceed 1000).  Subsequent lines start with either
"reference" or "citation".  The next two ids are the corpusId for the
query and the reference/citation.  The last two columns are the number
of citations and the title of the paper.

```sh
echo 232040593 | python $JSALTsrc/fetch_references_and_citations.py | head
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

<h2>Recommendations</h2>

Input a paper and output some recommendations.  The first two columns are the query id and the candidate id.
Col 3 is a cosine score.  Col 4 is a citation count.

```sh
echo fff114cbba4f3ba900f33da574283e3de7f26c83 | python $JSALTsrc/fetch_semantic_scholar_recommendations.py
# fff114cbba4f3ba900f33da574283e3de7f26c83	258060205	0.7751482087719826	2	A Comprehensive Survey on Deep Graph Representation Learning
# fff114cbba4f3ba900f33da574283e3de7f26c83	258011360	0.7550353496903267	0	Representation Learning for Texts and Graphs
# fff114cbba4f3ba900f33da574283e3de7f26c83	258171578	0.7626156134161819	0	Multi-View Graph Representation Learning Beyond Homophily
# fff114cbba4f3ba900f33da574283e3de7f26c83	258333932	0.7591129932705019	0	xGCN: An Extreme Graph Convolutional Network for Large-scale Social Link Prediction
# fff114cbba4f3ba900f33da574283e3de7f26c83	258180460	0.7546374271299047	0	The Deep Latent Position Topic Model for Clustering and Representation of Networks with Textual Edges
```

