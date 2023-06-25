#include <stdio.h>
#include <strings.h>
#include "util.h"

void usage()
{
  fatal("usage: XY_data_to_bigrams X Y data > bigrams");
}

int main(int ac, char **av)
{
  fprintf(stderr, "ac = %d\n", ac);
  long nX, nY, nData;
  int *X = (int *)mmapfile(av[1], &nX);
  int *Y = (int *)mmapfile(av[2], &nY);
  float *Data = (float *)mmapfile(av[3], &nData);
  nX /= sizeof(int);
  nY /= sizeof(int);
  nData /= sizeof(float);

  if(ac != 4) usage();
  if(nX != nY || nX != nData) fatal("confusion");
  int *Xend = X + nX;
  struct bigram b;
  
  for( ; X < Xend; X++,Y++,Data++) {
    b.val = *Data;
    b.elts[0] = *X;
    b.elts[1] = *Y;
    if(fwrite(&b, sizeof(b), 1, stdout) != 1)
      fatal("write failed");
  }
}
