#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

int main(int ac, char **av)
{
  int x, res[256];
  memset(res, 0, sizeof(int)*256);
  
  while((x=getchar()) != EOF)
    res[x]++;
  
  for(x=0;x<256;x++)
    printf("%d\t%d\n", x, res[x]);

}
