#include <stdio.h>
#include <memory.h>
#include <strings.h>
#include <stdlib.h>

#define MAXLINE 20000

int common_prefix(char *a, char *b)
{
  int i;
  for(i=0; ;i++)
    if(a[i] != b[i] || a[i] == 0) return i;
}

int main(int ac, char **av)
{
  char buf[2][MAXLINE];

  memset(buf, 0, 2*MAXLINE);
  
  while(1) {
    strcpy(buf[0], buf[1]);
    if(fgets(buf[1], 1024, stdin) == NULL) break;
    printf("%d\t%s", common_prefix(buf[0], buf[1]), buf[1]);
  }
}
