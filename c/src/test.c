#define TESTING
#include <stdio.h>

#include <gmp.h>

#include "primes.h"
#include "squares.h"
#include "search.h"

/* primes.c tests */

void test_tovalue() {
    primefactor_t factors[5] = {{2,5}, {3,2}, {5,1}, {11,2}, {41,7}};
    mpz_t value;
    mpz_init(value);
    tovalue(value, factors, 5);
    printf(    "Expected: 33933984681025440\n");
    gmp_printf("Value:    %Zd\n", value);
    mpz_clear(value);
}

void test_tostring() {
    primefactor_t factors[5] = {{2,5}, {3,2}, {5,1}, {11,2}, {41,7}};
    char repr[100];
    tostring(repr, 100, factors, 5);
    printf("Expected:       2^5 * 3^2 * 5^1 * 11^2 * 41^7\n");
    printf("Representation: %s\n", repr);
}

void test_enumerate() {
    unsigned long i;
    unsigned long p = 0;
    printf("Primes below 20: 2, 3, 5, 7, 11, 13, 17, 19, \n");
    printf("Using isprime:   ");
    for (i = 0; i < 20; i++) {
        if (isprime(i)) {
            printf("%lu, ", i);
        }
    }
    printf("\n");
    printf("Using nextprime: ");
    for (i=0; i < 8; i++) {
        p = nextprime(p);
        printf("%lu, ", p);
    }
    printf("\n");
    printf("Primes between 1000 and 1050: 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, \n");
    printf("Using isprime:                ");
    for (i = 1000; i < 1050; i++) {
        if (isprime(i)) {
            printf("%lu, ", i);
        }
    }
    printf("\n");
    printf("Using nextprime:              ");
    p = 1000;
    for (i=0; i < 8; i++) {
        p = nextprime(p);
        printf("%lu, ", p);
    }
    printf("\n");
}

void testprimes() {
    printf("\n*** Testing prime number functions.\n");
    test_tovalue();
    test_tostring();
    test_enumerate();
}

/* squares.c tests */

void test_countss() {
    primefactor_t factors1[5] = {{2,5}, {3,2}, {5,1}, {11,2}, {41,7}};
    primefactor_t factors2[5] = {{2,5}, {3,3}, {5,1}, {11,2}, {41,7}};
    printf("Expected count:    64\n");
    printf("countsumsquares(): %lu\n", countsumsquares(factors1, 5));
    printf("Expected count:    0\n");
    printf("countsumsquares(): %lu\n", countsumsquares(factors2, 5));
}

void test_primess() {
    pair_t out;
    unsigned long primes[7] = {2, 3, 5, 11, 13, 1009, 1019};
    unsigned long expected[7][2] = {{1, 1}, {0, 0}, {1, 2}, {0, 0}, {2, 3}, {15, 28}, {0, 0}};
    int i;
    pair_init(&out);
    for (i = 0; i < 7; i++) {
        unsigned long p = primes[i];
        unsigned long exp[2] = {expected[i][0], expected[i][1]};
        size_t res = primesumsquares(&out, p);
        printf("Prime: %lu\n", primes[i]);
        if (p % 4 == 3) {
            printf("Expected: 0\n");
            printf("Found:    %lu\n", res);
        } else {
            printf(    "Expected: %lu^2 + %lu^2 = %lu\n", exp[0], exp[1], p);
            gmp_printf("Found:    %Zd^2 + %Zd^2 = %lu\n", out.first, out.second, p);
        }
    }
}

void test_primepowerss() {
    pair_t out[100]; // intentionally oversized
    primefactor_t primepowers[9] = {{2,0}, {3,0}, {5,0}, {2, 5}, {2, 6}, {11, 1}, {11, 2}, {13, 5}, {13,6}};
    size_t expected[9] = {1, 1, 1, 1, 1, 0, 1, 6, 7};
    pair_array_init(out, 100);
    for (int i = 0; i < 9; i++) {
        unsigned int j;
        size_t count = primepowersumsquares(out, primepowers[i]);
        printf("Prime power %lu^%lu:\n", primepowers[i].p, primepowers[i].e);
        printf("Expected: %lu\nCount:   %lu\n", expected[i], count);
        for (j = 0; j < count; j++) {
            mpz_t sum;
            mpz_init_set_ui(sum, 0);
            mpz_addmul(sum, out[j].first, out[j].first);
            mpz_addmul(sum, out[j].second, out[j].second);
            gmp_printf("%Zd = (%Zd)^2 + (%Zd)^2\n", sum, out[j].first, out[j].second);
            mpz_clear(sum);
        }
    }
    pair_array_clear(out, 100);
}

void test_getss() {
    primefactor_t factors1[4] = {{2, 1}, {3, 2}, {5, 3}, {13, 1}};
    pair_t out[100]; // intentionally oversized
    size_t count;
    pair_array_init(out, 100);
    count = countsumsquares(factors1, 4);
    getsumsquares(out, factors1, 4);
    printf("Expected: 32 sums to 29250\n");
    for (size_t j = 0; j < count; j++) {
        mpz_t sum;
        mpz_init_set_ui(sum, 0);
        mpz_addmul(sum, out[j].first, out[j].first);
        mpz_addmul(sum, out[j].second, out[j].second);
        gmp_printf("%Zd = (%Zd)^2 + (%Zd)^2\n", sum, out[j].first, out[j].second);
        mpz_clear(sum);
    }
}

void testsquares() {
    printf("\n*** Testing sum of squares functions.\n");
    test_countss();
    test_primess();
    test_primepowerss();
    test_getss();
}

/* Run all tests */

int main() {
    printf("Hello world! From test.\n");
    testprimes();
    testsquares();
}