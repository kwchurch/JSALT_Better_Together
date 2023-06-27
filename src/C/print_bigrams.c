#include <stdio.h>
#include "util.h"
#include <memory.h>

struct head {
  struct bigram *b, *end, *ptr;
};

/* int bigram_compare(struct bigram *a, struct bigram *b) */
/* { */
/*   return memcmp(a->elts, b->elts, 2*sizeof(int)); */
/* } */

void fill_vals(float *vals, struct bigram *nbigram, struct head *heads, int nheads)
{
  int i;
  memset(vals, 0, sizeof(float)*nheads);
  for(i=0;i<nheads;i++)
    if(bigram_compare(nbigram, heads[i].ptr) == 0)
      vals[i] = heads[i].ptr->val;
    else vals[i] = -1.0;
}

int done(struct head *heads, int nheads)
{
  int i;
  for(i=0;i<nheads;i++)
    if(heads->ptr < heads->end) return 0;
  return 1;
}

struct bigram *next_bigram(struct head *heads, int nheads)
{
  struct head *end = heads + nheads;
  struct head *res = heads++;
  for( ; heads < end; heads++)
    if(bigram_compare(heads->ptr, res->ptr) < 0)
      res=heads;
  return res->ptr;
}

void advance(struct head *heads, int nheads, struct bigram *next_bigram)
{
  int i;
  for(i=0;i<nheads;i++) {
    if(heads[i].ptr < heads[i].end && bigram_compare(heads[i].ptr, next_bigram) <= 0)
      (heads[i].ptr)++;
  }
}

void output(float *vals, int nvals, struct bigram *b)
{
  int i;
  for(i=0;i<nvals;i++)
    printf("%0.3f\t", vals[i]);
  printf("%d\t%d\n", b->elts[0], b->elts[1]);
}

int main(int ac, char **av)
{
  if(ac == 1) {
    struct bigram b;
    while(fread(&b, sizeof(b), 1, stdin) > 0) {
      printf("%0.2f\t%d\t%d\n", b.val, b.elts[0], b.elts[1]);
    }
  }

  else {
    int i; long n;

    int nheads = ac-1;

    // fprintf(stderr, "nheads = %d\n", nheads);

    float *vals = (float *)malloc(sizeof(float) * nheads);
    memset(vals, 0, sizeof(float) * nheads);

    struct head *heads = (struct head *)malloc((ac-1) * sizeof(struct head));
    memset(heads, 0, nheads * sizeof(struct head));
    for(i=1;i<ac;i++) {
      struct head *h = &heads[i-1];
      h->ptr = h->b = (struct bigram *)mmapfile(av[i], &n);
      n /= sizeof(struct bigram);
      h->end = h->b + n;
    }
    
    while(!done(heads, nheads)) {
      struct bigram *nbigram = next_bigram(heads, nheads);
      fill_vals(vals, nbigram, heads, nheads);
      output(vals, nheads, nbigram);
      advance(heads, nheads, nbigram);
    }
  }
}
