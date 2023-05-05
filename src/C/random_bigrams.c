#include <stdio.h>
#include "util.h"
#include <openssl/rand.h>

void usage()
{
  fatal("usage: random_bigrams bigrams Nout");
}
 
int main(int ac, char **av)
{
  if(ac != 3) usage();
  long N, i, key;
  struct bigram *b = (struct bigram *)mmapfile(av[1], &N);
  N /= sizeof(struct bigram);

  int Nout = atoi(av[2]);

  for(i=0;i<Nout;i++) {
    
    if(RAND_bytes((void *)&key, sizeof(key)) != 1)
      fatal("random failed");

    key = key % N;
    if(key < 0) key += N;

    if(fwrite(b + key, sizeof(struct bigram), 1, stdout) != 1)
      fatal("write failed");
  }
}


      
    
  
