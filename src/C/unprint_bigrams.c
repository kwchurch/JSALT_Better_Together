#include <stdio.h>
#include "util.h"

int main(int ac, char *av)
{
  struct bigram b;

  while(scanf("%f%d%d", &b.val, b.elts, b.elts+1) == 3)
    if(fwrite(&b, sizeof(b), 1, stdout) != 1)
      fatal("write failed");
}


      
    
  
