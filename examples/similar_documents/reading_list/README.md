# Reading List (Dog Fooding)

We should develop some experience using our own tools (Dog Fooding).  
The examples in this directory were created by commands like this:

```sh
$JSALTsrc/near.sh 54609922 20 | $JSALTsrc/tsv_to_html.sh > Who_knows.md
```

The two arguments to near.sh specify a corpus id (from Semantic Scholar) and
a number of papers to find.  This will find 20 papers using Specter, plus 20 papers
using Proposed method.  The tsv_to_html command outputs html tables.  You may not want to do that if you are
reading the output in a text editor (as opposed to a web browser).
<p>

Some recommendations to read:

<ol>
<li>Methods
    <ol>
    <li><a href="https://aclanthology.org/2020.acl-main.207.pdf">Specter</a> (<a href="Specter.md">similar documents</a>)
(<a href="https://huggingface.co/allenai/specter2">HuggingFace</a>)
</li>
    <li><a href="https://www.ijcai.org/proceedings/2019/0594.pdf">ProNE</a> (<a href="ProNE.md">similar documents</a>) 
(<a href="https://github.com/VHRanger/nodevectors/blob/master/nodevectors/prone.py">code from nodevectors</a>)
(<a href="https://karateclub.readthedocs.io/en/latest/_modules/karateclub/node_embedding/neighbourhood/grarep.html">code from karateclub</a>)</li>
    <li><a href="https://dl.acm.org/doi/10.1145/2806416.2806512">GraRep</a>
(<a href="https://github.com/VHRanger/nodevectors/blob/master/nodevectors/grarep.py">code</a>) (<a href="GraRep.md">similar documents</a>)
</li>
<li><a href="https://karateclub.readthedocs.io/en/latest/modules/root.html?highlight=neighbourhood#neighbourhood-based-node-embedding">More code for more methods from karateclub</a></li>
    </ol>
</li>
<li>Evaluation Benchmarks, etc.
    <ol>
    <li><a href="https://arxiv.org/pdf/2103.09430.pdf">OGB (Open Graph Benchmark) (<a href="OGB_Benchmarks.md">similar documents</a>)</a></li>
    <li><a href="https://arxiv.org/abs/2211.13308">SciRepEval</a> (<a href="https://huggingface.co/datasets/allenai/scirepeval">HuggingFace</a>)</li>
(<a href="https://mimno.infosci.cornell.edu/data/nips_reviewer_data.tar.gz">tar file with benchmark</a>)
    <li><a href="https://arxiv.org/abs/2208.09126">GraphTTA: Test Time Adaptation on Graph Neural Networks</a></li>
    </ol>
</li>
<li> Use Cases
     <ol>
     	<li>Recommendation</li>	
	<li>Routing submissions to reviewers
		    <ol>
		        <li><a href="https://people.cs.umass.edu/~mccallum/papers/expertise-kdd2007s.pdf">Expertise Modeling for Matching Papers with Reviewers</a> (<a href="Expertise.md">similar documents</a>)</li>
		        <li><a href="http://engineering.nyu.edu/~suel/papers/reviewer.pdf">A Robust Model for Paper-Reviewer Assignment</a> (<a href="Reviewer.md">similar documents</a>)</li>
		    </ol></li>
         <li>Finding experts
                    <ol>
		        <li><a href="https://www.mitre.org/sites/default/files/pdf/06_1115.pdf">Expert Finding Systems</a> (<a href="Expert_finding.md">similar documents</a>)</li>
		        <li><a href="https://www.ics.uci.edu/~kobsa/papers/2003-JOCEC-kobsa.pdf">Expert-Finding Systems for Organizations: Problem and Domain Analysis and the DEMOIR Approach</a> (<a href="Expert_finding2.md">similar documents</a>)</li>
		        <li><a href="https://dl.acm.org/doi/10.1145/358916.358994">Expertise recommender: a flexible recommendation system and architecture</a> (<a href="Expert_finding3.md">similar documents</a>)</li>
		        <li><a href="https://cdn.aaai.org/AAAI/1996/AAAI96-002.pdf">The ContactFinder Agent: Answering Bulletin Board Questions with Referrals</a> (<a href="ContactFinder.md">similar documents</a>)</li>
		        <li><a href="https://dl.acm.org/doi/10.5555/3374430.3374464">Who knows: a system based on automatic representation of semantic structure</a> (<a href="Who_knows.md">similar documents</a>)</li>
		        <li><a href="https://aclanthology.org/C10-2145/">Citation Author Topic Model in Expert Search</a> (<a href="Expert.md">similar documents</a>)</li>
		    </ol></li>
         <li>Finding topics
	 	     <ol>
		        <li><a href="https://cocosci.princeton.edu/tom/papers/author_topics_kdd.pdf">Probabilistic Author-Topic Models for Information Discovery</a> (<a href="Author_Topic_Trends.md">similar documents</a>)</li>
		    </ol></li>
	<li>Muti-Document Summarization (<a href="https://paperswithcode.com/task/multi-document-summarization">papers with code</a>)
			<ol>
				<li><a href="https://aclanthology.org/2020.emnlp-main.648.pdf">Multi-XScience: A Large-scale Dataset for Extreme Multi-document Summarization of Scientific Articles</a> (<a href="automatic_related_work.md">similar documents</a>)</li>
				<li><a href="https://aclanthology.org/N18-2097.pdf">A Discourse-Aware Attention Model for
Abstractive Summarization of Long Documents</a> (<a href="summarize.md">similar documents</a>)</li>
				<li><a href="https://nlp.stanford.edu/pubs/bethard_2010_cikm_literature_search.pdf">Who Should I Cite?
Learning Literature Search Models from Citation Behavior</a> (<a href="who_should_I_cite.md">similar documents</a>)</li>
				<li><a href="https://aclanthology.org/P19-1102.pdf">Multi-News: a Large-Scale Multi-Document Summarization
Dataset and Abstractive Hierarchical Model</a> (<a href="MultiNews.md">similar documents</a>) (<a href="https://paperswithcode.com/dataset/multi-news">papers with code</a>)</li>
				<li><a href="https://aclanthology.org/K17-1021.pdf">A Supervised Approach to Extractive Summarisation of Scientific Papers</a> (<a href="Scientific_summarization.md">similar documents</a>)
(<a href="https://github.com/EdCo95/scientific-paper-summarisation">GitHub</a>)</li>
			</ol>
</li>
     </ol>
</li>
<li>Text Books
    <ol>
    <li><a href="https://www.cs.mcgill.ca/~wlh/grl_book/files/GRL_Book.pdf">Graph Representation Learning</a> (<a href="Graph_Learning_Book.md">similar documents</a>)</li>
    </ol>
</li>
<li>Theory
    <ol>
    <li><a href="https://arxiv.org/pdf/0711.0189.pdf">A Tutorial on Spectral Clustering</a> (<a href="Spectral_Graph_Theory.md">similar documents</a>)</li>   
    <li><a href="https://arxiv.org/pdf/1710.02971.pdf">Network Embedding as Matrix Factorization: Unifying
DeepWalk, LINE, PTE, and node2vec</a> (<a href="Unifying.md">similar documents</a>)</li>
    <li><a href="https://arxiv.org/pdf/1709.07604.pdf">A Comprehensive Survey of Graph Embedding:
Problems, Techniques and Applications</a> (<a href="Graph_Embedding_Survey.md">similar documents</a>)</li>
    </ol>
</li>
<li>Oldies but goodies
    <ol>
    <li><a href="https://aclanthology.org/N19-1423.pdf">BERT</a> (<a href="BERT.md">similar documents</a>)</li>
    <li><a href="https://arxiv.org/pdf/1402.3722.pdf">Word2vec Explained (<a href="Levy_and_Goldberg2014.md">similar documents</a>)</a></li>
    <li><a href="https://cs.stanford.edu/people/jure/pubs/node2vec-kdd16.pdf">Node2vec (<a href="node2vec.md">similar documents</a>)</a></li>
    <li><a href="https://arxiv.org/pdf/1403.6652.pdf">DeepWalk</a> (<a href="DeepWalk.md">similar documents</a>)</li>
    <li><a href="https://arxiv.org/pdf/1609.02907.pdf">Semi-Supervised Classification with Graph Convolutional Networks</a> (<a href="Kipf.md">similar documents</a>)</li>
    <li><a href="https://arxiv.org/pdf/0912.3848.pdf">Wavelets on Graphs via Spectral Graph Theory</a> (<a href="Hammond.md">similar documents</a>); section 6 introduces the Chebyshev approximation (used in ProNE)</li>
    <li><a href="https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=45bd1a97bde5ffe34638b37ad54d1b929568426d">Estimating the number of unseen species: How many
words did Shakespeare know?</a> (<a href="Skakespeare.md">similar documents</a>); section 6 introduces the Chebyshev approximation (used in ProNE)</li>
    </ol>
</li>
</ol>

