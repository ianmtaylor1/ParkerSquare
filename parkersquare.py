#!/usr/bin/env python3

import math
import itertools
from datetime import datetime
import timeit

import gmpy2

import factors


###############################################################################

def distfromsquare(n):
    """Return the distance from a number n to the nearest square."""
    if n < 0:
        return abs(n)
    root = gmpy2.isqrt(n)
    sqbelow = root ** 2
    err = n - sqbelow
    if err <= root:
        return int(err)
    else:
        return int(2 * root + 1 - err)


###############################################################################


def _getsumsquares_direct(n):
    """Find all unique ways n can be the sum of two squares of positive
    integers. Return a list of tuples (a,b) with 0 < a < b such that
    a^2 + b^2 = n. Note: this will not return cases when n
    is square, a = 0 and b^2 = n, and cases when n is twice a square and a = b.
    """
    pairs = []
    a = 1
    asquared = 1
    b = math.isqrt(n - asquared)
    bsquared = b * b
    while asquared < bsquared:
        if asquared + bsquared == n:
            pairs.append((a,b))
            a += 1
            asquared += a + a - 1
            b -= 1
            bsquared -= b + b + 1
        elif asquared + bsquared > n:
            b -= 1
            bsquared -= b + b + 1
        elif asquared + bsquared < n:
            a += 1
            asquared += a + a - 1
    return pairs


def getsumsquares(fac):
    """Given the prime factorization of a number, n, find all pairs of 
    square numbers A = a^2 and B = b^2 where 0 < A < B and A + B = n."""
    try:
        pairs_sqrt = factors.getsumsquares(fac)
    except factors.FactorException:
        print(f"Falling back to slow sum of squares enumeration for {factors.tostring(fac)}", flush=True)
        pairs_sqrt = _getsumsquares_direct(factors.getnum(fac))
    return [(a**2, b**2) for a,b in pairs_sqrt if (0 < a) and (a < b)]


###############################################################################

def getbestsquare(pairs):
    """Check if a magic square can be constructed from the given
    pairs of numbers (a,b) such that a and b are square numbers
    and a + b = n for a common n. Return the "best" square as measured
    by fewest non-square elements
    """
    # Find out what the common sum of the square would be
    total = (pairs[0][0] + pairs[0][1]) * 3 // 2
    middle = total // 3
    if not gmpy2.is_square(middle):
        raise Exception("Center number not square")
    # Pick two pairs to make up the corners of the magic square.
    # Due to reflectional and rotational symmetry, it doesn't matter in which
    # order we place the pairs
    besterror = (4, total)
    bestsquare = None
    for corners1,corners2 in itertools.combinations(pairs, 2):
        # See if the three pairs can fit into the corners and let the other
        # spaces be also filled with squares
        square = [[corners1[0], 0, corners2[0]],
                  [0, middle, 0],
                  [corners2[1], 0, corners1[1]]]
        # Try to fill the missing numbers
        square[0][1] = total - square[0][0] - square[0][2]  # top
        square[2][1] = total - square[2][0] - square[2][2]  # bottom
        square[1][0] = total - square[0][0] - square[2][0]  # left
        square[1][2] = total - square[0][2] - square[2][2]  # right
        # Calculate the error
        nummissing = 4
        totalerror = 0
        # top
        if gmpy2.is_square(square[0][1]):
            nummissing -= 1
        else:
            totalerror += distfromsquare(square[0][1])
        # bottom
        if gmpy2.is_square(square[2][1]):
            nummissing -= 1
        else:
            totalerror += distfromsquare(square[2][1])
        # left
        if gmpy2.is_square(square[1][0]):
            nummissing -= 1
        else:
            totalerror += distfromsquare(square[1][0])
        # right
        if gmpy2.is_square(square[1][2]):
            nummissing -= 1
        else:
            totalerror += distfromsquare(square[1][2])
        if (nummissing, totalerror) < besterror:
            besterror = (nummissing, totalerror)
            bestsquare = square
    return besterror, bestsquare


###############################################################################

def getborderpairs(fac):
    """For a number m representing the square root of the central value
    of the Parker square, passed to this function in terms of its prime
    factorization, find the possible pairs of squares to surround
    the center value. These are the unique ways two squares can add to
    2*m^2, if four such unique ways exist. If they exist, return a list
    of tuples of all these pairs. If they don't exist, return None. If
    the only pairs of such squares would all have a common factor with
    m^2, then skip."""
    # Adjust the prime factorization to be for 2m^2
    fac = {p:2*e for p,e in fac.items()}
    fac[2] = fac.get(2, 0) + 1
    numways = (factors.countsumsquares(fac) - 4) // 8 # remove irrelevant pairs
    if numways < 4:
        return None
    # If there theoretically are 4 pairs, find them
    pairs = getsumsquares(fac)
    if len(pairs) != numways:
        raise Exception(f"Expected {numways} pairs, got {len(pairs)}")
    return pairs


def square_sqrt(square):
    return [[math.isqrt(n) for n in row] for row in square]

def count_forever(start):
    while True:
        yield start
        start += 1

def _tobase(n, b):
    """Convert a number n to its base b representation, expressed as a
    tuple of base b digits from least significant to most significant."""
    if n == 0:
        return (0,)
    digits = []
    while n > 0:
        digits.append(n % b)
        n //= b
    return tuple(digits)

def count_by_primes():
    """Generator that will count over tuples of increasing length representing
    the exponents in the prime factorization of positive integers. Will count
    every integer exactly once and reach every integer eventually. Exponents go
    smallest prime to largest. Each tuple is assumed to have an infinite string
    of zeros after it for exponents of all other primes."""
    # Count every 'base' digit, base 'base' number, skipping representations
    # that are equivalent to the ones already seen
    for base in count_forever(2):
        for num in range(base ** base):
            rep = _tobase(num, base)
            rep = rep + (0,) * (base - len(rep))
            if (base > 2) and (rep[base-1] == 0) and all(rep[i] < base - 1 for i in range(base-1)):
                continue
            yield rep


def iter_middle():
    """Iterate over candidate square roots of middle numbers of the magic,
    i.e., numbers with only primes congruent to 1 mod 4 in their prime
    factorization. Yield the prime factorizations directly."""
    primes = (p for p in factors.primes() if p % 4 == 1)
    cachedprimes = []
    for exponents in count_by_primes():
        while len(cachedprimes) < len(exponents):
            cachedprimes.append(next(primes))
        yield {p:e for p,e in zip(cachedprimes, exponents) if e > 0}


def search():
    """Search for Parker Squares by enumerating prime factorizations of
    the square root of the central number. Will return immediately if
    a Parker Square is found, otherwise, will loop forever."""
    #Iterators of primes
    primes = (p for p in factors.primes() if p % 4 == 1)
    cachedprimes = []
    
    besterror = (5,0)
    bestsquare = None
    for count,fac in enumerate(iter_middle()):
        # See if there are at least 4 pairs of squares that sum to 2m^2
        pairs = getborderpairs(fac)
        if pairs is not None:
            (nummissing, totalerror),square = getbestsquare(pairs)
            if nummissing == 0:
                print(
                    "*******************",
                    "** PARKER SQUARE **",
                    "*******************", 
                    f" {square}\n {square_sqrt(square)}", 
                    sep="\n", flush=True
                )
                return square
            # Report progress so far
            if (nummissing, totalerror) < besterror:
                besterror = (nummissing, totalerror)
                bestsquare = square
                print(f"#{count+1}: {factors.tostring(fac)} = {factors.getnum(fac)},",
                      flush = True)
                print("New Best:", f"{bestsquare}", 
                      f"Non-squares = {nummissing}, Total error = {totalerror}",
                      sep="\n", flush=True)
            elif (count + 1) % 100 == 0:
                print(f"#{count+1}", flush=True)

###############################################################################

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('search()')
    search()


