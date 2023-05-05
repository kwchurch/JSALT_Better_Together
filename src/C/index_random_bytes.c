#include <stdio.h>
#include "util.h"
#include <memory.h>

void usage()
{
  fprintf(stderr, "usage: index_random_bytes random_bytes random_permutation > index\n");
  fprintf(stderr, "or\n");
  fprintf(stderr, "usage: index_random_bytes random_bytes N --simple_case > index\n");
  fprintf(stderr, "The simple case if replaces the permutation with identity (N is record size)\n");
  fatal("usage");
}

void *random_bytes;
long nrandom_bytes;
long N;

long *random_permutation;

int permuted_memcmp(char *a, char *b)
{
  long *p = random_permutation;
  long *pend = p+N;
  for( ; p<pend; p++) {
    int comp = memcmp(a + *p, b + *p, 1);
    if(comp != 0) return comp;
  }
  return 0;
}

int index_compare(long *a, long *b)
{
  return permuted_memcmp(random_bytes + *a * N, random_bytes + *b * N);
}

int mem_compare(long *a, long *b)
{
  char *aa = random_bytes + *a * N;
  char *bb = random_bytes + *b * N;
  return memcmp(aa, bb, N);
}

void simple_case(int ac, char **av)
{
  long i;
  fprintf(stderr, "Simple case (no permutation)\n");
  N = atoi(av[2]);
  
  random_bytes = (void *)mmapfile(av[1], &nrandom_bytes);
  nrandom_bytes /= N;

  fprintf(stderr, "N = %d, nrandom_bytes=%ld\n", N, nrandom_bytes);

  long *idx = (long *)malloc(sizeof(long) * nrandom_bytes);

  if(!idx) fatal("malloc failed");

  for(i=0;i<=nrandom_bytes;i++)
    idx[i] = i;

  fprintf(stderr, "calling qsort\n");

  qsort(idx, nrandom_bytes, sizeof(long), (__compar_fn_t)mem_compare);

  fprintf(stderr, "finished qsort\n");

  if(fwrite(idx, sizeof(long), nrandom_bytes, stdout)  != nrandom_bytes)
    fatal("write failed");

  exit(0);
}

int main(int ac, char **av)
{
  long i;
  
  for(i=1;i<=ac;i++)
    if(strcmp(av[i], "--simple_case") == 0)
      simple_case(ac, av);

  if(ac != 3) usage();


  random_permutation = (long *)mmapfile(av[2], &N);
  N /= sizeof(long);

  random_bytes = (void *)mmapfile(av[1], &nrandom_bytes);
  nrandom_bytes /= N;

  fprintf(stderr, "N = %d, nrandom_bytes=%ld\n", N, nrandom_bytes);
  for(i=0;i<N;i++)
    fprintf(stderr, "random_permutation[%d] = %ld\n", i, random_permutation[i]);

  long *idx = (long *)malloc(sizeof(long) * nrandom_bytes);

  if(!idx) fatal("malloc failed");

  for(i=0;i<=nrandom_bytes;i++)
    idx[i] = i;

  fprintf(stderr, "calling qsort\n");

  qsort(idx, nrandom_bytes, sizeof(long), (__compar_fn_t)index_compare);

  fprintf(stderr, "finished qsort\n");

  if(fwrite(idx, sizeof(long), nrandom_bytes, stdout)  != nrandom_bytes)
    fatal("write failed");

  exit(0);
}


      
    
  
