#include <stdio.h>
#include "util.h"
#include <memory.h>

struct head {
  struct lbigram *b, *end, *ptr;
};

void fill_vals(float *vals, struct lbigram *nbigram, struct head *heads, int nheads)
{
  int i;
  memset(vals, 0, sizeof(float)*nheads);
  for(i=0;i<nheads;i++)
    if(lbigram_compare(nbigram, heads[i].ptr) == 0)
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

struct lbigram *next_bigram(struct head *heads, int nheads)
{
  struct head *end = heads + nheads;
  struct head *res = heads++;
  for( ; heads < end; heads++)
    if(lbigram_compare(heads->ptr, res->ptr) < 0)
      res=heads;
  return res->ptr;
}

void advance(struct head *heads, int nheads, struct lbigram *next_bigram)
{
  int i;
  for(i=0;i<nheads;i++) {
    if(heads[i].ptr < heads[i].end && lbigram_compare(heads[i].ptr, next_bigram) <= 0)
      (heads[i].ptr)++;
  }
}

void output(float *vals, int nvals, struct lbigram *b)
{
  int i;
  for(i=0;i<nvals;i++)
    printf("%0.3f\t", vals[i]);
  printf("%d\t%ld\n", b->elts[0], b->elts[1]);
}

int main(int ac, char **av)
{
  if(ac == 1) {
    struct lbigram b;
    while(fread(&b, sizeof(b), 1, stdin) > 0) {
      printf("%0.3f\t%d\t%d\n", b.val, b.elts[0], b.elts[1]);
    }
  }

  else {
    int i; long n;

    int nheads = ac-1;

    float *vals = (float *)malloc(sizeof(float) * nheads);
    memset(vals, 0, sizeof(float) * nheads);

    struct head *heads = (struct head *)malloc((ac-1) * sizeof(struct head));
    memset(heads, 0, nheads * sizeof(struct head));
    for(i=1;i<ac;i++) {
      struct head *h = &heads[i-1];
      h->ptr = h->b = (struct lbigram *)mmapfile(av[i], &n);
      n /= sizeof(struct lbigram);
      h->end = h->b + n;
    }
    
    while(!done(heads, nheads)) {
      struct lbigram *nbigram = next_bigram(heads, nheads);
      fill_vals(vals, nbigram, heads, nheads);
      output(vals, nheads, nbigram);
      advance(heads, nheads, nbigram);
    }
  }
}
