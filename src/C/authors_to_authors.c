#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <memory.h>

void usage()
{
  fatal("authors_to_authors: usage --papers_to_authors /work/k.church/JSALT-2023/semantic_scholar/releases/2023-06-20/database/papers/authors/papers_to_authors --max_authors 5 < bigrams");
}

int main(int ac, char **av)
{
  fprintf(stderr, "authors_to_authors, calling main\n");
  struct bigram b;
  struct lbigram B;
  char fn[1024];
  long nY=0, nXidx=0;
  long *Y, *Xidx;
  int i, j, max_authors = 5;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--papers_to_authors") == 0) {
      char *f = av[++i];
      sprintf(fn, "%s.Y.i", f);
      Y = (long *)mmapfile(fn, &nY);
      nY /= sizeof(long);
      fprintf(stderr, "authors_to_authors: nY = %ld\n", nY);

      sprintf(fn, "%s.X.i.idx", f);
      Xidx = (long *)mmapfile(fn, &nXidx);
      nXidx /= sizeof(long);
      fprintf(stderr, "authors_to_authors: nXidx = %ld\n", nXidx);
    }
    else if(strcmp(av[i], "--max_authors") == 0) max_authors = atoi(av[++i]);
    else usage();
  }

  long nA[2];
  long *A[2];
  A[0] = (long *)malloc(sizeof(long) * max_authors);
  A[1] = (long *)malloc(sizeof(long) * max_authors);
  if(!A[0] || !A[1]) fatal("malloc failed");

  B.val = 1.0;

  while(fread(&b, sizeof(b), 1, stdin) > 0) {
    for(i=0;i<2;i++) {
      int paper = b.elts[i];
      if(paper+1 >= nXidx) nA[i] = 0;
      else {
	if(paper == 0) {
	  A[i] = Y;
	  nA[i] = Xidx[0];
	}
	else {
	  A[i] = Y + Xidx[paper-1];
	  nA[i] = Xidx[paper] - Xidx[paper-1];
	}
	fprintf(stderr, "freq(CorpusId:%ld) = %ld\n", paper, nA[i]);
	if(nA[i] > max_authors) nA[i] = max_authors;
      }
    }

    // fprintf(stderr, "input papers: %d, %d; nA = %ld, %ld\n", b.elts[0], b.elts[1], nA[0], nA[1]);

    if(nA[0] <= 0 || nA[1] <= 0) continue;
    // B.val = 1/(double)(nA[0] * nA[1]);
    for(i=0;i<nA[0];i++) {
      for(j=0;j<nA[1];j++) {
	long ai = A[0][i];
	long aj = A[1][j];
	if(ai <= aj) {
	  B.elts[0] = ai;
	  B.elts[1] = aj;
	}
	else if(aj < ai) {
	  B.elts[0] = aj;
	  B.elts[1] = ai;
	}
	if(fwrite(&B, sizeof(struct lbigram), 1, stdout) != 1)
	  fatal("write failed");
      }
    }
  }
  return 0;
}
