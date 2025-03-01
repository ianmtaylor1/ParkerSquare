#include <stdlib.h>
#include <math.h>

#include <gmp.h>

#include "primes.h"
#include "squares.h"

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
unsigned long isqrt(unsigned long value) {
    unsigned long mid, high, low;
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
Return a single instance of a pair_t whose squares add to the
given prime. Store the result in out, return 1 if a pair was
found, 0 if not.
*/
size_t primesumsquares(pair_t *out, unsigned long prime) {
    // By cases by the modulus of the prime
    if (prime % 4 == 3) {
        return 0;
    } else {
        // For 2 or primes congruent to 1 mod 4
        unsigned long a = 1, asquared = 1;
        unsigned long b, bsquared;
        b = isqrt(prime - asquared);
        bsquared = b * b;
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
        return 1;
    }
}

/*
Perform diophantus's identity with the pairs ab and cd to
produce a new pair which is stored in out. If ab represents
a complex number (a + bi) and cd respresents (c + di), then
the result represents (a+bi)(c+di)'s real and imaginary components.
*/
void diophantus(pair_t *out, pair_t ab, pair_t cd) {
    // a*c - b*d
    mpz_mul(out->first, ab.first, cd.first);
    mpz_submul(out->first, ab.second, cd.second);
    // a*d + b*c
    mpz_mul(out->second, ab.first, cd.second);
    mpz_addmul(out->second, ab.second, cd.first);
}

/*
For a prime pf.p raised to a power pf.e, find up to pf.e + 1 'distinct' pairs
(a,b) such that a^2 + b^2 = p^e. The results will be 'distinct' up to pi/2
rotation, i.e., (a,b), (-b,a), (-a,-b), (b,-a) are all considered the same.
Stores the result in the array out, returns the number found. It will either
find 0, 1, or e+1 such pairs, depending on the prime and power.
*/
size_t primepowersumsquares(pair_t *out, primefactor_t pf) {
    // Break into cases based on prime and power
    if (pf.p == 2 && pf.e % 2 == 0) {
        // (2^(e/2), 0)
        mpz_ui_pow_ui(out[0].first, pf.p, pf.e / 2);
        mpz_set_ui(out[0].second, 0);
        return 1;
    } else if (pf.p == 2 && pf.e % 2 == 1) {
        // (2^(e/2), 2^(e/2)), e is odd so round down
        mpz_ui_pow_ui(out[0].first, pf.p, pf.e / 2);
        mpz_set(out[0].second, out[0].first);
        return 1;
    } else if (pf.p % 4 == 3 && pf.e % 2 == 0) {
        // (p^(e/2), 0)
        mpz_ui_pow_ui(out[0].first, pf.p, pf.e / 2);
        mpz_set_ui(out[0].second, 0);
        return 1;
    } else if (pf.p % 4 == 3 && pf.e % 2 == 1) {
        // N/A, no possible sums of squares
        return 0;
    } else { // All primes congruent to 1 mod 4
        pair_t *tmp1, *tmp2;
        pair_t base, rev;
        unsigned long i;

        tmp1 = (pair_t *)malloc((pf.e + 1) * sizeof(pair_t));
        tmp2 = (pair_t *)malloc((pf.e + 1) * sizeof(pair_t));
        pair_array_init(tmp1, pf.e + 1);
        pair_array_init(tmp2, pf.e + 1);
        pair_init(&base);
        pair_init(&rev);

        // Get the base pairs: sums of squares to the prime p
        primesumsquares(&base, pf.p);
        mpz_set(rev.first, base.second);
        mpz_set(rev.second, base.first);
        // Initialize the first element of each array to 'one'
        mpz_set_ui(out[0].first, 1);
        mpz_set_ui(out[1].second, 0);
        mpz_set_ui(tmp1[0].first, 1);
        mpz_set_ui(tmp1[1].second, 0);
        mpz_set_ui(tmp2[0].first, 1);
        mpz_set_ui(tmp2[1].second, 0);
        // Construct the rest of each array with powers of each base
        for (i = 1; i <= pf.e; i++) {
            diophantus(&tmp1[i], tmp1[i-1], base);
            diophantus(&tmp2[i], tmp2[i-1], rev);
        }
        // Combine the arrays
        for (i = 0; i <= pf.e; i++) {
            diophantus(&out[i], tmp1[i], tmp2[pf.e - i]);
        }

        pair_array_clear(tmp1, pf.e);
        pair_array_clear(tmp2, pf.e);
        free(tmp1);
        free(tmp2);
        pair_clear(&base);
        pair_clear(&rev);
        
        return pf.e + 1;
    }
}



/*
Find all pairs (a,b) such that a^2+b^2 equals the number represented
by the prime factorization pf. Store the pairs in out and return the
number of pairs found. This will always find the number of pairs identified
by countsumsquares(pf, pflen). This function produces *all* such pairs,
that is, negating an element or reversing the elements produces a different
pair.
*/
size_t getsumsquares(pair_t *out, const primefactor_t *pf, size_t pflen) {

}