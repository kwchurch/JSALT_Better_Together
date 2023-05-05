#include <stdio.h>
#include "util.h"

void usage()
{
  fatal("usage, check_bigrams bigrams");
}

#define BINS 300
long bins[BINS+2] = {0};

void print_bins()
{
  int i;
  printf("bins[neg] = %ld\n", bins[BINS+1]);
  for(i=0;i<BINS;i++)
    printf("bins[%d] = %ld\n", i, bins[i]);
  printf("bins[%d+] = %ld\n", BINS, bins[BINS]);
}

int main(int ac, char **av)
{
  long comps[3];
  double total_vals = 0;
  double min_vals, max_vals;
  long nbigrams;
  int min_elts[2];
  int max_elts[2];
  int i;

  if(ac != 2) usage();
  struct bigram *b = (struct bigram *)mmapfile(av[1], &nbigrams);
  nbigrams /= sizeof(struct bigram);
  if(nbigrams <= 0) fatal("mmapfile failed");

  struct bigram *bb = b;
  struct bigram *end = b + nbigrams;

  memset(min_elts,0,2*sizeof(int));
  memset(max_elts,0,2*sizeof(int));
  memset(comps,0,3*sizeof(long));

  min_vals = max_vals = bb->val;

  for( ; bb < end; bb++) {
    if(bb > b) comps[1+bigram_compare(bb-1, bb)]++;

    int bin = (int)bb->val;
    if(bin >= BINS) bin = BINS;
    if(bin < 0) bin = BINS + 1;
    bins[bin]++;

    total_vals += bb->val;
    int e0 = bb->elts[0];
    int e1 = bb->elts[1];

    if(e0 < min_elts[0]) min_elts[0] = e0;
    if(e1 < min_elts[1]) min_elts[1] = e1;

    if(e0 > max_elts[0]) max_elts[0] = e0;
    if(e1 > max_elts[1]) max_elts[1] = e1;
  }

  printf("check_bigrams: %s\n", av[1]);
  printf("%ld bigrams\n", nbigrams);
  printf("%f total_vals; %f mean vals; %f min -- %f max\n", total_vals, total_vals/nbigrams, min_vals, max_vals);
  printf("comparisons: %ld (expected order)\t%ld (duplicates)\t%ld (mismatches)\n", comps[0], comps[1], comps[2]);
  printf("%d - %d elt[0]\n", min_elts[0], max_elts[0]);
  printf("%d - %d elt[1]\n", min_elts[1], max_elts[1]);

  print_bins();

  exit(0);
}


      
    
  
