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
<td>1592</td>
<td>IEEE Transactions on Pattern Analysis and Machine Intelligence</td>
<td>IEEE Transactions on Pattern Analysis and Machine Intelligence</td>
</tr>
<tr>
<td>732</td>
<td>IEEE Transactions on Pattern Analysis and Machine Intelligence</td>
<td>IEEE Transactions on Image Processing</td>
</tr>
<tr>
<td>686</td>
<td>Machine Translation Summit</td>
<td>Machine Translation Summit</td>
</tr>
<tr>
<td>574</td>
<td>Conference on Empirical Methods in Natural Language Processing</td>
<td>Conference on Machine Translation</td>
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
<td>388</td>
<td>British Machine Vision Conference</td>
<td>IEEE Transactions on Pattern Analysis and Machine Intelligence</td>
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
<td>320</td>
<td>International Conference on Language Resources and Evaluation</td>
<td>Machine Translation Summit</td>
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