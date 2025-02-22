#!/usr/bin/env python3

import gmpy2
import timeit
import math

# Fibonacci test

def fib(n):
    a = 1
    b = 1
    for i in range(3, n+1):
        a,b = b, a+b
    return b

def fib_gmpy(n):
    a = gmpy2.mpz(1)
    b = gmpy2.mpz(1)
    for i in range(3, n+1):
        a,b = b, a+b
    return b

print("Fibonacci test")
N = 10000
reps = 1000
print("gmpy2:   ", timeit.timeit(lambda: fib_gmpy(N), number = reps))
print("builtin: ", timeit.timeit(lambda: fib(N), number = reps))

# is_square test

def is_square(n):
    return (n >= 0) and (pow(math.isqrt(n), 2) == n)

def is_square_gmpy(n):
    return (n >= 0) and (gmpy2.isqrt(n) ** 2 == n)

def check_squares(n):
    x = 1
    numsquares = 0
    for i in range(n):
        numsquares += is_square(x)
        x = 2 * x + n

def check_squares_gmpy(n):
    x = gmpy2.mpz(1)
    numsquares = 0
    for i in range(n):
        numsquares += is_square_gmpy(x)
        x = 2 * x + n

def check_squares_gmpy_builtin(n):
    x = gmpy2.mpz(1)
    numsquares = 0
    for i in range(n):
        numsquares += gmpy2.is_square(x)
        x = 2 * x + n

def check_squares_gmpy_converted(n):
    x = 1
    numsquares = 0
    for i in range(n):
        numsquares += gmpy2.is_square(x)
        x = 2 * x + n

print("Square checking test")
N = 10000
reps = 100
print("gmpy2:           ", timeit.timeit(lambda: check_squares_gmpy(N), number = reps))
print("gmpy2 builtin:   ", timeit.timeit(lambda: check_squares_gmpy_builtin(N), number = reps))
print("gmpy2 converted: ", timeit.timeit(lambda: check_squares_gmpy_converted(N), number = reps))
print("builtin:         ", timeit.timeit(lambda: check_squares(N), number = reps))

