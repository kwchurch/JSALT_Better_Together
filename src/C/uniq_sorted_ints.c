#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "util.h"

void usage()
{
  fprintf(stderr, "usage: uniq_sorted_ints <files>\n");
  fatal("usage");
}

struct env{
  int n;
  int **heads;
  int **tails;
  int next;
  int freq;
} the_env;

int done(struct env *e)
{
  int i;
  for(i=0;i<e->n;i++)
    if(e->heads[i] >= e->tails[i])
      return 0;
  return 1;
}

void advance(struct env *e)
{
  int i;

  for(i=0;i<e->n;i++) {
    if(e->heads[i] >= e->tails[i]) continue;
    if((e->heads[i])[0] == e->next)
      e->heads[i] = e->heads[i] + 1;
  }
  e->next = e->freq = -1;
}

void get_next(struct env *e)
{
  int i;
  int best=2147483647;
  int freq=0;

  for(i=0;i<e->n;i++) {
    if(e->heads[i] >= e->tails[i]) continue;
    if((e->heads[i])[0] < best)
      best=(e->heads[i])[0];
  }

  for(i=0;i<e->n;i++) {
    if(e->heads[i] >= e->tails[i]) continue;
    if((e->heads[i])[0] == best) freq++;
  }

  if(best < 0 || freq <= 0) fatal("confusion");

  e->next= best;
  e->freq = freq;
  
}

int int_compare(int *a, int *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

int main(int ac, char **av)
{
  int N = 0;
  int i,n = ac-1;
  long *nints = (long *)malloc(sizeof(long) * n);
  int **ints = (int **)malloc(sizeof(int *) * n);

  the_env.heads = (int **)malloc(sizeof(int *) * n);
  the_env.tails = (int **)malloc(sizeof(int *) * n);
  the_env.n = n;
  the_env.next = -1;

  for(i=0;i<n;i++) {
    ints[i] = (int *)mmapfile(av[i+1], &nints[i]);
    nints[i] /= sizeof(int *);
    N += nints[i];
  }

  fprintf(stderr, "N = %d\n", N);

  int *res = (int *)malloc(sizeof(int) * N);
  int *bres = res;
  for(i=0;i<n;i++) {
    memcpy(bres, ints[i], nints[i] * sizeof(int));
    bres += nints[i];
  }

  qsort(res, N, sizeof(int), (int (*)(const void *, const void *))int_compare);

  int freq=0;
  int prev=-1;
  for(i=0;i<N;i++) {
    if(res[i] == prev) freq++;
    else {
      if(prev >= 0 && freq > n/2) printf("%d\t%d\n", freq, prev);
      prev = res[i];
      freq = 1;
    }
  }
  if(freq > n/2) printf("%d\t%d\n", freq, prev);
  return 0;
}

int old_main(int ac, char **av)
{
  int i,n = ac-1;
  long *nints = (long *)malloc(sizeof(long) * n);
  int **ints = (int **)malloc(sizeof(int *) * n);

  the_env.heads = (int **)malloc(sizeof(int *) * n);
  the_env.tails = (int **)malloc(sizeof(int *) * n);
  the_env.n = n;
  the_env.next = -1;

  for(i=0;i<n;i++) {
    ints[i] = (int *)mmapfile(av[i+1], &nints[i]);
    nints[i] /= sizeof(int *);
    the_env.heads[i] = ints[i];
    the_env.tails[i] = ints[i] + nints[i];

    // printf("%ld: %s\n", nints[i], av[i+1]);
  }

  int prev = -1;
  while(!done(&the_env)) {
    get_next(&the_env);
    if(the_env.freq >= n/2) printf("%d\t%d\n", the_env.freq, the_env.next);
    if(the_env.next <= prev) fatal("assertion failed");
    prev = the_env.next;
    advance(&the_env);
  }  

  return 0;
}
