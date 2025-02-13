#!/usr/bin/env python3

import math
import itertools
from datetime import datetime
import timeit

###############################################################################

def is_square(n):
    """Returns true or false if n is a square integer."""
    return (math.isqrt(n) ** 2 == n)

###############################################################################

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
    factors = check_factorize(m)
    if factors is None:
        return None
    for p in factors.keys():
        if (p == 2) or (p % 4 == 3):
            return None
    factors = {p:2*e for p,e in factors.items()}
    factors[2] = factors.get(2, 0) + 1
    numways = (countsumsquares(factors) - 4) // 8 # remove irrelevant pairs
    if numways < 4:
        return None
    # If there theoretically are 4 pairs, find them
    pairs = getsumsquares(2 * m * m, stopafter = numways)
    if len(pairs) != numways:
        raise Exception(f"Expected {numways} pairs, got {len(pairs)}")
    return pairs

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

def square_sqrt(square):
    return [[math.isqrt(n) for n in row] for row in square]

def count_forever(start):
    while True:
        yield start
        start += 1

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
    search(1, report = 10**5)


