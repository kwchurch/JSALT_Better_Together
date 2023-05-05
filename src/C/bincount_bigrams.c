#include <stdio.h>
#include "util.h"

void usage()
{
  fatal("usage, bincount_bigrams N < bigrams");
}

int main(int ac, char **av)
{
  long errors = 0;
  struct bigram b;

  if(ac != 2) usage();
  int N = atoi(av[1]);

  fprintf(stderr, "N = %d\n", N);
  int *result = (int *)malloc(sizeof(int) * (N+1));
  memset(result, 0, sizeof(int) * (N+1));
  while(fread(&b, sizeof(b), 1, stdin) > 0) {
    int r = (int)(b.val);
    if(r > N) r = N;
    result[r]++;
  }
    
  if(fwrite(result, sizeof(int), N+1, stdout) != (N+1))
    fatal("write failed");
}


      
    
  
