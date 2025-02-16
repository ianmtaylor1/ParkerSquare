"""Module containing functions for factorizing numbers and learning about
sums of squares from factorizations."""

import math
import itertools
from functools import reduce
from operator import mul


class FactorException(Exception):
    pass

def _countup():
    """Generator of 2 and all odd integers"""
    yield 2
    n = 3
    while True:
        yield n
        n += 2

def isprime(n):
    """Return True if n is prime, False otherwise."""
    for p in _countup():
        if n % p == 0:
            return False
        elif p * p > n:
            return True

def primes():
    """Generator of all primes."""
    for n in _countup():
        if isprime(n):
            yield n


def factorize1mod4(n):
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
    """Return the prime factorization of n in the form of a dictionary of
    entries {p:e}, where p is a prime factor and e is the exponent it is
    raised to in the prime factorization."""
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


def _diophantus(pair1, pair2):
    """Given two pairs of integers, (a,b) and (p,q), such that
    a^2 + b^2 == n and p^2 + q^2 == m, return a pair of integers, 
    (x,y) such that x^2 + y^2 = m*n."""
    a,b = pair1
    p,q = pair2
    return (a*p+b*q),(a*q-b*p)


def _primesumsquares(p):
    """Given a prime p == 1 (mod 4), exhaustively look for a pair of
    integers (a,b), with 0 < a < b, such that a^2 + b^2 == p."""
    # Base cases:
    if p < 2:
        raise FactorException("Got non-prime.")
    elif p == 2:
        return (1,1)
    elif p % 4 == 3:
        return None
    # Look exhaustively, return a pair when found
    a = 1
    asquared = 1
    b = math.isqrt(p - asquared)
    bsquared = b * b
    nfound = 0
    while asquared < bsquared:
        if asquared + bsquared == p:
            return (a,b)
        elif asquared + bsquared > p:
            b -= 1
            bsquared -= b + b + 1
        elif asquared + bsquared < p:
            a += 1
            asquared += a + a - 1
    # Error: above algorithm should always find a pair
    raise FactorException(f"Algorithm did not find pair (a,b) for {p}")


def _primepowersumsquares(p, e):
    """Find the ways the nubmer p^e can be written as the sum
    of two squares, where p is a prime and e >= 1. Does not check
    whether p is prime."""
    if (p % 4 == 3):
        return set()
    a,b = _primesumsquares(p)
    basepairs = {(a,b),(-a,b),(a,-b),(-a,-b),(b,a),(-b,a),(b,-a),(-b,-a)}
    pairs = basepairs
    # Iterate up the powers using Diophantus's identity
    for _ in range(2, e+1):
        pairs = {_diophantus(x,y) for x,y in itertools.product(pairs, basepairs)}
    return pairs


def getsumsquares(factors):
    """Given the prime factorization of a positive integer, return all pairs of
    integers (a,b) such that a^2 + b^2 = n. a and b can be zero or negative,
    and (a,b) is distinct from (b,a)."""
    # Building up from 1 using each prime power in the factorization, apply
    # Diophantus's identity to each combination of sums of squares building
    # up to n.
    pairs = {(0,1),(1,0),(0,-1),(-1,0)}
    for p,e in factors.items():
        if (p % 4 == 1):
            fpairs = _primepowersumsquares(p,e)
            pairs = {_diophantus(x,y) for x,y in itertools.product(pairs, fpairs)}
        elif (p % 4 == 3) and (e % 2 == 1):
            pairs = set()
            break
        elif (p % 4 == 3) and (e % 2 == 0):
            scale = p ** (e // 2)
            pairs = {(a * scale, b * scale) for a,b in pairs}
    # Compare the number produced to the expected number (Jacobi)
    if len(pairs) != countsumsquares(factors):
        raise FactorException("Failed to produce all pairs.")
    return pairs


def getnum(factors):
    """Recompute the original number represented by this prime factorization."""
    if len(factors) == 0:
        return 1
    else:
        return reduce(mul, (p**e for p,e in factors.items()))


