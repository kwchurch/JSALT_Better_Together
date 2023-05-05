#include <stdio.h>
#include "util.h"

// input filename
// output a bunch of files: <prefix>.<piece>
// if you cat the pieces together, you should recover the input file
// lengths of each piece should be a multiple of record_size

void usage()
{
  fatal("usage, split_binary_records -pieces int -record_size int -filename str -prefix str");
}

FILE *open_piece(char *prefix, int piece)
{
  char buf[1024];
  sprintf(buf, "%s.%03d", prefix, piece);
  FILE *res = fopen(buf, "wb");
  if(!res) fatal("open failed");
  return res;
}

int main(int ac, char **av)
{
  long errors = 0;
  struct bigram b;

  char *prefix=NULL;
  char *filename=NULL;
  int pieces = 0;
  int record_size = 0;
  int i;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "-prefix") == 0) prefix=av[++i];
    else if(strcmp(av[i], "-filename") == 0) filename=av[++i];
    else if(strcmp(av[i], "-pieces") == 0) pieces = atoi(av[++i]);
    else if(strcmp(av[i], "-record_size") == 0) record_size = atoi(av[++i]);
    else fatal("bad arg");
  }

  if(!prefix || !filename || !pieces || !record_size) usage();

  long N;
  void *obj = (void *)mmapfile(filename, &N);

  long records = N/record_size;
  if(records * record_size != N) fatal("confusion: expect file length to be a mutiple of record size");

  long records_per_piece = records/pieces;
  long records_for_last_piece = records - (pieces-1) * records_per_piece;

  int piece;
  for(piece=0;piece<pieces;piece++) {
    long r = records_per_piece;
    if(piece+1 == pieces) r = records_for_last_piece;
    FILE *fd = open_piece(prefix, piece);
    if(fwrite(obj + piece*records_per_piece*record_size, record_size, r, fd) != r) fatal("write failed");
    fclose(fd);
  }
}


      
    
  
