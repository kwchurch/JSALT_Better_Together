#include <stdio.h>
#include "util.h"
#include <memory.h>

void usage()
{
  fatal("usage: invert_permutation permutation > permutatation.inv");
}

long *idx;
long nidx;

int my_compare(long *a, long *b)
{
  long ia = idx[*a];
  long ib = idx[*b];
  if(ia < ib) return -1;
  if(ia > ib) return 1;
  return 0;
}

int main(int ac, char **av)
{
  long i;
  if(ac != 2) usage();

  idx = (long *)mmapfile(av[1], &nidx);
  nidx /= sizeof(long);

  long *result = (long *)malloc(sizeof(long) * nidx);
  if(!result) fatal("malloc failed");
  for(i=1;i<nidx;i++) 
    result[i] = i;

  qsort(result, nidx, sizeof(long), (__compar_fn_t)my_compare);

  if(fwrite(result, sizeof(long), nidx, stdout) != nidx)
    fatal("write failed");

  exit(0);
}

