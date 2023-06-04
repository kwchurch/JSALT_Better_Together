# Similar Venues

<p>

Suppose we have an embedding: M.  Let E =  M @ M^T > 0.95 be evidence ( papers that are very similar to one another).
<p>
If we have a matrix V that maps venues to papers, then V @ E @ V^T is an estimate of similarites between venues.  The following shows some (partial) results.
<p>
We can come up with lots of matrices like V that assigns groups of papers to classes.  Suppose A maps between authors and the papers they wrote.
<p>
Lots of issues: normalization, etc.
<p>
Hypothesis, while we cannot materialize M @ M^T, we can estimate E (using indexes for approximate nearest neighbors).  That is, for each pi (permutation/index), we can
compute cosines for papers near one another in pi.

<p>

This output is $JSALTdir/eval/results/venue/venue.hist5.txt, which you can get to from <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F%7E%2F">large datasets from Globus</a>.  Unfortunately, our machines have some scheduled down time, so this data is also posted here:
<a href="https://drive.google.com/file/d/1jP7UXcQv8b76SwzoPJtQTxZnzeR0qb9v/view?usp=sharing">Download zip file</a>

<p>

Here are the top 20 Venues (by evidence):

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
</tr>
<tr>
<td>145902</td>
<td>Nature</td>
</tr>
<tr>
<td>122058</td>
<td>Acta Crystallographica Section E</td>
</tr>
<tr>
<td>102239</td>
<td>Journal of Biological Chemistry</td>
</tr>
<tr>
<td>84037</td>
<td>Reactions weekly</td>
</tr>
<tr>
<td>78778</td>
<td>Physical Review Letters</td>
</tr>
<tr>
<td>67424</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>66915</td>
<td>Journal of Virology</td>
</tr>
<tr>
<td>64567</td>
<td>Journal of Chemical Physics</td>
</tr>
<tr>
<td>59036</td>
<td>Journal of the American Chemical Society</td>
</tr>
<tr>
<td>57543</td>
<td>Organic Letters</td>
</tr>
<tr>
<td>57412</td>
<td>Behavioral and Brain Sciences</td>
</tr>
<tr>
<td>54175</td>
<td>Science</td>
</tr>
<tr>
<td>52814</td>
<td>Angewandte Chemie</td>
</tr>
<tr>
<td>48221</td>
<td>ACS Applied Materials and Interfaces</td>
</tr>
<tr>
<td>44904</td>
<td>Bioresource Technology</td>
</tr>
<tr>
<td>44513</td>
<td>British medical journal</td>
</tr>
<tr>
<td>44389</td>
<td>Journal of Bacteriology</td>
</tr>
<tr>
<td>39653</td>
<td>Biochimica et Biophysica Acta</td>
</tr>
<tr>
<td>37324</td>
<td>Journal of Organic Chemistry</td>
</tr>
<tr>
<td>36387</td>
<td>Optics Express</td>
</tr>
</table></html>

Here are the top 50 Venues (by evidence) mactching 'Comp.*Ling':

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>7931</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>4052</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>3932</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
</tr>
<tr>
<td>3619</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>2205</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>2070</td>
<td>International Conference on Computational Linguistics</td>
<td>International Conference on Computational Linguistics</td>
</tr>
<tr>
<td>2059</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>International Conference on Computational Linguistics</td>
</tr>
<tr>
<td>1997</td>
<td>International Conference on Computational Linguistics</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>1716</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>1693</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>International Conference on Language Resources and Evaluation</td>
</tr>
<tr>
<td>1678</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>1585</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
</tr>
<tr>
<td>1393</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>1153</td>
<td>International Conference on Computational Linguistics</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>1138</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>Findings</td>
</tr>
<tr>
<td>1122</td>
<td>International Conference on Computational Linguistics</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
</tr>
<tr>
<td>1106</td>
<td>AAAI Conference on Artificial Intelligence</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>973</td>
<td>Findings</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>882</td>
<td>International Conference on Language Resources and Evaluation</td>
<td>International Conference on Computational Linguistics</td>
</tr>
<tr>
<td>866</td>
<td>International Conference on Computational Linguistics</td>
<td>International Conference on Language Resources and Evaluation</td>
</tr>
<tr>
<td>841</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>International Workshop on Semantic Evaluation</td>
</tr>
<tr>
<td>832</td>
<td>International Workshop on Semantic Evaluation</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>830</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>810</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>668</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>560</td>
<td>International Joint Conference on Artificial Intelligence</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>529</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>International Conference on Computational Linguistics</td>
</tr>
<tr>
<td>484</td>
<td>International Conference on Computational Linguistics</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>482</td>
<td>International Conference on Computational Linguistics</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>477</td>
<td>International Conference on Language Resources and Evaluation</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>475</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>International Conference on Computational Linguistics</td>
</tr>
<tr>
<td>462</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
</tr>
<tr>
<td>436</td>
<td>International Joint Conference on Natural Language Processing</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>419</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>416</td>
<td>International Conference on Computational Linguistics</td>
<td>International Workshop on Semantic Evaluation</td>
</tr>
<tr>
<td>410</td>
<td>International Workshop on Semantic Evaluation</td>
<td>International Conference on Computational Linguistics</td>
</tr>
<tr>
<td>405</td>
<td>Conference on Machine Translation</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>400</td>
<td>International Workshop on Spoken Language Translation</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>386</td>
<td>Conference on Computational Natural Language Learning</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>361</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>International Workshop on Semantic Evaluation</td>
</tr>
<tr>
<td>359</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>356</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>AAAI Conference on Artificial Intelligence</td>
</tr>
<tr>
<td>346</td>
<td>Machine Translation Summit</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>341</td>
<td>International Conference on Learning Representations</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>333</td>
<td>International Workshop on Semantic Evaluation</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>319</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
<td>International Conference on Language Resources and Evaluation</td>
</tr>
<tr>
<td>317</td>
<td>International Conference on Language Resources and Evaluation</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>309</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>Findings</td>
</tr>
<tr>
<td>287</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>Conference of the European Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>252</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
<td>Interspeech</td>
</tr>
</table></html>

Here are the top 10 Venues machine 'Mach.*Trans':

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>686</td>
<td>Machine Translation Summit</td>
<td>Machine Translation Summit</td>
</tr>
<tr>
<td>493</td>
<td>Conference on Machine Translation</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>405</td>
<td>Conference on Machine Translation</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>346</td>
<td>Machine Translation Summit</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>335</td>
<td>European Association for Machine Translation Conferences/Workshops</td>
<td>European Association for Machine Translation Conferences/Workshops</td>
</tr>
<tr>
<td>285</td>
<td>Machine Translation Summit</td>
<td>International Workshop on Spoken Language Translation</td>
</tr>
<tr>
<td>272</td>
<td>European Association for Machine Translation Conferences/Workshops</td>
<td>Machine Translation Summit</td>
</tr>
<tr>
<td>260</td>
<td>Conference of the Association for Machine Translation in the Americas</td>
<td>Machine Translation Summit</td>
</tr>
<tr>
<td>260</td>
<td>Machine Translation Summit</td>
<td>International Conference on Language Resources and Evaluation</td>
</tr>
<tr>
<td>245</td>
<td>Machine Translation Summit</td>
<td>Conference of the Association for Machine Translation in the Americas</td>
</tr>
</table></html>

Here are top 20 matching NeurIPS:

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>161</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>33</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>Annual Meeting of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>32</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
</tr>
<tr>
<td>30</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>Neural Information Processing Systems</td>
</tr>
<tr>
<td>27</td>
<td>Preregister@NeurIPS</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>26</td>
<td>ViGIL@NeurIPS</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>21</td>
<td>2019 Fifth Workshop on Energy Efficient Machine Learning and Cognitive Computing - NeurIPS Edition (EMC2-NIPS)</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>16</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>International Conference on Learning Representations</td>
</tr>
<tr>
<td>15</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>IEEE International Conference on Computer Vision</td>
</tr>
<tr>
<td>14</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>North American Chapter of the Association for Computational Linguistics</td>
</tr>
<tr>
<td>13</td>
<td>ML4H@NeurIPS</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>12</td>
<td>ICBINB@NeurIPS</td>
<td>International Conference on Learning Representations</td>
</tr>
<tr>
<td>12</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>AAAI Conference on Artificial Intelligence</td>
</tr>
<tr>
<td>10</td>
<td>NeurIPS Datasets and Benchmarks</td>
<td>International Conference on Machine Learning</td>
</tr>
<tr>
<td>9</td>
<td>ViGIL@NeurIPS</td>
<td>Computer Vision and Pattern Recognition</td>
</tr>
<tr>
<td>7</td>
<td>ViGIL@NeurIPS</td>
<td>International Conference on Learning Representations</td>
</tr>
<tr>
<td>7</td>
<td>ViGIL@NeurIPS</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
</tr>
<tr>
<td>6</td>
<td>ICBINB@NeurIPS</td>
<td>International Conference on Machine Learning</td>
</tr>
<tr>
<td>4</td>
<td>Preregister@NeurIPS</td>
<td>Computer Vision and Pattern Recognition</td>
</tr>
<tr>
<td>4</td>
<td>ViGIL@NeurIPS</td>
<td>Neural Information Processing Systems</td>
</tr>
</table></html>

Vision:

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>31754</td>
<td>Vision Research</td>
<td>Vision Research</td>
</tr>
<tr>
<td>8083</td>
<td>Computer Vision and Pattern Recognition</td>
<td>Computer Vision and Pattern Recognition</td>
</tr>
<tr>
<td>6959</td>
<td>Computer Vision and Pattern Recognition</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>6167</td>
<td>Journal of Vision</td>
<td>Vision Research</td>
</tr>
<tr>
<td>5783</td>
<td>Journal of Vision</td>
<td>Journal of Vision</td>
</tr>
<tr>
<td>3456</td>
<td>Computer Vision and Pattern Recognition</td>
<td>IEEE International Conference on Computer Vision</td>
</tr>
<tr>
<td>3286</td>
<td>IEEE International Conference on Computer Vision</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>3278</td>
<td>IEEE International Conference on Computer Vision</td>
<td>Computer Vision and Pattern Recognition</td>
</tr>
<tr>
<td>2944</td>
<td>Journal of The Optical Society of America A-optics Image Science and Vision</td>
<td>Journal of The Optical Society of America A-optics Image Science and Vision</td>
</tr>
<tr>
<td>2786</td>
<td>Optometry and Vision Science</td>
<td>Optometry and Vision Science</td>
</tr>
</table></html>

Speech:

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>12824</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
</tr>
<tr>
<td>4535</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>arXiv.org</td>
</tr>
<tr>
<td>3803</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>IEEE Transactions on Signal Processing</td>
</tr>
<tr>
<td>2215</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>European Signal Processing Conference</td>
</tr>
<tr>
<td>2058</td>
<td>Journal of Speech, Language and Hearing Research</td>
<td>Journal of Speech, Language and Hearing Research</td>
</tr>
<tr>
<td>1526</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>IEEE Signal Processing Letters</td>
</tr>
<tr>
<td>1447</td>
<td>Journal of Speech and Hearing Research</td>
<td>Journal of Speech and Hearing Research</td>
</tr>
<tr>
<td>1241</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>Signal Processing</td>
</tr>
<tr>
<td>1060</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>IEEE Transactions on Communications</td>
</tr>
<tr>
<td>1009</td>
<td>IEEE International Conference on Acoustics, Speech, and Signal Processing</td>
<td>IEEE Transactions on Information Theory</td>
</tr>
</table></html>

Psychology:

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>3613</td>
<td>Journal of Experimental Psychology</td>
<td>Journal of Experimental Psychology</td>
</tr>
<tr>
<td>3075</td>
<td>Frontiers in Psychology</td>
<td>Frontiers in Psychology</td>
</tr>
<tr>
<td>3057</td>
<td>Journal of Comparative and Physiological Psychology</td>
<td>Journal of Comparative and Physiological Psychology</td>
</tr>
<tr>
<td>2805</td>
<td>Journal of Experimental Psychology: Human Perception and Performance</td>
<td>Journal of Experimental Psychology: Human Perception and Performance</td>
</tr>
<tr>
<td>2499</td>
<td>Journal of Experimental Psychology. Learning, Memory and Cognition</td>
<td>Journal of Experimental Psychology. Learning, Memory and Cognition</td>
</tr>
<tr>
<td>2400</td>
<td>Journal of Experimental Psychology. Learning, Memory and Cognition</td>
<td>Memory & Cognition</td>
</tr>
<tr>
<td>2261</td>
<td>Journal of Experimental Child Psychology</td>
<td>Journal of Experimental Child Psychology</td>
</tr>
<tr>
<td>2042</td>
<td>Journal of Experimental Psychology: Human Perception and Performance</td>
<td>Perception & Psychophysics</td>
</tr>
<tr>
<td>1913</td>
<td>Journal of Abnormal Psychology</td>
<td>Journal of Abnormal Psychology</td>
</tr>
<tr>
<td>1785</td>
<td>Journal of Comparative and Physiological Psychology</td>
<td>Physiology and Behavior</td>
</tr>
</table></html>

Frontiers:

<html><table><tr>
<th>Evidence</th>
<th>Venue</th>
<th>Venue</th>
</tr>
<tr>
<td>5253</td>
<td>Frontiers in Microbiology</td>
<td>Frontiers in Microbiology</td>
</tr>
<tr>
<td>4448</td>
<td>Frontiers in Plant Science</td>
<td>Frontiers in Plant Science</td>
</tr>
<tr>
<td>3615</td>
<td>Frontiers in Immunology</td>
<td>Frontiers in Immunology</td>
</tr>
<tr>
<td>3075</td>
<td>Frontiers in Psychology</td>
<td>Frontiers in Psychology</td>
</tr>
<tr>
<td>2452</td>
<td>Frontiers in Microbiology</td>
<td>PLoS ONE</td>
</tr>
<tr>
<td>2263</td>
<td>Frontiers in Plant Science</td>
<td>Plant Physiology</td>
</tr>
<tr>
<td>2027</td>
<td>Frontiers in Immunology</td>
<td>Journal of Immunology</td>
</tr>
<tr>
<td>2025</td>
<td>Frontiers in Plant Science</td>
<td>PLoS ONE</td>
</tr>
<tr>
<td>1905</td>
<td>Frontiers in Oncology</td>
<td>Frontiers in Oncology</td>
</tr>
<tr>
<td>1897</td>
<td>Frontiers in Plant Science</td>
<td>Journal of Experimental Botany</td>
</tr>
</table></html>