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

size_t primesumsquares(pair_t *out, unsigned long prime);
size_t primepowersumsquares(pair_t *out, primefactor_t pf);
size_t getsumsquares(pair_t *out, const primefactor_t *pf, size_t pflen);

#endif //ifndef SQUARES_H