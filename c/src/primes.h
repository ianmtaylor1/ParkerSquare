#ifndef PRIMES_H
#define PRIMES_H

#include <stdlib.h>
#include <stdbool.h>
#include <gmp.h>

typedef struct primefactor_t {
    unsigned long p;
    unsigned long e;
} primefactor_t;

void tovalue(mpz_t out, const primefactor_t *factors, size_t len);
size_t tostring(char *buf, size_t buflen, const primefactor_t *factors, size_t faclen);

bool isprime(unsigned long n);
unsigned long nextprime(unsigned long n);

#endif //ifndef PRIMES_H