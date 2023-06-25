#include <stdio.h>
#include <strings.h>
#include "util.h"

void old_do_file(char *Xfn)
{
  fprintf(stderr, "do_file: %s\n", Xfn);

  struct bigram b;
  char Yfn[1024];
  long nX, nY, i;
  int *X = (int *)mmapfile(Xfn, &nX);
  nX /= sizeof(int);

  fprintf(stderr, "nX = %ld\n", nX);

  strcpy(Yfn, Xfn);
  Yfn[strlen(Yfn)-1] = 'Y';
  int *Y = (int *)mmapfile(Yfn, &nY);
  nY /= sizeof(int);

  fprintf(stderr, "nY = %ld\n", nY);

  if(nX != nY) fatal("confusion in do_file");

  b.val = 1.0;

  for(i=0;i<nX;i++) {
    b.elts[0] = X[i];
    b.elts[1] = Y[i];
    if(fwrite(&b, sizeof(b), 1, stdout) != 1)
      fatal("write failed");
  }
}

void do_file(char *Xfn)
{
  int x, y;
  fprintf(stderr, "do_file: %s\n", Xfn);

  struct bigram b;
  char Yfn[1024];
  FILE *Xfd = fopen(Xfn, "rb");
  if(!Xfd) fatal("open failed");
  strcpy(Yfn, Xfn);
  Yfn[strlen(Yfn)-1] = 'Y';

  FILE *Yfd = fopen(Yfn, "rb");
  if(!Yfd) fatal("open failed");
  b.val = 1.0;

  while(fread(&x, sizeof(int), 1, Xfd) == 1 &&
	fread(&y, sizeof(int), 1, Yfd) == 1) {
    b.elts[0] = x;
    b.elts[1] = y;
    if(fwrite(&b, sizeof(b), 1, stdout) != 1)
      fatal("write failed");
  }
  if(fclose(Xfd) != EOF) fatal("close failed");
  if(fclose(Yfd) != EOF) fatal("close failed");
}

int main(int ac, char **av)
{
  fprintf(stderr, "ac = %d\n", ac);
  int i;
  for(i=1;i<ac;i++)
    do_file(av[i]);
}
