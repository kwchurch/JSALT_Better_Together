#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include "util.h"

void usage()
{
  fprintf(stderr, "usage: substream_records --piece 0-99 --npieces 100 --record_size nbytes --input foo > bar\n");
  exit(2);
}


int main(int ac, char **av)
{
  long i, piece=-1, npieces=-1, record_size = -1;
  long start=0, end=0;
  char *input_file = NULL;
  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--piece") == 0) piece = atol(av[++i]);
    else if(strcmp(av[i], "--npieces") == 0) npieces = atol(av[++i]);
    else if(strcmp(av[i], "--record_size") == 0) record_size = atol(av[++i]);
    else if(strcmp(av[i], "--input") == 0) input_file = av[++i];
    else {
      fprintf(stderr, "bad arg: %s\n",  av[i]);
      usage();
    }
  }

  if(piece < 0) fatal("--piece is required");
  if(npieces < 0) fatal("--npieces is required");
  if(record_size < 0) fatal("--record_size is required");
  if(input_file < 0) fatal("--input is required");

  FILE *fd = fopen(input_file, "rb");
  long N = fd_length(fd);

  long step = ((N /npieces)/record_size)*record_size;
  start = piece * step;
  end = (1+piece)*step;

  fprintf(stderr, "start = %ld, end = %ld\n", start, end);
  
  if(start >  0) {
    if(fseek(fd, start, SEEK_SET) != 0) {
      fprintf(stderr, "seek failed");
      exit(2);
    }
  }
    
  N = end - start;

  for(i=0;i<N;i++) {
    int c = getc(fd);
    putchar(c);
  }
}
