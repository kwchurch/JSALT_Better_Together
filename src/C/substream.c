#include <stdio.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fprintf(stderr, "usage: substream N < foo > bar\n");
  exit(2);
}


#define BUFSIZE 65536

int main(int ac, char **av)
{
  long start=0, end=0, i, N;
  if(ac == 2) end = atol(av[1]);
  else if(ac == 3) {
    start = atol(av[1]);
    end = atol(av[2]);
  }
  else usage();
    
  if(start >  0) {
    if(fseek(stdin, start, SEEK_SET) != 0) {
      fprintf(stderr, "seek failed");
      exit(2);
    }
  }
  else if(start < 0) {
    start *= -1;
    if(fseek(stdin, start, SEEK_END) != 0) {
      fprintf(stderr, "seek failed");
      exit(2);
    }
  }

  if(end < 0) {
    for(; ;) {
      int c = getchar();
      if(c == EOF) return 0;
      putchar(c);
    }
  }
    
  N = end - start;

  char buf[BUFSIZE];
  i=0;
  for(;;){
    if(i+BUFSIZE > N) break;
    int found = fread(buf, sizeof(char), BUFSIZE, stdin);
    if(found != BUFSIZE) {
      fprintf(stderr, "confusion: found = %d\n", found);
      exit(2);
    }
    i+=found;
    if(fwrite(buf, sizeof(char), found, stdout) != found) {
      fprintf(stderr, "write failed\n");
      exit(2);
    }
  }

  for(;i<N;i++) {
    int c = getchar();
    putchar(c);
  }
}
