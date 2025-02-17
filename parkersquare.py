#!/usr/bin/env python3

import math
import itertools
from datetime import datetime
import timeit

import factors

###############################################################################

def is_square(n):
    """Returns true or false if n is a square integer."""
    return (math.isqrt(n) ** 2 == n)

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
        pairs_sqrt = _getsumsquares_direct(factors.getnum(fac))
    return [(a**2, b**2) for a,b in pairs_sqrt if (0 < a) and (a < b)]


###############################################################################

def partialsquares(pairs):
    """Check if a magic square can be constructed from the given
    pairs of numbers (a,b) such that a and b are square numbers
    and a + b = n for a common n.
    Iterate through all squares in the form of 3x3 lists representing
    the magic square in row-major order.
    'pairs' is a list of at least 4 tuples of integers that have a common sum.
    """
    # Pick three pairs to make up the top and bottom row of the magic square.
    # We can show that the small number in the column pair must be smaller
    # than the small number of both corner pairs. Further, due to reflectional
    # symmetry, we can arbitrarily decide that the top left corner of the
    # square is smaller than the top right corner of the pair, and that the
    # smaller of each corner pair is in the top row
    for column,corners1,corners2 in itertools.combinations(sorted(pairs), 3):
        # See if the three pairs can fit into the diagonals and center column,
        # i.e., if they can be placed there such that the top and
        # bottom row sum to the same value. Because we've oriented the corners
        # such that the smaller number is on top, we know that if a pair works
        # it must have its larger value on the top row
        toprowsum    = corners1[0] + column[1] + corners2[0]
        bottomrowsum = corners2[1] + column[0] + corners1[1]
        if toprowsum == bottomrowsum:
            square = [[corners1[0], column[1], corners2[0]],
                      [0, 0, 0],
                      [corners2[1], column[0], corners1[1]]]
            yield square

def finishsquare(square):
    """Given a partially completed magic square,
    fill in the rest if possible. If possible, return the completed square.
    If not possible, return None.
    'square' is a 3x3 array in row-major order. The top and bottom rows are
    finished and the middle row is unfinished. The top and bottom rows must
    sum to the same total"""
    total = sum(square[0])
    works = True
    for col in range(3):
        candidate = total - square[0][col] - square[2][col]
        if is_square(candidate):
            square[1][col] = candidate
        else:
            works = False
    return works, square

###############################################################################

def getborderpairs(m):
    """For a number m representing the square root of the central value
    of the Parker square, find the possible pairs of squares to surround
    the center value. These are the unique ways two squares can add to
    2*m^2, if four such unique ways exist. If they exist, return a list
    of tuples of all these pairs. If they don't exist, return None. If
    the only pairs of such squares would all have a common factor with
    m^2, then skip."""
    # Quick(er) check based on prime factorization of m
    if (m % 4 != 1):
        return None
    fac = factors.factorize1mod4(m)
    if fac is None:
        return None
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


def search(start, end=None, report=None):
    """Search for Parker Squares whose center number is m^2, for m from
    'start' to 'end', inclusive. Report progress every 'report' values
    of m. Will return immediately if a Parker square is found, otherwise,
    will return None after 'end' is reached."""
    if report is None:
        if end is not None:
            report = 10 ** (math.floor(math.log10(end - start + 1)) - 1)
        else:
            report = 10 ** 4
    
    starttimer = timeit.default_timer()
    qssfound = 0
    searchspace = count_forever(start) if end is None else range(start, end + 1)
    for middle in searchspace:
        pairs = getborderpairs(middle)
        if pairs is not None:
            qssfound += 1
            for ps in partialsquares(pairs):
                found, square = finishsquare(ps)
                if found:
                    print(f"*******************\n** PARKER SQUARE **\n*******************\n{square}\n{square_sqrt(square)}", flush=True)
                    return square
                else:
                    print(f"Candidate square:\n {square}\n {square_sqrt(square)}", flush=True)
        if middle % report == 0:
            currenttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            currenttimer = timeit.default_timer()
            elapsed = round((currenttimer - starttimer) / 60, 1)
            print(f"{currenttime} ({elapsed} minutes) middle number: {middle}^2 = {middle * middle}, QSS found: {qssfound}/{report}", flush=True)
            qssfound = 0
    return None

###############################################################################

if __name__ == '__main__':
    start = 1
    search(start, end = None, report = 10**6)


