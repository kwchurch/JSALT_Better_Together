#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <search.h>

double lookup(struct lbigram *query, struct lbigram *bigrams, long N)
{
  struct lbigram *found = (struct lbigram *)bsearch(query, bigrams, N, sizeof(struct lbigram), lbigram_compare);
  if(!found) return 0;
  return found->val;
}

void usage()
{
  fatal("usage: lookup_bigram.c x y bigrams1 bigrams2 ... bigramsN");
}

void do_it(struct lbigram *query, struct lbigram **bigrams, long *N, int ac)
{
  int i;
  for(i=3;i<ac;i++)
    printf("%0.2f\t", lookup(query, bigrams[i], N[i]));
  printf("%ld\t%ld\n", query->elts[0], query->elts[1]);
}

int main(int ac, char **av)
{
  if(ac < 4) usage();
  int i;
  long *N = (long *)malloc(sizeof(long) * ac);
  struct lbigram query, **bigrams = (struct lbigram **)malloc(sizeof(struct lbigram *) * ac);

  for(i=3;i<ac;i++) {
    bigrams[i] = (struct lbigram *)mmapfile(av[i], N+i);
    N[i] /= sizeof(struct lbigram);
  }
    
  
  if(strcmp(av[1], "-") == 0)
    while(scanf("%ld%ld", query.elts, query.elts+1) == 2)
      do_it(&query, bigrams, N, ac);
  else {
    query.elts[0] = atoi(av[1]);
    query.elts[1] = atoi(av[2]);
    do_it(&query, bigrams, N, ac);
  }
}
