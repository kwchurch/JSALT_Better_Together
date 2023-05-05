#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include "util.h"

double lookup(struct bigram *query, char *fn)
{
  long N;
  struct bigram *b = (struct bigram *)mmapfile(fn, &N);
  N /= sizeof(struct bigram);
  struct bigram *found = (struct bigram *)bsearch(query, b, N, sizeof(struct bigram), (__compar_fn_t)bigram_compare);
  if(!found) return 0;
  return found->val;
}

void usage()
{
  fatal("usage: lookup_bigram.c x y bigrams1 bigrams2 ... bigramsN");
}

int main(int ac, char **av)
{
  if(ac < 4) usage();
  int i;
  long N, n_index;
  struct bigram query;
  query.val = 0;
  query.elts[0] = atoi(av[1]);
  query.elts[1] = atoi(av[2]);

  for(i=3;i<ac;i++) {
    double f = lookup(&query, av[i]);
    printf("%f\t%d\t%d\t%s\n", f, query.elts[0], query.elts[1], av[i]);
  }
}
