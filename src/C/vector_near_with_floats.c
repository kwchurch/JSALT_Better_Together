#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>

int verbose = 1;
int show_details = 0;
int find_best = 1;
int threshold = 0;
int record_size = -1;
int random_bytes = -1;
float *floats = NULL;
long nfloats = -1;

void usage()
{
  fatal("usage: cat vector | near_with_floats --dir <dir> --offset <n> index1 index2 index3 > report");
}

// input two vectors (a and b) of length n
double dot(float *a, float *b, int n)
{
  double res = 0;
  float *end = a+n;
  while(a<end)
    res += *a++ * *b++;
  return res;
}

/* // output the sign of the dot product of the two input vectors */
/* int dot(float *a, float *b, int n) */
/* { */
/*   double res = 0; */
/*   float *end = a+n; */
/*   while(a<end) */
/*     res += *a++ * *b++; */

/*   return (res > 0); */
/* } */

// F are some floats from an embedding with K hidden dimensions
// R are random floats of length 8*K

// output a byte (8 bits), where each bit is the sign of the dot
// product of the random vector with F

int do_it1(float *F, float *R, int K)
{
  int i = 0;
  int res = 0;
  for(i=0;i<8;i++,R+=K) 
    res = 2*res + (dot(F, R, K) > 0);
  return res;
}

// want uniform random floats between -1 and 1
void init_random_floats(float *res, int n)
{
  float *end = res + n;
  double d = RAND_MAX/2.0;
  while(res < end)
    *res++ = rand()/d - 1.0;
}      

struct idx {
  float *random_floats;
  long *idx, nidx;
  long *idx_inv, nidx_inv;
};

struct node_map{
  int *old_to_new;
  int *new_to_old;
  long nold_to_new, nnew_to_old;
};

int long_compare(long *a, long *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

struct node_map *the_node_map = NULL;

int NEW_TO_OLD = 1;
int OLD_TO_NEW = 0;

long map_node(long node, int new_to_old, int no_map)
{

  if(no_map) return node;
  struct node_map *M = the_node_map;

  if(!M) return node;
  long N;
  int *MM;

  if(new_to_old) {
    MM = M->new_to_old;
    N = M->nnew_to_old;
  }
  else {
    MM = M->old_to_new;
    N = M->nold_to_new;
  }

  if(node < 0 || node >= N) {
    fprintf(stderr, "warning, node = %ld; N = %ld\n", node, N);
    fatal("confusion in map_node");
  }

  return MM[node];
}

void vec2bytes(char *bytes, int random_bytes, float *vec, int record_size, struct idx *idx)
{
  // fprintf(stderr, "vec2bytes: random_bytes = %d, record_size = %d\n", random_bytes, record_size);
  float *R = idx->random_floats;
  int i;
  for(i=0; i<random_bytes; i++,R+=8*record_size)
    *bytes++ = do_it1(vec, R, record_size);
}

double SMALL = 1e-10;

double norm(float *a, int n)
{
  double res = 0;
  float *end = a+n;
  while(a<end) {
    float aa = *a++;
    res += aa * aa;
  }
  return sqrt(res);
}

double my_cos(float *a, float *b, int n)
{
  if(a == floats || b == floats) return -1.0;

  double alen = norm(a, n);
  if(alen < SMALL) return -1.0;
  double blen = norm(b, n);
  if(blen < SMALL) return -1.0;
  double res = dot(a, b, n)/(alen * blen);
  // fprintf(stderr, "res = %f, alen = %f, blen = %f, n = %d\n", res, alen, blen, n);
  return res;
}

int good_index(struct idx *idx)
{
  return ((idx->nidx > 0) && (idx->nidx_inv == idx->nidx));
}

char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}

int filename_to_seed(char *fn)
{
  char *end = fn + strlen(fn) - 2;
  if(strcmp(end, ".i") != 0) fatal("confusion in filename to seed");
  while(end > fn && isdigit(end[-1])) end--;
  return atoi(end);
}

void init_node_map(char *filename)
{
  char buf[1024];
  the_node_map = (struct node_map *)malloc(sizeof(struct node_map));
  if(!the_node_map) fatal("malloc failed");

  the_node_map->old_to_new = (int *)mmapfile(my_filename(buf, filename, "old_to_new.i"), &the_node_map->nold_to_new);
  the_node_map->new_to_old = (int *)mmapfile(my_filename(buf, filename, "new_to_old.i"), &the_node_map->nnew_to_old);
  the_node_map->nold_to_new /= sizeof(int);
  the_node_map->nnew_to_old /= sizeof(int);
}

void init_idx(struct idx *idx, char *filename)
{
  char buf[1024];
  memset(idx, 0, sizeof(struct idx));
  
  if(file_exists(filename)) {
    idx->idx = (long *)mmapfile(filename, &idx->nidx);
    idx->nidx /= sizeof(long);
  }

  char *fn = my_filename(buf, filename, "inv");
  if(file_exists(fn)) {
    idx->idx_inv = (long *)mmapfile(fn, &idx->nidx_inv);
    idx->nidx_inv /= sizeof(long);
  }

  int seed = filename_to_seed(filename);
  srand(seed);
  idx->random_floats = (float *)malloc(sizeof(float) * record_size * random_bytes * 8);				       
  init_random_floats(idx->random_floats, record_size * random_bytes * 8);
  if(verbose) fprintf(stderr, "init_idx: %s, seed: %d, nidx: %ld, nidx_inv: %ld\n", filename, seed, idx->nidx, idx->nidx_inv);
}

struct idx *init_indexes(char **filenames, int n)
{
  int i;
  struct idx *indexes = (struct idx *)malloc(n * sizeof(struct idx));
  for(i=0; i<n; i++) {
    if(verbose) fprintf(stderr, "filenames[%d] = %s\n", i, filenames[i]);
    init_idx(indexes+i, filenames[i]);
  }
  return indexes;
}

void check_sort(struct idx *idx)
{
  char *buf = malloc(random_bytes*2);
  char *buf2 = buf+random_bytes;
  vec2bytes(buf, random_bytes, floats + idx->idx[0] * record_size, record_size, idx);
  long i;
  for(i=1;i<idx->nidx;i++) {
    vec2bytes(buf2, random_bytes, floats + idx->idx[i] * record_size, record_size, idx);
    int comp = memcmp(buf, buf2, random_bytes);
    if(comp > 0) fprintf(stderr, "check_sort (disorder): i: %ld\tcomp: %d\n", i, comp);
    memcpy(buf, buf2, random_bytes);
  }
}


long paper_near(char *bytes, int random_bytes, struct idx *idx)
{
  char *buf = malloc(random_bytes*4);
  if(!buf) fatal("malloc failed");
  memset(buf, 0, random_bytes*4);
  char *buf_lo = buf+random_bytes;
  char *buf_hi = buf_lo+random_bytes;
  char *buf2 = buf_hi+random_bytes;

  long lo = 0;
  long hi = idx->nidx;
  while(hi - lo > 3) {
    long mid = lo + (hi-lo)/2;

    vec2bytes(buf, random_bytes, floats + idx->idx[mid] * record_size, record_size, idx);
    // vec2bytes(buf2, random_bytes, floats + mid * record_size, record_size, idx);
    
    vec2bytes(buf_lo, random_bytes, floats + idx->idx[lo] * record_size, record_size, idx);
    vec2bytes(buf_hi, random_bytes, floats + idx->idx[hi-1] * record_size, record_size, idx);

    int comp = memcmp(buf, bytes, random_bytes);
    int comp_sanity = memcmp(buf_lo, buf_hi, random_bytes);
    // int comp_sanity0 = memcmp(buf, buf2, random_bytes);

    int comp_sanity1 = memcmp(buf_lo, buf, random_bytes);
    int comp_sanity2 = memcmp(buf, buf_hi, random_bytes);

    /* fprintf(stderr, "paper_near: lo = %ld, mid = %ld, hi = %ld; comp = %d, comp_sanity = %d, %d, %d\n", */
    /* 	    lo, mid, hi, comp, comp_sanity, comp_sanity1, comp_sanity2); */
    
    if(comp_sanity > 0) fatal("confusion: sanity");
    if(comp_sanity1 > 0) fatal("confusion: sanity1");
    if(comp_sanity2 > 0) fatal("confusion: sanity2");

    if(comp == 0) return idx->idx[mid];
    else if(comp < 0) lo = mid;
    else hi = mid+1;
  }
  for(; lo <  hi; lo++) {
    // fprintf(stderr, "paper_near: lo = %ld, hi = %ld\n", lo, hi);
    vec2bytes(buf, random_bytes, floats + idx->idx[lo] * record_size, record_size, idx);
    int comp = memcmp(buf, bytes, random_bytes);
    if(comp >= 0) return idx->idx[lo];
  }
  free(buf);
  return idx->idx[lo];
}

long *find_near(long paper, struct idx *idx, int offset, int *nfound)
{
  if(paper < 0 || paper >= idx->nidx) {
    fprintf(stderr, "paper = %ld\n", paper);
    fatal("confusion: paper is out of range");
  }
  long o = idx->idx_inv[paper];

  if(o < 0 || o >= idx->nidx) fatal("confusion: o is out of range");

  long start = o - offset;
  long end = o + offset;
  if(start < 0) start=0;
  if(end >= idx->nidx) end = idx->nidx - 1;
  *nfound = end - start;
  return idx->idx + start;
}

void get_args_from_dir(char *dir)
{
  // fprintf(stderr, "get_args_from_dir: %s\n", dir);
  char buf[1024];
  sprintf(buf, "%s/record_size", dir);

  FILE *fd = fopen(buf, "r");
  fscanf(fd, "%d", &record_size);
  fgets(buf, 1024, fd);
  fscanf(fd, "%d", &random_bytes);
  fclose(fd);
  
  sprintf(buf, "%s/embedding.f", dir);
  floats = (float *)mmapfile(buf, &nfloats);
  nfloats /= sizeof(float);

  sprintf(buf, "%s/map", dir);
  init_node_map(buf);
  // fprintf(stderr, "leaving, get_args_from_dir: %s, record_size = %d, random_bytes = %d, nfloats = %ld\n", dir, record_size, random_bytes, nfloats);
}    

int main(int ac, char **av)
{
  // fprintf(stderr, "entering main\n");
  int i;
  long old_paper_id;
  struct idx *indexes;
  int nindexes = -1;
  int offset = -1;
  int no_map = 1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--dir") == 0) {
      // fprintf(stderr, "found --dir\n");
      no_map = 0;
      get_args_from_dir(av[++i]);
    }
    else if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--offset") == 0) offset = atoi(av[++i]);
    else {
      nindexes=ac-i;
      indexes = init_indexes(av+i, nindexes);
      break;
    }
  }

  // fprintf(stderr, "nindexes = %d\n", nindexes);
  // fprintf(stderr, "record_size = %d\n", record_size);
  // fflush(stderr);

  if(!floats) fatal("no floats???");
  if(nindexes <= 0) fatal("no indexes???");
  if(offset <= 0) fatal("--offset arg is required");
  if(record_size <= 0) fatal("--record_size arg is required");

  float *vec = (float *)malloc(sizeof(float) * record_size);
  if(!vec) fatal("malloc failed");
  char *bytes = (char *)malloc(sizeof(char) * random_bytes * 3);
  if(!bytes) fatal("malloc failed");
  memset(bytes, 0, random_bytes * 3);
  char *bytes2 = bytes + random_bytes;
  char *bytes3 = bytes2 + random_bytes;

  // check_sort(indexes);
  
  while(fread(vec, sizeof(float), record_size, stdin) == record_size) {
    for(i=0;i<nindexes;i++) {
      if(good_index(indexes+i)) {
	vec2bytes(bytes, random_bytes, vec, record_size, indexes+i);
	long new_paper_id = paper_near(bytes, random_bytes, indexes+i);
	long old_paper_id = map_node(new_paper_id, NEW_TO_OLD, no_map);

	int nfound;
	long *found = find_near(new_paper_id, indexes + i, offset, &nfound);
	long *end = found + nfound;
	while(found < end) {
	  long new_j = *found++;
	  long old_j = map_node(new_j, NEW_TO_OLD, no_map);

	  vec2bytes(bytes3, random_bytes, floats + new_j * record_size, record_size, indexes+i);
	  int comp1 = memcmp(bytes2, bytes3, random_bytes);
	  int comp2 = memcmp(bytes, bytes3, random_bytes);

	  printf("%f\t%f\t%d\t%d\t%ld\t%ld\t%ld\t%ld\t%d\t%s\n",
		 my_cos(floats + found[0] * record_size, floats + new_j * record_size, record_size),
		 my_cos(vec, floats + new_j * record_size, record_size),
		 comp1, comp2,
		 old_paper_id, old_j,
		 new_paper_id, new_j,
		 i,
		 av[ac - nindexes + i]);
	  memcpy(bytes2, bytes3, random_bytes);

	}
      }
    }
  }
}
