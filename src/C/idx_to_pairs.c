#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>

int verbose = 0;
int show_details = 0;
int find_best = 1;
int threshold = 0;

void usage()
{
  fatal("usage: idx_to_pairs [--offset <n>] [--idx idx]");
}

int main(int ac, char **av)
{
  long i, j;

  int offset = -1;
  long *idx = NULL;
  long nidx = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--offset") == 0) offset = atoi(av[++i]);
    else if(strcmp(av[i], "--idx") == 0) {
      idx = (long *)mmapfile(av[++i], &nidx);
      nidx /= sizeof(long);
    }
    else usage();
  }

  fprintf(stderr, "offset = %d, nidx = %ld\n", offset, nidx);

  if(nidx <= 0) fatal("--idx arg is required");
  if(offset <= 0) fatal("--offset arg is required");

  for(i=offset;i<nidx;i++) {
    long a = idx[i];
    for(j=i-offset;j<i;j++) {
      long b = idx[j];
      if(a == b) continue;
      if(a < b) printf("%09ld\t%09ld\n", a, b);
      else printf("%09ld\t%09ld\n", b, a);
    }
  }
}
