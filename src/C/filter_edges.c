#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fatal("usage: filter_edges good Xin Yin Xout Yout");
}

int *byte_ify(int *good, long ngood)
{
  int i = 0;
  int *gend = good + ngood;
  int *g = good;
  long n = 1+good[ngood-1];
  // fprintf(stderr, "n = %ld\n", n);
  int *result = (int *)malloc(n * sizeof(int));
  memset(result, -1, n * sizeof(int));
  while(g < gend)
    result[*g++] = i++;
  return result;
}

int main(int ac, char **av)
{
  if(ac != 6) usage();
  long i;
  long nXin, nYin, ngood;
  int *good = (int *)mmapfile(av[1], &ngood);
  int *Xin = (int *)mmapfile(av[2], &nXin);
  int *Yin = (int *)mmapfile(av[3], &nYin);
  FILE *Xout = fopen(av[4], "wb");
  FILE *Yout = fopen(av[5], "wb");

  if(!Xout || !Yout) fatal("open failed");

  // fprintf(stderr, "pt1\n");

  ngood /= sizeof(int);
  nXin /= sizeof(int);
  nYin /= sizeof(int);
  
  // fprintf(stderr, "ngood = %ld, nXin = %ld, nYin = %ld\n", ngood, nXin, nYin);

  if(nXin != nYin) fatal("confusion");


  long last = good[ngood-1];

  int *bgood = byte_ify(good, ngood);

  // fprintf(stderr, "pt2\n");
  
  for(i = 0;i<nXin; i++) {
    int x = Xin[i];
    int y = Yin[i];
    if(x <= last && y <= last && bgood[x] >= 0 && bgood[y] >= 0) {
      if(fwrite(&bgood[x], sizeof(int), 1, Xout) != 1) fatal("write failed");
      if(fwrite(&bgood[y], sizeof(int), 1, Yout) != 1) fatal("write failed");
    }
  }
}

