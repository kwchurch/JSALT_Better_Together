#include <stdio.h>
#include "util.h"

void usage()
{
  fatal("usage, sum_bigrams N < bigrams");
}

double sum_bigrams(char *fn)
{
  FILE *fd;
  
  if(strcmp(fn, "-") == 0) fd = stdin;
  else fd = fopen(fn, "rb");
  if(!fd) fatal("open failed");
  double sum = 0;
  struct bigram b;
  while(fread(&b, sizeof(b), 1, fd) > 0)
    sum += b.val;
  if(strcmp(fn, "-") != 0) fclose(fd);
  printf("%f\t%s\n", sum, fn);
  fflush(stdout);
}  
  

int main(int ac, char **av)
{
  long errors = 0;
  int i;
  
  for(i=1;i<ac;i++)
    sum_bigrams(av[i]);
  return 0;
}



      
    
  