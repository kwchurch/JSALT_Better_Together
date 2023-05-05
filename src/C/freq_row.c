#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <strings.h>
#include "util.h"

void check_order(int *X, int *Xend)
{
  X++;
  for( ; X < Xend; X++)
    if(X[-1] > X[0])
      fatal("check_order failed");
}

int freq(int *X, int *Xend)
{
  int *base = X;
  
  for( ; X < Xend; X++)
    if(*X != *base)
      break;
  
  int res = X-base;
  // fprintf(stderr, "freq returning %d\n", res);
  return res;
}


void usage()
{
  fprintf(stderr, "usage: freq_row input output npieces T\n");
  fprintf(stderr, "\tinput and output are pairs of files with suffixes .X and .Y\n");
  fprintf(stderr, "\tnpieces is a number such as 1000\n");
  fprintf(stderr, "\tT is a threshold on freq for sketching, typically 100\n");
  fatal("usage");
}


void my_output(FILE **outf, int *X, int *Y, int n)
{
  // fprintf(stderr, "my_output: n = %d\n", n);
  if(fwrite(X, sizeof(int), n, outf[0]) != n) fatal("write failed");
  // fprintf(stderr, "my_output: midpoint\n");
  if(fwrite(Y, sizeof(int), n, outf[1]) != n) fatal("write failed");
  // fprintf(stderr, "my_output: finished\n");
}

int main(int ac, char **av)
{
  char filenames[6][256];

  if(ac != 5) usage();

  char *Xfilename = filename(filenames[0], av[1], "X");
  char *Yfilename = filename(filenames[1], av[1], "Y");

  FILE *small_outf[2];
  FILE *big_outf[2];
  big_outf[0] = big_outf[1] = NULL;

  small_outf[0]= fopen(filename(filenames[2], av[2], "small.X"), "wb");
  small_outf[1]= fopen(filename(filenames[3], av[2], "small.Y"), "wb");

  long int nX, nY;
  int *X = (int *)mmapfile(Xfilename, &nX);
  int *Y = (int *)mmapfile(Yfilename, &nY);
  nX /= sizeof(int);
  nY /= sizeof(int);
  int *Xend = X + nX;
  int *Yend = Y + nY;

  fprintf(stderr, "nX = %ld; nY = %ld\n", nX, nY);
  if(nX != nY) fatal("expected nX == nY");

  if(X == NULL || Y == NULL) fatal("mmap failed");

  check_order(X, Xend);
  fprintf(stderr, "check_order succeeded\n");

  int T = atoi(av[4]);
  int N = X[nX-1] + 1;
  int Nbig = 0;
  int freqp, p, piece_ptr;

  for(p=0 ; p<nX; p+=freqp) {
    freqp = freq(X+p, Xend);
    // This invariant does not hold
    // check_order(Y+p, freqp);
    if(freqp > T) Nbig++;
  }

  int npieces = atoi(av[3]);
  int piece_length = (Nbig+npieces-1)/npieces;
  int piece = 0;

  fprintf(stderr, "Nbig = %d, npieces = %d, piece_length = %d, T = %d\n",
	  Nbig, npieces, piece_length, T);

  for(p=0 ; p<nX; p+=freqp) {
    freqp = freq(X+p, Xend);
    // fprintf(stderr, "main: freqp = %d (point 1)\n", freqp);
    FILE **outf = small_outf;
    if(freqp > T) {
      //fprintf(stderr, "main: freqp = %d (point 1a)\n", freqp);
      if(big_outf[0] == NULL || piece_ptr >= piece_length) {
	if(big_outf[0] != NULL) {
	  fprintf(stderr, "closing big_outf: piece = %d (of %d)\n", piece, npieces);
	  if(fclose(big_outf[0]) == EOF) fatal("close failed");
	  if(fclose(big_outf[1]) == EOF) fatal("close failed");
	}
	// fprintf(stderr, "main: freqp = %d (point 1b)\n", freqp);
	piece_ptr = 0;
	big_outf[0] = fopen(filename2(filenames[4], av[2], "big.X", piece), "wb");
	big_outf[1] = fopen(filename2(filenames[5], av[2], "big.Y", piece), "wb");
	piece++;

	// fprintf(stderr, "main: freqp = %d (point 1c)\n", freqp);
      }      
      outf = big_outf;
      piece_ptr++;
    }
    // fprintf(stderr, "main: freqp = %d (point 2)\n", freqp);
    my_output(outf, X+p, Y+p, freqp);
  }
}
