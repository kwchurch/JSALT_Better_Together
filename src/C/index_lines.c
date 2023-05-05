#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fatal("usage: index_lines map file");
}

int main(int ac, char **av)
{
  char buf[1024];
  if(ac != 2) usage();
  int i;
  long nfile;
  char *file = (char *)mmapfile(av[1], &nfile);
  nfile /= sizeof(int);

  sprintf(buf, "%s.line_index.i", av[1]);
  FILE *fd = fopen(buf, "wb");
  if(!fd) fatal("open failed");

  putw(0, fd);
  for(i=1;i<nfile;i++)
    if(file[i-1] == '\n') putw(i, fd);
  putw(nfile, fd);
}


