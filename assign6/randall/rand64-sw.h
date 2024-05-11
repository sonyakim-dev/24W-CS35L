#ifndef RAND64SW_H
#define RAND64SW_H

void software_rand64_init (char* filename);
unsigned long long software_rand64 (void);
void software_rand64_fini (void);

void software_lrand48_r_init (void);
unsigned long long software_lrand48_r (void);
void software_lrand48_r_fini (void);

#endif