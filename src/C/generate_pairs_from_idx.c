#include <stdio.h>
#include <memory.h>
#include <stdlib.h>
#include <math.h>
#include "util.h"

int verbose = 0;
int debug = 0;

void usage()
{
  fatal("usage: generate_pairs_from_idx --offset <n>  --debug idx.*.i");
}

void debug_do_it(char *fn, int offset)
{
  long buf[2];
  if(offset <= 0) usage();
  long *j, N;
  long *idx = (long *)mmapfile(fn, &N);
  N /= sizeof(long);
  long *end = idx + N;
  idx = idx + offset;

  printf("debug_do_it: fn = %s (contains %ld longs), offset = %d\n", fn, N, offset);


  for( ; idx<end; idx++) {
    buf[1] = idx[0];
    printf("idx[0] = buf[1] = %ld\n", idx[0]);
    for(j = idx-offset; j<idx; j++) {
      buf[0] = j[0];
      printf("%ld\t%ld\t(gap = %ld)\n", buf[0], buf[1], idx-j);
    }
  }
}

void do_it(char *fn, int offset)
{
  if(debug) return debug_do_it(fn, offset);

  fprintf(stderr, "working on: %s\n", fn);

  // printf("fn = %s\n", fn);
  // return;
  long buf[2];
  if(offset <= 0) usage();
  long *j, N;
  long *idx = (long *)mmapfile(fn, &N);
  N /= sizeof(long);
  long *end = idx + N;
  idx = idx + offset;

  for( ; idx<end; idx++) {
    buf[1] = idx[0];
    for(j = idx-offset; j<idx; j++) {
      buf[0] = j[0];
      if(buf[0] == buf[1]) continue;
      else if(buf[0] < buf[1]) {
	if(fwrite(buf, sizeof(long), 2, stdout) != 2)
	  fatal("write failed");
      }
      else {
	if((fwrite(buf+1, sizeof(long), 1, stdout) != 1) || (fwrite(buf+0, sizeof(long), 1, stdout) != 1))
	  fatal("write failed");
      }
    }
  }
}


int main(int ac, char **av)
{
  // fprintf(stderr, "generate_pairs_from_idx: av[0] = %s\n", av[0]);
  int offset = -1;
  int i;
  for(i=0;i<ac;i++) 
    fprintf(stderr, "generate_pairs_from_idx: av[%d] = %s\n", i, av[i]);

  for(i=1;i<ac;i++) {
    // fprintf(stderr, "generate_pairs_from_idx: av[%d] = %s\n", i, av[i]);
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--offset") == 0) offset=atoi(av[++i]);
    else if(strcmp(av[i], "--debug") == 0) debug=1;
    else do_it(av[i], offset);
  }
  return 0;
}
