#!/usr/bin/env python3

import math
import itertools

checkmod = 144
#checkmod = 5184

# Calculate the possible residuals for squares and sums of squares in the given mod
squareresids = {(i ** 2) % checkmod for i in range(checkmod)}
sumsquareresids = {(i + j) % checkmod for i,j in itertools.combinations_with_replacement(squareresids, 2)}
# For each sum of squares residual, find all square residuals that could contribute to it
candidatesquareresids = {
    x:{i for i in squareresids if (x - i) % checkmod in squareresids} 
    for x in sumsquareresids
}
candidateresids = {
    x:{i for i in range(checkmod) if (i**2) % checkmod in candidatesquareresids[x]}
    for x in sumsquareresids
}

print(squareresids)
print(sumsquareresids)
print(candidatesquareresids)
print(candidateresids)
for x in candidateresids:
    print(f"{x}: {len(candidateresids[x])/checkmod}")

print(2450 % checkmod in sumsquareresids)
