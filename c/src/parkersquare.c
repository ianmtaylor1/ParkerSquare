#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <gmp.h>

#include "primes.h"



int main(void) {
    primefactor_t factors[3];
    mpz_t value;
    size_t sscount;

    mpz_init(value);

    factors[0].p = 2;
    factors[0].e = 30;
    factors[1].p = 3;
    factors[1].e = 4;
    factors[2].p = 41;
    factors[2].e = 30;

    printf("Hello world!\n");

    tovalue(value, factors, 3);
    sscount = countsumsquares(factors, 3);

    gmp_printf("%Zd\n", value);
    printf("%lu\n", sscount);

    mpz_clear(value);
}
