# Suggested project: Random Walk Hypo

<ol>
<li>Let f(d) be a vector for d</li>
<li>and fhat(d) be a vector for d, using the centroid method on all references of d</li>
<li>and fhat_rw(d) be a vector for d, using the centroid method on related work references of d</li>
<li>and fhat_rw_bar(d) be a vector for d, using the centroid method on non-related work references of d</li>
</li>

Then we want to fit a regression:

f(d) ~ fhat_rw(d) + fhat_rw_bar(d)

to learn the weights on the two terms.


