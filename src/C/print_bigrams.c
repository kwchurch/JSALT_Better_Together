#include <stdio.h>
#include "util.h"

int main(int ac, char *av)
{
  struct bigram b;
  while(fread(&b, sizeof(b), 1, stdin) > 0) {
    printf("%0.2f\t%d\t%d\n", b.val, b.elts[0], b.elts[1]);
  }
}


      
    
  
