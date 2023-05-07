#include <stdio.h>
#include <stdlib.h>

void usage()
{
  fprintf(stderr, "x_to_y xy, where xy is a 2-letter string indicating a type for stdin (x) and a type for stdout (y)\
One of them must be 'a' (ascii) and the other must be something else:\
'i' (int)\
's' (short)\
'L' (long long)\
'f' (float)\
'd' (double)\
'c' (char)\n");
  exit(2);
}

void wfail()
{
  fprintf(stderr, "x_to_y: write failed\n");
  exit(2);
}

void case_ai()
{
  int j;
  while(scanf("%d", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_as()
{
  short j;
  while(scanf("%d", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}


void case_aL()
{
  long long j;
  while(scanf("%Ld", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_af()
{
  float j;
  while(scanf("%f", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_ad()
{
  double j;
  while(scanf("%lf", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_ac()
{
  int j;
  while(scanf("%d", &j) == 1)
    if(fwrite(&j, sizeof(char), 1, stdout) != 1) wfail();
}

void case_si()
{
  int j;
  while(scanf("%d", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_sL()
{
  long long j;
  while(scanf("%Ld", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_sf()
{
  float j;
  while(scanf("%f", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}


void case_sd()
{
  double j;
  while(scanf("%lf", &j) == 1)
    if(fwrite(&j, sizeof(j), 1, stdout) != 1) wfail();
}

void case_sc()
{
  int j;
  while(scanf("%d", &j) == 1)
    if(fwrite(&j, sizeof(char), 1, stdout) != 1) wfail();
}

void case_ia()
{
  int j;
  while(fread(&j, sizeof(j), 1, stdin) == 1)
    printf("%d\n", j);
}

void case_sa()
{
  short j;
  while(fread(&j, sizeof(j), 1, stdin) == 1)
    printf("%d\n", j);
}


void case_La()
{
  long long j;
  while(fread(&j, sizeof(j), 1, stdin) == 1)
    printf("%Ld\n", j);
}

void case_fa()
{
  
  float j;
  while(fread(&j, sizeof(j), 1, stdin) == 1)
    printf("%f\n", j);
}

void case_da()
{
   double j;
   while(fread(&j, sizeof(j), 1, stdin) == 1)
     printf("%f\n", j);
}

void case_ca()
{
  char j;
  while(fread(&j, sizeof(j), 1, stdin) == 1)
    printf("%d\n", j);
}

int main(int ac, char **av)
{
  if(ac != 2) usage();
  
  if(strcmp(av[1], "ai") == 0) case_ai();
  else if(strcmp(av[1], "as") == 0) case_as();
  else if(strcmp(av[1], "aL") == 0) case_aL();
  else if(strcmp(av[1], "af") == 0) case_af();
  else if(strcmp(av[1], "ad") == 0) case_ad();
  else if(strcmp(av[1], "ac") == 0) case_ac();

  else if(strcmp(av[1], "ia") == 0) case_ia();
  else if(strcmp(av[1], "sa") == 0) case_sa();
  else if(strcmp(av[1], "La") == 0) case_La();
  else if(strcmp(av[1], "fa") == 0) case_fa();
  else if(strcmp(av[1], "da") == 0) case_da();
  else if(strcmp(av[1], "ca") == 0) case_ca();
  
  else usage();

  exit(0);
}
