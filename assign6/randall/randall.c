/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"

/* Main program, which outputs N bytes of random data.  */
int main (int argc, char **argv)
{
  long long nbytes = 0;
  enum input i_option = i_none;
  enum output o_option = o_none;
  char* filename = NULL;
  long long N = 0;

  int status = get_options(argc, argv, &nbytes, &i_option, &o_option, &filename, &N);

  if (status) return status;
  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0) return 0;


  unsigned long long (*rand64) (void);
  void (*finalize) (void);

  if (i_option == i_lrand48_r) {
    software_lrand48_r_init();
    rand64 = software_lrand48_r;
    finalize = software_lrand48_r_fini;
  }
  else if (i_option == i_file) {
    software_rand64_init(filename);
    rand64 = software_rand64;
    finalize = software_rand64_fini;
  }
  else { // i_option == i_rdrand || i_none
    if (rdrand_supported()) {
      hardware_rand64_init();
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
    }
    else {
      fprintf(stderr, "error: rdrand not supported\n");
      return 1;
    }
  }
  
  
  int output_errno = 0;
  int wordsize = sizeof rand64();

  if (o_option == o_n) {
    char *buf = (char *) malloc(N);
    unsigned long long x;

    if (buf == NULL) {
      fprintf(stderr, "error: failed to allocate memory\n");
      return 1;
    }

    // Write N bytes at a time
    while (nbytes > 0) {
      size_t outbytes = MIN(nbytes, N);
      for (size_t i = 0; i < outbytes; i += wordsize) {
        x = rand64();
        generate_random_word(x, buf + i);
      }
      write_n(buf, outbytes, N);
      nbytes -= outbytes;
    }
    
    free(buf);
  }
  else { // o_option == o_stdio || o_none
    while (nbytes > 0) {
      unsigned long long x = rand64();
      int outbytes = nbytes < wordsize ? nbytes : wordsize;

      if (!writebytes (x, outbytes)) {
        output_errno = errno;
        break;
      }

      nbytes -= outbytes;
    }
  }

  
  if (fclose(stdout) != 0) {
    output_errno = errno;
  }

  if (output_errno) {
    errno = output_errno;
    perror("output");
  }
  
  finalize();

  return !!output_errno;
}
