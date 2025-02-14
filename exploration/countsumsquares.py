#!/usr/bin/env python3

def factorize(n):
    """Return the prime factorization of n in the form of a dictionary
    {p:e} where p is each prime factor and e is the exponent it is raised
    to in the prime factorization."""
    i = 2
    factors = {}
    while i*i <= n:
        if n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        else:
            i += 1
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

start = 30000000
end =   30100000

for i in range(start, end + 1):
    factors = factorize(i)
    factors = {k:2*v for k,v in factors.items()}
    factors[2] = factors.get(2, 0) + 1
    ways = countsumsquares(factors)
    ways = (ways - 4) // 8
    if ways >= 4:
        print(f"2*{i}^2 = {2*i**2}: {ways}")


