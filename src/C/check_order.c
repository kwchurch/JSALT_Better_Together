#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <strings.h>
#include "util.h"

int check_order(int *X, int *Xend)
{
  X++;
  for( ; X < Xend; X++)
    if(X[-1] > X[0]) return EOF;
  return 0;
}

int freq(int *X, int *Xend)
{
  int *base = X;
  
  for( ; X < Xend; X++)
    if(*X != *base)
      break;
  
  int res = X-base;
  // fprintf(stderr, "freq returning %d\n", res);
  return res;
}


void usage()
{
  fprintf(stderr, "usage: check_order input.X input.Y\n");
  fatal("usage");
}

int main(int ac, char **av)
{
  if(ac != 3) usage();

  long int nX, nY;
  int *X = (int *)mmapfile(av[1], &nX);
  int *Y = (int *)mmapfile(av[2], &nY);
  nX /= sizeof(int);
  nY /= sizeof(int);
  int *Xend = X + nX;
  int *Yend = Y + nY;

  fprintf(stderr, "nX = %ld; nY = %ld\n", nX, nY);
  if(nX != nY) fatal("expected nX == nY");

  if(X == NULL || Y == NULL) fatal("mmap failed");

  if(check_order(X, Xend) == EOF)
    fprintf(stderr, "check_order failed: %s\n", av[1]);
  else fprintf(stderr, "check_order succeeded: %s\n", av[1]);

  int freqp, p;

  // This invariant does not hold
  // Not clear what the order should be for these indexes
  for(p=0 ; p<nX; p+=freqp) {
    freqp = freq(X+p, Xend);
    if(check_order(Y+p, Y+p + freqp) == EOF) {
      fprintf(stderr, "check_order failed: %s, X[%d] = %d\n", av[1], p, X[p]);
      fatal("failure");
    }
  }

  fprintf(stderr, "check_order succeeded: %s\n", av[2]);
}
