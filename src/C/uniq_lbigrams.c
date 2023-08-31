#include <stdio.h>
#include <strings.h>
#include "util.h"

void usage()
{
  fatal("uniq_bigrams --sum --max < bigrams > bigrams.uniq");
}

void my_output(struct lbigram *out)
{
  if(out->val != 0) {
    if(fwrite(out, sizeof(struct lbigram), 1, stdout) != 1)
      fatal("write failed");
  }
 }

int main(int ac, char **av)
{
  int max_option = 0;
  int sum_option = 0;
  if(ac == 2 && strcmp(av[1], "--max") == 0) max_option=1;
  if(ac == 2 && strcmp(av[1], "--sum") == 0) sum_option=1;
  else if(ac != 1) usage();
  struct lbigram b;
  struct lbigram out;
  out.val=0;

  while(fread(&b, sizeof(struct lbigram), 1, stdin) == 1) {
    if(lbigram_compare(&out, &b) == 0) {
      if(max_option) {
	if(b.val > out.val) out.val = b.val;
      }
      else if(sum_option) {
	out.val += b.val;
      }
    }
    else {
      my_output(&out);
      memcpy(&out, &b, sizeof(struct lbigram));
    }
  }

  my_output(&out);

  return 0;
}
