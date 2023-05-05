#include <stdio.h>
#include <stdlib.h>
#include "util.h"


int main(int ac, char **av)
{
  int i;
  int ninputs = ac-2;
  FILE **fd = malloc(ninputs*sizeof(FILE *));
  int N = atoi(av[1]);

  char *buf = malloc(N);
  if(!buf) fatal("malloc failed");

  for(i=0;i<ninputs;i++)
    fd[i] = my_fopen(av[i+2], "rb");

  for(i=0;;i++) {
    if(i>= ninputs)i=0;
    if(fread(buf, 1, N, fd[i]) != N) break;
    if(fwrite(buf, 1, N, stdout) != N) fatal("write failed");
  }

  exit(0);
}
