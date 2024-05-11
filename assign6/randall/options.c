#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "options.h"

int get_options(int argc, char **argv, long long *nbytes,
							enum input *i_option, enum output *o_option,
							char **filename, long long *N)
{
	int c; // store option char

	while ((c = getopt(argc, argv, "i:o:")) != -1) {
		switch (c) {
		case 'i':
			if (strcmp(optarg, "rdrand") == 0) {
				*i_option = i_rdrand;
			}
			else if (strcmp(optarg, "lrand48_r") == 0) {
				*i_option = i_lrand48_r;
			}
			else if (optarg[0] == '/') {
				*i_option = i_file;
				*filename = strdup(optarg);
				// check if the memory allocation was successful
				if (*filename == NULL) {
					fprintf(stderr,
						"error: failed to allocate memory for file: %s\n",
						optarg
					);
					return 1;
				}
			}
			else {
				fprintf(stderr, "%s: invalid -i option arg: %s\n",
					argv[0], optarg
				);
				return 1;
			}
			break;

		case 'o':
			if (strcmp(optarg, "stdio") == 0) {
				*o_option = o_stdio;
			}
			else {
				// check if the argument is a positive decimal integer
				errno = 0;
				char *endptr;
				*N = strtoll(optarg, &endptr, 10); // string to long long
				
				// check if the conversion was successful
				if (errno || *endptr != '\0' || *N <= 0) {
					if (errno)
						perror(optarg);
					else
						fprintf(stderr, "%s: invalid -o option arg: %s\n",
							argv[0], optarg
						);
					return 1;
				}

				*o_option = o_n;
			}
			break;
			
		default:
			return 1;
		}
	}

	// check if there are any non-option arguments
	if (optind < argc) {
		// check if there are more than one non-option arguments
		if (optind + 1 < argc) {
			fprintf(stderr, "%s: extra operand: %s\n",
				argv[0], argv[optind + 1]
			);
			return 1;
		}

		// check if the non-option argument is a positive decimal integer
		errno = 0;
		char *endptr;
		*nbytes = strtoll(argv[optind], &endptr, 10);

		if (errno || *endptr != '\0' || *nbytes < 0) {
			if (errno)
				perror(argv[optind]);
			else
				fprintf(stderr, "%s: invalid NBYTES: %s\n", argv[0], argv[optind]);
			return 1;
		}
	}
	else {
		fprintf(stderr, "%s: usage: %s [-i INPUT] [-o OUTPUT] NBYTES\n", argv[0], argv[0]);
		return 1;
	}

	return 0;
}