#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fatal("usage: aref map < keys > report");
}

int main(int ac, char **av)
{
  if(ac != 2) usage();
  int i;
  long nmap;
  int *map = (int *)mmapfile(av[1], &nmap);
  nmap /= sizeof(int);
  
  while(scanf("%d", &i) == 1) {
    if(i < 0 || i>= nmap) printf("***ERROR***\t%d\n", i);
    else printf("%d\n", map[i]);
  }
}

