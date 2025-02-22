"""Module containing functions for factorizing numbers and learning about
sums of squares from factorizations."""

import math
import itertools
import functools
import operator


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
        if p * p > n:
            return True
        elif n % p == 0:
            return False


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
    factors = {}
    tocheck = _countup()
    i = next(tocheck)
    while i*i <= n:
        if n % i == 0:
            if i % 4 == 1:
                factors[i] = factors.get(i, 0) + 1
                n //= i
            else:
                return None
        else:
            i = next(tocheck)
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
    tocheck = _countup()
    i = next(tocheck)
    while i*i <= n:
        if n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        else:
            i = next(tocheck)
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
    return (a*p-b*q),(a*q+b*p)


@functools.lru_cache(maxsize = None)
def _primesumsquares(p):
    """Given a prime p == 1 (mod 4), exhaustively look for a pair of
    integers (a,b), with 0 < a < b, such that a^2 + b^2 == p. Will
    return exactly one pair."""
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


@functools.lru_cache(maxsize = None)
def _primepowersumsquares(p, e):
    """Find the ways the nubmer p^e can be written as the sum
    of two squares, where p is a prime and e >= 1. Does not check
    whether p is prime. Will return all pairs up to multiplication
    by a unit."""
    # Base cases
    if e == 0:
        return[(1,0)]
    elif (p % 4 == 3) and (e % 2 == 1):
        return []
    elif (p % 4 == 3) and (e % 2 == 0):
        return [(p ** (e // 2),0)]
    elif (p == 2) and (e % 2 == 1):
        return [(2 ** (e // 2), 2 ** (e // 2))]
    elif (p == 2) and (e % 2 == 0):
        return [(2 ** (e // 2), 0)]
    # Find the base pair for the prime
    a,b = _primesumsquares(p)
    # Create lists of powers of that pair
    powers = [(1,0)] + [None] * e
    reversepowers = [(1,0)] + [None] * e
    for i in range(1, e + 1):
        powers[i]        = _diophantus((a,b), powers[i-1])
        reversepowers[i] = _diophantus((b,a), reversepowers[i-1])
    # Combine lists pairwise with one in reverse order
    pairs = [_diophantus(x,y) for x,y in zip(powers, reversed(reversepowers))]
    # Check that this procedure produced the correct number of pairs
    if len(pairs) != (e + 1):
        raise FactorException("Failed to produce all pairs.")
    return pairs

def _associates(pairs):
    """Given a list of pairs of integers, returns a list four times as long
    with all 'associates' of those pairs. i.e. if the pairs (a,b) represent
    complex numbers a + bi, this function returns all pairs multiplied by the
    complex units: 1, i, -1, and -i."""
    units = [(1,0),(0,1),(-1,0),(0,-1)]
    return [_diophantus(x,y) for x,y in itertools.product(units, pairs)]

def getsumsquares(factors):
    """Given the prime factorization of a positive integer, return all pairs of
    integers (a,b) such that a^2 + b^2 = n. a and b can be zero or negative,
    and (a,b) is distinct from (b,a)."""
    # Building up from 1 using each prime power in the factorization, apply
    # Diophantus's identity to each combination of sums of squares building
    # up to n.
    pairs = [(1,0)]
    for p,e in factors.items():
        if (p % 4 == 1) or (p == 2):
            fpairs = _primepowersumsquares(p,e)
            pairs = [_diophantus(x,y) for x,y in itertools.product(pairs, fpairs)]
        elif (p % 4 == 3) and (e % 2 == 1):
            pairs = []
            break
        elif (p % 4 == 3) and (e % 2 == 0):
            scale = p ** (e // 2)
            pairs = [(a * scale, b * scale) for a,b in pairs]
    # Complete by finding all associates
    pairs = _associates(pairs)
    # Compare the number produced to the expected number (Jacobi)
    if len(pairs) != countsumsquares(factors):
        raise FactorException("Failed to produce all pairs.")
    return pairs


def getnum(factors):
    """Recompute the original number represented by this prime factorization."""
    if len(factors) == 0:
        return 1
    else:
        return functools.reduce(operator.mul, (p**e for p,e in factors.items()))


def tostring(factors):
    """Prints the prime factorization in a nice readable format."""
    components = [f"{p}^{e}" for p,e in sorted(factors.items()) if e > 0]
    if len(components) > 0:
        return " * ".join(components)
    else:
        return "1"
