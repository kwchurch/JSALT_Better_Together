#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "util.h"

void usage()
{
  fprintf(stderr, "usage: merge_transposed_ints <outfile> <infile1> <infile2>\n");
  fatal("usage");
}

int tick = 1000000;

FILE *outX = NULL;
FILE *outY = NULL;

struct pair {
  int *X, *Y;
  long n, head;
};

char *fileX(char *fn)
{
  char buf[1024];
  if(strlen(fn) > 1000) fatal("assert: fn is too long");
  sprintf(buf, "%s.X.i", fn);
  return strdup(buf);
}

char *fileY(char *fn)
{
  char buf[1024];
  if(strlen(fn) > 1000) fatal("assert: fn is too long");
  sprintf(buf, "%s.Y.i", fn);
  return strdup(buf);
}


struct pair *load_pairs(char *fn)
{
  struct pair *res = (struct pair *)malloc(sizeof(struct pair));
  long nX, nY;

  res->head = 0;
  res->X = (int *)mmapfile(fileX(fn), &nX);
  if(res->X == NULL) fatal("load_pairs: assertion failed, res->X is NULL");
  nX /= sizeof(int);

  res->Y = (int *)mmapfile(fileY(fn), &nY);
  if(res->Y == NULL) fatal("load_pairs: assertion failed, res->Y is NULL");
  nY /= sizeof(int);

  if(nX != nY) fatal("assertion failed: nX != nY");

  fprintf(stderr, "load_pairs: found %ld pairs in %s\n", nX, fn);

  res->n = nX;
  return res;
}

int pair_compare(struct pair *a, struct pair *b)
{
  if(a->head >= a->n) return 1;
  if(b->head >= b->n) return -1;

  if(a->X[a->head] < b->X[b->head]) return -1;
  if(a->X[a->head] > b->X[b->head]) return 1;

  if(a->Y[a->head] < b->Y[b->head]) return -1;
  if(a->Y[a->head] > b->Y[b->head]) return 1;

  return 0;
}

void my_output(struct pair *p)
{
  if(fwrite(&p->X[p->head], sizeof(int), 1, outX) != 1) fatal("write failed");
  if(fwrite(&p->Y[p->head], sizeof(int), 1, outY) != 1) fatal("write failed");
  (p->head)++;
}

int main(int ac, char **av)
{
  long stats[3];
  int N = 0;
  if (ac != 4) usage();

  memset(stats, 0, sizeof(stats));
  
  outX = fopen(fileX(av[1]), "wb");
  outY = fopen(fileY(av[1]), "wb");
  if(!outX || !outY) fatal("open failed");

  struct pair *f1 = load_pairs(av[2]);
  struct pair *f2 = load_pairs(av[3]);

  while(f1->head < f1->n || f2->head < f2->n) {

    if(f1->head % tick == 0)
      fprintf(stderr, "f1->head = %ld (%0.2f%% done); stats = %ld, %ld, %ld\n", 
	      f1->head, 100*f1->head/(float)f1->n,
	      stats[0], stats[1], stats[2]);

    int comp = pair_compare(f1, f2);
    stats[comp+1]++;

    if(comp == 0) {
      my_output(f1);
      (f2->head)++;
    }
    else if(comp < 0) my_output(f1);
    else my_output(f2);
  }

  for(int i=0;i<3;i++)
    fprintf(stderr, "stats[%d] = %ld\n", i, stats[i]);

  return 0;
}

