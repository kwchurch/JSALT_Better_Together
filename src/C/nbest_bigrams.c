#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <stdlib.h>
#include <search.h>

void usage()
{
  fatal("nbest_bigrams N bigrams > bigrams.nbest");
}

int bigram_freq_compare(struct bigram *a, struct bigram *b)
{
  if(a->val < b->val) return 1;
  if(a->val > b->val) return -1;
  return 0;
}

int freq(struct bigram *b, struct bigram *bend)
{
  struct bigram *bstart = b;
  if(b >= bend) return 0;
  for( ; b < bend; b++) {
    if(b+1 >= bend || b[0].elts[0] != b[1].elts[0])
      break;
  }
  return b - bstart + 1;
}  

int main(int ac, char **av)
{
  long N;
  int nbest = atoi(av[1]);
  fprintf(stderr, "nbest_bigrams: nbest = %d\n", nbest);

  struct bigram *bigrams = (struct bigram *)mmapfile(av[2], &N);
  N /= sizeof(struct bigram);
  fprintf(stderr, "found %ld bigrams in %s\n", N, av[2]);

  struct bigram *b = bigrams;
  struct bigram *bend = b + N;
  int f;

  int bcopy_len = 10000;
  struct bigram *bcopy = (struct bigram *)malloc(sizeof(struct bigram) * bcopy_len);
  if(!bcopy) fatal("malloc failed");

  for(; b < bend; b += f) {
    f = freq(b, bend);
    // fprintf(stderr, "f = %d\n", f);
    if(f > bcopy_len) {
      free(bcopy);
      bcopy_len = f;
      fprintf(stderr, "growing bcopy to %d\n", bcopy_len);
      struct bigram *bcopy = (struct bigram *)malloc(sizeof(struct bigram) * bcopy_len);
      if(!bcopy) fatal("malloc failed");
    }
    memcpy(bcopy, b, sizeof(struct bigram) * f);
    qsort(bcopy, f, sizeof(struct bigram), bigram_freq_compare);
    int nout = nbest;
    if(nout > f) nout=f;
    if(fwrite(bcopy, sizeof(struct bigram), nout, stdout) != nout)
      fatal("write failed");
  }

  exit(0);
 }



      
    
  
