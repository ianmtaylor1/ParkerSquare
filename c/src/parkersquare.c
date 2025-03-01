#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <gmp.h>

#include "primes.h"

typedef struct pair_t {
    mpz_t first;
    mpz_t second;
} pair_t;

void pair_array_init(pair_t *pairs, size_t len) {
    size_t i;
    for (i = 0; i < len; i++) {
        mpz_init(pairs[i].first);
        mpz_init(pairs[i].second);
    }
}
void pair_init(pair_t *pair) {
    pair_array_init(pair, 1);
}

void pair_array_clear(pair_t *pairs, size_t len) {
    size_t i;
    for (i = 0; i < len; i++) {
        mpz_clear(pairs[i].first);
        mpz_clear(pairs[i].second);
    }
}
void pair_clear(pair_t *pair) {
    pair_array_clear(pair, 1);
}

/*
Count the number of ways the number represented by the given prime
factorization can be written as the sum of two squares.
*/
size_t countsumsquares(const primefactor_t *factors, size_t len) {
    size_t count = 4;
    size_t i;
    for (i = 0; i < len; i++) {
        if (factors[i].p % 4 == 1) {
            count *= factors[i].e + 1;
        } else if (factors[i].p % 4 == 3 && factors[i].e % 2 == 1) {
            count = 0;
        }
        // If p == 2, or the power of a prime == 3(mod4) is even, no change
    }
    return count;
}

/*
Integer square root - largest integer less than or equal to the
square root of value. Binary search for root.
*/
unsigned long long isqrt(unsigned long long value) {
    unsigned long long mid, high, low;
    high = value + 1;
    low = 0;
    while (low < high - 1) {
        mid = (high + low) / 2;
        if (mid * mid <= value) {
            low = mid;
        } else {
            high = mid;
        }
    }
    return low;
}

/*
*/
void primesumsquares(pair_t *out, unsigned long prime) {
    unsigned long a, asquared, b, bsquared;
    a = 1;
    asquared = 1;
    bsquared = prime - asquared;
    b = isqrt(bsquared);
    while (asquared + bsquared != prime && a < b) {
        if (asquared + bsquared > prime) {
            b--;
            bsquared -= b + b + 1;

        } else if (asquared + bsquared < prime) {
            a++;
            asquared += a + a - 1;
        }
    }
    mpz_set_ui(out->first, a);
    mpz_set_ui(out->second, b);
}

void diophantus(pair_t *out, pair_t ab, pair_t cd) {
    // a*c - b*d
    mpz_mul(out->first, ab.first, cd.first);
    mpz_submul(out->first, ab.second, cd.second);
    // a*d + b*c
    mpz_mul(out->second, ab.first, cd.second);
    mpz_addmul(out->second, ab.second, cd.first);
}

/*
*/
void primepowersumsquares(pair_t *out, primefactor_t pf) {
    pair_t tmp[pf.e + 1];
    pair_t base, rev;
    unsigned long i;

    pair_array_init(tmp, pf.e);
    pair_init(&base);
    pair_init(&rev);

    // Get the base pairs: sums of squares to the prime p
    primesumsquares(&base, pf.p);
    mpz_set(rev.first, base.second);
    mpz_set(rev.second, base.first);
    // Initialize the first element of each array to 'one'
    mpz_set_ui(out[0].first, 1);
    mpz_set_ui(out[1].second, 0);
    mpz_set_ui(tmp[0].first, 1);
    mpz_set_ui(tmp[1].second, 0);
    // Construct the rest of each array with powers of each base
    for (i = 1; i <= pf.e; i++) {
        diophantus(&out[i], out[i-1], base);
        diophantus(&tmp[i], tmp[i-1], rev);
    }
    // Combine the arrays
    for (i = 0; i <= pf.e; i++) {
        diophantus(&out[i], out[i], tmp[pf.e - i]);
    }

    pair_array_clear(tmp, pf.e);
    pair_clear(&base);
    pair_clear(&rev);
}

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
