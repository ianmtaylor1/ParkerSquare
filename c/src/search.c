// This file contains the code to search through the pairs of squares 
// surrounding the middle number of a magic square and see if they can
// be assembled into a magic square of squares
#include <stddef.h>
#include <gmp.h>

#include "primes.h"
#include "squares.h"
#include "search.h"

/*
Given the prime factorization of the square root of the 
*/
int constructsquare(
    mpz_t *square,
    const primefactor_t *rootmidfac, size_t numfac,
    const pair_t *outerpairs, size_t numpairs)
{
    return 0;
}

/*
For a number n with a prime factorization represented by 'in', with length 
'len', store in 'out' the prime factorization of 2m^2. 'out'should point 
to an array with length len + 1, because if n has no 2's in its factorization
then 'out' will be one longer. Otherwise, out will have the same length. 
Return the length of 'out': len if n already contains 2's, n+1 otherwise.
*/
int twice_squared(primefactor_t *out, const primefactor_t *in, size_t len) {
    bool twofound = false;
    /* double the exponents, add one if p == 2 */
    for (size_t i = 0; i < len; i++) {
        out[i].p = in[i].p;
        out[i].e = in[i].e * 2;
        if (out[i].p == 2) {
            out[i].e++;
            twofound = true;
        }
    }
    /* Add a 2 if one wasn't already there */
    if (twofound) {
        return len;
    } else {
        out[len].p = 2;
        out[len].e = 1;
        return len + 1;
    }
}

/*
For an array of pair_t, square the values of each pair and
filter to unique pairs, with the smaller value first. Store the new pairs
in the same array, and pair_array_clear the remainder of the array. Return
the new size of the array.
*/
size_t square_filter(pair_t *pairs, size_t len) {
    size_t store = 0;
    for (size_t get = 0; get < len; get++) {
        // Only operate if 0 < a < b for a pair (a,b)
        if (mpz_sgn(pairs[get].first) > 0 && mpz_cmp(pairs[get].first, pairs[get].second) < 0) {
            // mpz functions work fine with the same argument as src and dest
            mpz_pow_ui(pairs[store].first, pairs[get].first, 2);
            mpz_pow_ui(pairs[store].second, pairs[get].second, 2);
            store++;
        }
    }
    // Clear the remainder of the array
    pair_array_clear(pairs + store, len - store);
    return store;
}

/*
Find a parker square whose middle number's square root is given by the prime
factorization rootmidfac, with numfac factors. Store the square, if it exists,
in 'square', which should point to an array of mpz_t with length 9. The square
will be stored in row-major order. The return value will be nonzero if any
interesting squares are found. 
*/
int findparkersquare(
    mpz_t *square, 
    const primefactor_t *rootmidfac, size_t numfac)
{
    primefactor_t *pairsum;
    size_t pairsumlen;
    pair_t *borderpairs;
    size_t numpairs;
    int found;

    // get sum for pairs that surround middle number
    pairsum = (primefactor_t *)malloc((numfac + 1) * sizeof(primefactor_t));
    pairsumlen = twice_squared(pairsum, rootmidfac, numfac);

    // get pairs that surround middle number
    // start with "raw" pairs
    numpairs = countsumsquares(pairsum, pairsumlen);
    borderpairs = (pair_t *)malloc(numpairs * sizeof(pair_t));
    pair_array_init(borderpairs, numpairs);
    getsumsquares(borderpairs, pairsum, pairsumlen);
    // square the pairs and filter to just strictly ordered
    numpairs = square_filter(borderpairs, numpairs);
    
    // Assemble pairs into square
    found = constructsquare(square, rootmidfac, numfac, borderpairs, numpairs);

    // Free allocated memory
    pair_array_clear(borderpairs, numpairs);
    free(borderpairs);
    free(pairsum);

    return found;
}