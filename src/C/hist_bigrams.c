#include <stdio.h>
#include "util.h"

void usage()
{
  fatal("usage, hist_bigrams axis N < bigrams (axis is 0 or 1; -1 --> sum all bigrams)");
}

int main(int ac, char **av)
{
  long errors = 0;
  struct bigram b;

  if(ac < 2) usage();

  int axis = atoi(av[1]);

  if(axis < 0) {
    fprintf(stderr, "axis < 0 --> sum all bigrams\n");
    double result = 0;
    while(fread(&b, sizeof(b), 1, stdin) > 0)
         result += b.val;
    fprintf(stdout, "sum_all_bigrams:\t%f\n", result);
    exit(2);
  }
    
  if(ac != 3) usage();

  int N = atoi(av[2]);

  fprintf(stderr, "axis = %d, N = %d\n", axis, N);

  float *hist = (float *)malloc(sizeof(float) * N);
  if(!hist) fatal("malloc failed");

  if(!(axis == 0 || axis == 1)) fatal("axis should be 0 or 1");

  memset(hist, 0, sizeof(int) * N);

  while(fread(&b, sizeof(b), 1, stdin) > 0) {
    int x = b.elts[axis];
    if(x < 0 || x >= N) errors++;
    else hist[x] += b.val;
  }

  if(fwrite(hist, sizeof(float), N, stdout) != N)
    fatal("write failed");

  fprintf(stderr, "%ld errors\n", errors);
}


      
    
  
