#!/usr/bin/env python3

# Find primes p, such that if two squares' sum is 0 mod p^2,
# The only way that can happen is if both squares are also 0 mod p^2
# This is important because for such primes p,
# Center number == 0 mod p^2
# => Sum of each pair surrounding the center number == 0 mod p^2
# => Every number in the square == 0 mod p^2
# => square can be reduced

import math
import itertools

def is_prime(n):
    if n < 2:
        return False
    if (n == 2) or (n == 3):
        return True
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def quad_residues(mod):
    return {i**2 % mod for i in range(mod)}

def checkprime(p):
    qr = quad_residues(p**2)
    qr.remove(0)
    for i in qr:
        if (-i) % (p**2) in qr:
            return False
    return True


max = 100
primes = (p for p in range(max) if is_prime(p))

for p in primes:
    print(f"{p} ({p % 4}): {checkprime(p)}")

