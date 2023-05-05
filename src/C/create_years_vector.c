#include <stdio.h>
#include <memory.h>
#include <stdlib.h>

int main(int ac, char **av)
{
  long errors = 0;
  long N = atol(av[1]);
  long key;
  int val;
  short *result = (short *)malloc(sizeof(short) * N);
  if(!result) {
    fprintf(stderr, "malloc failed\n");
    exit(2);
  }

  memset(result, 0, sizeof(short)*N);
  
  while(scanf("%ld%d", &key, &val) == 2) {
    if(key > 0 && key < N) result[key] = val;
    else errors++;
  }

  fprintf(stderr, "%ld errors\n", errors);

  while(result[N-1] == 0) N--;
  
  if(fwrite(result, sizeof(short), N, stdout) != N) {
    fprintf(stderr, "write failed\n");
    exit(2);
  }    

  return 0;
}
