#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <stdlib.h>
#include <search.h>

void usage()
{
  fatal("sort_bigrams bigrams > bigrams.sorted OR sort_bigrams -m bigrams1 bigrams2 ... > bigrams.sorted");
}

struct head {
  FILE *fd;
  struct bigram bigram;
  int eof;
};

int head_compare(struct head *a, struct head *b)
{
  if(a->eof && b->eof) return 0;
  if(a->eof) return 1;
  if(b->eof) return -1;
  return bigram_compare(&(a->bigram), &(b->bigram));
}

void advance(struct head *h)
{
  for(;;) {
    if(fread(&(h->bigram), sizeof(struct bigram), 1, h->fd) != 1) {
      h->eof=1;
      return;
    }
    if(h->bigram.val != 0)
      return;
  }
}

struct head *next_head(struct head *heads, int nheads)
{
  int i, best=0;
  for(i=1;i<nheads;i++) {
    if(head_compare(heads+i, heads+best) < 0)
      best=i;
  }
  return heads+best;  
}

void init_head(struct head *h, char *filename)
{
  fprintf(stderr, "init_head: %s\n", filename);
  memset(h, 0, sizeof(struct head));
  h->fd = fopen(filename, "rb");
  if(h->fd == NULL) fatal("open failed");
  advance(h);
}

void merge_sort(int ac, char **av)
{
  fprintf(stderr, "merge_sort: ac = %d\n", ac);

  int i, nheads = ac-2;
  struct head *heads = (struct head *)malloc(sizeof(struct head) * nheads);
  for(i=0;i<nheads;i++)
    init_head(heads+i, av[i+2]);
  for(;;) {
    struct head *h = next_head(heads, nheads);
    if(h->eof) return;
    if(fwrite(&(h->bigram), sizeof(struct bigram), 1, stdout) != 1)
      fatal("write failed");
    advance(h);
  }
}

int main(int ac, char **av)
{
  fprintf(stderr, "main: ac = %d\n", ac);

  if((ac > 2) && (strcmp(av[1], "-m") == 0)) {
    merge_sort(ac, av);
    exit(0);
  }

  // simple in-memory sort

  if(ac != 2) usage();
  long N;
  struct bigrams *b = (struct bigrams *)readchars(av[1], &N);

  N /= sizeof(struct bigram);
  fprintf(stderr, "found %ld bigrams in %s\n", N, av[1]);

  qsort(b, N, sizeof(struct bigram), bigram_compare);
  // qsort(b, N, sizeof(struct bigram), (__compar_fn_t)bigram_compare);
  
  if(fwrite(b, sizeof(struct bigram), N, stdout) != N)
    fatal("write failed");

  exit(0);
 }



      
    
  
