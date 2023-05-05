#include <stdio.h>
#include <strings.h>
#include "util.h"

int row_length(struct bigram *b, struct bigram *end)
{
  struct bigram *p = b+1;
  while(p<end && p->elts[0] == b->elts[0]) p++;
  return p-b;
}

void cross(struct bigram *b, struct bigram *end)
{
  struct bigram *i, *j, out;
  out.val = 1.0;
  for(i=b;i<end;i++) {
    out.elts[0] = i->elts[1];
    for(j=b; j<end; j++) {
      out.elts[1] = j->elts[1];
      if(fwrite(&out, sizeof(out), 1, stdout) != 1)
	fatal("write failed");
    }
  }
}

int main(int ac, char **av)
{
  long N;
  struct bigram *b = (struct bigram *)mmapfile(av[1], &N);
  N /= sizeof(struct bigram);
  long steps = N/1000;
  fprintf(stderr, "found %ld bigram in %s\n", N, av[1]);
  struct bigram *end = b+N;
  struct bigram *milestone = b+steps;
  struct bigram *start = b;

  while(b<end) {
    int rlen = row_length(b, end);
    cross(b, b+rlen);
    b += rlen;
    if(b >= milestone) {
      fprintf(stderr, "milestone: %ld\n", (milestone-start)/steps);
      fflush(stderr);
      milestone += steps;
    }
  }
}



      
    
  
