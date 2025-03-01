#include <stdio.h>

#include <gmp.h>

#include "primes.h"
#include "squares.h"
#include "search.h"

void testprimes() {
    printf("\n*** Testing prime number functions.\n");
    {
        primefactor_t factors[5] = {{2,5}, {3,2}, {5,1}, {11,2}, {41,7}};
        mpz_t value;
        char repr[100];
        mpz_init(value);
        tostring(repr, 100, factors, 5);
        tovalue(value, factors, 5);
        gmp_printf("Value: %Zd\n", value);
        printf("Representation: %s\n", repr);
        mpz_clear(value);
    }
}

int main() {
    printf("Hello world! From test.\n");
    testprimes();
}