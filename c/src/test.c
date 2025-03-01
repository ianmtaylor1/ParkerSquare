#include <stdio.h>

#include <gmp.h>

#include "primes.h"
#include "squares.h"
#include "search.h"

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

int main() {
    printf("Hello world! From test.\n");
    testprimes();
}