#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#include <gmp.h>

#include "primes.h"

/*
Compute the value of the number given by a prime factorization and store
the result in the mpz_t number out.
*/
void tovalue(mpz_t out, const primefactor_t *factors, size_t len) {
    mpz_t tmp;
    size_t i;
    mpz_init(tmp);
    mpz_set_ui(out, 1ul);
    for (i = 0; i < len; i++) {
        mpz_ui_pow_ui(tmp, factors[i].p, factors[i].e);
        mpz_mul(out, out, tmp);
    }
    mpz_clear(tmp);
}

/*
Represent the prime factorization as a string, storing at most buflen
characters in buf, including the null terminator. Uses snprintf behind
the scenes.
*/
size_t tostring(char *buf, size_t buflen, const primefactor_t *factors, size_t faclen) {
    size_t start = 0;
    size_t idx;
    size_t written;

    for (idx = 0; idx < faclen && start < buflen; idx++) {
        if (idx == 0) {
            written = snprintf(buf + start, buflen - start, "%lu^%lu", factors[idx].p, factors[idx].e);
        } else {
            written = snprintf(buf + start, buflen - start, " * %lu^%lu", factors[idx].p, factors[idx].e);
        }
        start += written;
    }

    return start;
}

/* Return true if a number n is prime, false if it is not.
*/
bool isprime(unsigned long n) {
    unsigned long p, psquared;
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;
    p = 3;
    psquared = 9;
    while (psquared < n && n % p != 0) {
        // (a + 2)^2 = a^2 + (4a + 4) = a^2 + [4(a+2) - 4] = a^2 + 4[(a+2) - 1]
        p += 2;
        psquared += 4 * (p - 1);
    }
    return n % p != 0;
}

/* Return the next prime number that is strictly larger than n.
*/
unsigned long nextprime(unsigned long n) {
    unsigned long i = n + 1;
    while (!isprime(i)) {
        i++;
    }
    return i;
}