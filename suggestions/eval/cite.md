# Suggestions for cite evaluation

Split corpusIds into 100 bins (by publication date); see <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Fj.ortega%2Fgraphs.V2%2F">here</a> for an example.  There are almost 100 files there with 3-digit names.
<p>
The first 50 bins are for training.  You can do whatever you want with those ids, and any of their properties.
<p>

The next 50 bins are for testing.  The task is to input an id, and
output 10 candidate citations, with 10 probabilities, <i>p</i> (that sum to 1).

<p>
Scoring suggestions:
<ol>
<li>Simple method: P@10 (ignore probabilities)</li>
<li>Weighted method: We need a method to combine the vector of 10 <i>p</i> with a vector of 10 ground truth citations, <i>c</i> such as: -c*log(p)</li>
</ol>

Expectation: Systems will be more successful when tested on bins that are closer in time to training