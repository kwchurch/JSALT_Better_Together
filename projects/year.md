# Suggestion for project: predict year

How to get data?

```sh
# $JSALTsrc/C/print_bigrams < $proposed/bigrams | head
# 0.93	2	1882
# 0.92	2	73308
# 0.92	2	96619
# 0.87	2	106894
# 0.93	2	115452
# 0.91	2	159197
# 0.92	2	199806
# 0.90	2	220406
# 0.94	2	256488
# 0.94	2	282449
```

This outputs a cosine and two corpus ids, id1 and id2.
<p>
Let's assume you have a way to convert corpus ids to bins (or years).
<p>
Compute a matrix of counts, C, with shape: 100 by 100.  Let C[i,j] be the number
of bigrams where i is bin(id1) and j is bin(id2).
<p>
Use imshow to plot C
<p>
Variations:
<ol>
<li>filter out bigrams with cosines less than T (for T approx 0.95); does that change the picture?</li>
<li>replace $proposed with $specter, $specter2, $scincl, etc.</li>
</ol>

