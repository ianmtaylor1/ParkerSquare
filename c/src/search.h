#ifndef SEARCH_H
#define SEARCH_H

#include <stddef.h>
#include <gmp.h>
#include "primes.h"
#include "squares.h"

int findparkersquare(mpz_t *square, const primefactor_t *rootmidfac, size_t numfac);

#ifdef TESTING
int constructsquare(
    mpz_t *square,
    const primefactor_t *rootmidfac, size_t numfac,
    const pair_t *outerpairs, size_t numpairs);
int twice_squared(primefactor_t *out, const primefactor_t *in, size_t len);
size_t square_filter(pair_t *pairs, size_t len);
#endif //ifdef TESTING

#endif //ifndef SEARCH_H