#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <search.h>

int topK = 20;
float T = 10.0;


double lookup(struct bigram *query, char *fn)
{
  long N;
  struct bigram *b = (struct bigram *)mmapfile(fn, &N);
  N /= sizeof(struct bigram);
  struct bigram *found = (struct bigram *)bsearch(query, b, N, sizeof(struct bigram), bigram_compare);
  // struct bigram *found = (struct bigram *)bsearch(query, b, N, sizeof(struct bigram), (__compar_fn_t)bigram_compare);
  if(!found) return 0;
  return found->val;
}

void usage()
{
  fatal("usage: filter_bigram --topK <int> --threshold <float> --bigrams <bigrams>");
}

int float_compare(float *a, float *b)
{
  if(*a < *b) return 1;
  if(*a > *b) return -1;
  return 0;
}

double find_val_threshold(struct bigram *bigrams, struct bigram *end)
{
  int nbuf = 0;
  float *buf = (float *)malloc((end-bigrams) * sizeof(float));
  if(!buf) fatal("malloc failed");
  float *buf_end = buf + (end-bigrams);
  struct bigram *b;
  
  for(b=bigrams;b<end;b++) {
    if(b->val < T && b->elts[0] != b->elts[1])
      buf[nbuf++] = b->val;
  }

  qsort(buf, nbuf, sizeof(float), float_compare);
  double res = buf[topK];
  free(buf);
  return res;
}
  
struct bigram *end_of_run(struct bigram *bigrams, struct bigram *end)
{
  struct bigram *b;
  if(bigrams+1 >= end) return end;
  for(b = bigrams+1;b<end;b++)
    if(b[0].elts[0] != bigrams[0].elts[0])
      return b;
  if(b >= end) return end;
  return b;
}

int fill_buf(struct bigram *res, struct bigram *b, struct bigram *bend, float threshold)
{
  int n=0;
  for(; b < bend && n < topK; b++)
    if(b->val >= threshold && b->val < T && b->elts[0] != b->elts[1])
      res[n++] = *b;
  return n;
}
       
int main(int ac, char **av)
{
  int i;
  long N = 0;
  struct bigram *b = NULL;
  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--topK") == 0) topK = atoi(av[++i]);
    else if(strcmp(av[i], "--threshold") == 0) T = atof(av[++i]);
    else if(strcmp(av[i], "--bigrams") == 0) {
      b = (struct bigram *)mmapfile(av[++i], &N);
      N /= sizeof(struct bigram);
      if(N <= 0) fatal("expected to see more bigrams");
    }
    else usage();
  }

  if(!b) usage();
  struct bigram *bend = b + N;
  struct bigram *erun;

  struct bigram *buf = (struct bigram *)malloc(topK * sizeof(struct bigram));
  int nbuf;

  for( ; b < bend; b = erun) {
    erun = end_of_run(b,bend);
    // fprintf(stderr, "%d: run of %d\n", b[0].elts[0], erun - b);
    float threshold = find_val_threshold(b, erun);
    // fprintf(stderr, "threshold: %f\n", threshold);
    nbuf = fill_buf(buf, b, erun, threshold);
    // fprintf(stderr, "found %d\n", nbuf);
    if(nbuf <= 0) continue;
    if(fwrite(buf, sizeof(struct bigram), nbuf, stdout) != nbuf)
      fatal("write failed");
  }
  return 0;
}
