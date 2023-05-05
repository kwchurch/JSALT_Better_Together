#include <stdio.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fprintf(stderr, "usage: substream N < foo > bar\n");
  exit(2);
}


int main(int ac, char **av)
{
  if(ac != 2) usage();
  int i, N = atoi(av[1]);
  for(i=0;i<N;i++) {
    int c = getchar();
    putchar(c);
  }
}

