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

}

void testsquares() {
    printf("\n*** Testing sum of squares functions.\n");
    test_countss();
    test_primess();
    test_primepowerss();
}

/* Run all tests */

int main() {
    printf("Hello world! From test.\n");
    testprimes();
    testsquares();
}