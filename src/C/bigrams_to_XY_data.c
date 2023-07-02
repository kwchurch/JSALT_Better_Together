#include <stdio.h>
#include <strings.h>
#include "util.h"

void usage()
{
  fatal("usage: bigrams_to_XY_data threshold X Y < bigrams");
}

int main(int ac, char **av)
{
  fprintf(stderr, "ac = %d\n", ac);
  float T = atof(av[1]);
  FILE *Xfd = fopen(av[2], "wb");
  FILE *Yfd = fopen(av[3], "wb");
  struct bigram b;

  while(fread(&b, sizeof(b), 1, stdin) == 1) {
    if(b.val >= T) {
      int x = b.elts[0];
      int y = b.elts[1];
      if(fwrite(&x, sizeof(int), 1, Xfd) != 1) fatal("write failed");
      if(fwrite(&y, sizeof(int), 1, Yfd) != 1) fatal("write failed");
    }
  }
  return 0;
}
