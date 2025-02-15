#!/usr/bin/env python3

import math
import itertools
from functools import reduce
from operator import mul

def check_factorize(n):
    """Check if the prime factorization of a number n contains only odd primes
    congruent to 1 mod 4. If yes, return the prime factorization of n in the
    form of a dictionary {p:e} where p is each prime factor and e is the
    exponent it is raised to in the prime factorization. If no, return None"""
    if n % 2 == 0:
        return None
    i = 3
    factors = {}
    while i*i <= n:
        if n % i == 0:
            if i % 4 == 1:
                factors[i] = factors.get(i, 0) + 1
                n //= i
            else:
                return None
        else:
            i += 2
    if n > 1:
        if n % 4 == 1:
            factors[n] = factors.get(n, 0) + 1
        else:
            return None
    return factors


def factorize(n):
    """Return the prime factorization of n in the
    form of a dictionary {p:e} where p is each prime factor and e is the
    exponent it is raised to in the prime factorization."""
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2,0) + 1
        n //= 2
    i = 3
    while i*i <= n:
        if n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        else:
            i += 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def countsumsquares(factors):
    """Given the prime factorization of a number, return the number of
    ways in which it can be expressed as the sum of two squares. This is
    based on Jacobi's two-square theorem. The count includes all pairs (a,b)
    such that a^2 + b^2 = n, including some that may be considered
    equivalent. i.e. a pair (a,b) with a != b will be counted 8 times:
    (a,b), (-a,b), (a,-b), (-a,-b), (b,a), (-b,a), (b,-a), (-b,-a)."""
    ways = 4
    for p, e in factors.items():
        if (p % 4 == 3) and (e % 2 == 1):
            return 0
        elif (p % 4 == 1):
            ways *= e + 1
    return ways


def getsumsquares(n, stopafter = None):
    """Find all unique ways n can be the sum of two squares of positive
    integers. Return a list of tuples (a,b) with 0 < a < b such that a and b
    are square numbers and a + b = n. Note: this will not return cases when n
    is square, a = 0 and b = n, and cases when n is twice a square and a = b.
    If the number of expected pairs is known, that can be supplied in
    'stopafter' for a slight improvement in time, stopping the search early.
    """
    if stopafter is None:
        stopafter = n # Guaranteed to be less than n values
    pairs = []
    a = 1
    asquared = 1
    b = math.isqrt(n - asquared)
    bsquared = b * b
    nfound = 0
    while (asquared < bsquared) and (nfound < stopafter):
        if asquared + bsquared == n:
            pairs.append((asquared,bsquared))
            nfound += 1
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


def diophantus(pair1, pair2):
    a,b = pair1
    p,q = pair2
    return (a*p+b*q),(a*q-b*p)


def primepowersumsquares(p, e):
    """Find the ways the nubmer p^e can be written as the sum
    of two squares, where p is a prime and e >= 1. Does not check
    whether p is prime."""
    if (p % 4 == 3):
        return set()
    if (p == 2):
        a,b = 1,1
    else:
        a2,b2 = getsumsquares(p)[0]
        a,b = math.isqrt(a2),math.isqrt(b2)
    basepairs = {(a,b),(-a,b),(a,-b),(-a,-b),(b,a),(-b,a),(b,-a),(-b,-a)}
    pairs = basepairs
    # Iterate up the powers using Diophantus's identity
    for _ in range(2, e+1):
        pairs = {diophantus(x,y) for x,y in itertools.product(pairs, basepairs)}
    return pairs


def fact2sumsquares(factors):
    pairs = {(0,1),(1,0),(0,-1),(-1,0)}
    for p,e in factors.items():
        if (p % 4 == 1):
            fpairs = primepowersumsquares(p,e)
            pairs = {diophantus(x,y) for x,y in itertools.product(pairs, fpairs)}
        elif (p % 4 == 3) and (e % 2 == 1):
            return set()
    return pairs

def fact2num(factors):
    if len(factors) == 0:
        return 1
    else:
        return reduce(mul, (p**e for p,e in factors.items()))


for n in range(1,100001):
    factors = factorize(n)
    ways = countsumsquares(factors)
    pairs = fact2sumsquares(factors)
    if n != fact2num(factors):
        print(f"{n} - factorization failed.")
    if ways != len(pairs):
        print(f"{n} - Count does not match.")


#for prime in [2,5,13,17,29]:
#    for power in [1,2,3,4,5,6,7]:
#        sums = primepowersumsquares(prime, power)
#        if any(a*a+b*b != prime**power for a,b in sums):
#            print("Sums don't add up?")
#        print(f"{prime}^{power}: {len(sums)}, {sums}\n\n")
