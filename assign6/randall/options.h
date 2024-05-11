#ifndef OPTIONS_H
#define OPTIONS_H

enum input { i_none, i_rdrand, i_lrand48_r, i_file };
enum output { o_none, o_stdio, o_n };

int get_options(int argc, char **argv, long long *nbytes,
                enum input *i_option, enum output *o_option,
                char **filename, long long *N);

#endif