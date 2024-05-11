#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "rand64-sw.h"

/* Software implementation.  */

/* Input stream containing random bytes.  */
FILE *urandstream;
struct drand48_data buffer;

/* Initialize the software rand64 implementation.  */
void software_rand64_init (char* filename)
{
  if (filename) {
    urandstream = fopen (filename, "r");
    if (! urandstream) {
      fprintf(stderr, "error: cannot open file: %s\n", filename);
      exit(1);
    }
  }
  else {
    srand48_r(time(NULL), &buffer);
  }
}

/* Return a random value, using software operations.  */
unsigned long long software_rand64 (void)
{
  unsigned long long x;

  if (fread (&x, sizeof x, 1, urandstream) != 1) {
    fprintf(stderr, "error: cannot read the file\n");
    exit(1);
  }

  return x;
}

/* Finalize the software rand64 implementation.  */
void software_rand64_fini (void)
{
  fclose(urandstream);
}


/* Initialize the software lrand48 implementation.  */
void software_lrand48_r_init (void)
{
  srand48_r(time(NULL), &buffer);
}

/* Return a random value, using software operations.  */
unsigned long long software_lrand48_r (void)
{
  // generates 64-bit random number by generating two 32-bit numbers and combining them
  long int lower;
  long int upper;
  mrand48_r(&buffer, &lower);
  mrand48_r(&buffer, &upper);
  return ((unsigned long long)upper << 32) | (unsigned long long)lower;
}

/* Finalize the software lrand48 implementation.  */
void software_lrand48_r_fini (void)
{
}