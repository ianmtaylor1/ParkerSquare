#ifndef SQUARES_H
#define SQUARES_H

#include <stdlib.h>

#include "primes.h"

typedef struct pair_t {
    mpz_t first, second;
} pair_t;

void pair_array_init(pair_t *pairs, size_t len);
void pair_init(pair_t *pair);
void pair_array_clear(pair_t *pairs, size_t len);
void pair_clear(pair_t *pair);

size_t countsumsquares(const primefactor_t *factors, size_t len);
void getsumsquares(pair_t *out, const primefactor_t *pf, size_t pflen);

#ifdef TESTING
/* Testing functions, only need to expose if we're testing them. */
unsigned long isqrt(unsigned long value);
void diophantus(pair_t *out, const pair_t *ab, const pair_t *cd);
size_t primesumsquares(pair_t *out, unsigned long prime);
size_t primepowersumsquares(pair_t *out, primefactor_t pf);
void getunits(pair_t *out);
void diophantus_prod(pair_t *out, pair_t *arr1, size_t len1, pair_t *arr2, size_t len2);
#endif //ifdef TESTING

#endif //ifndef SQUARES_H