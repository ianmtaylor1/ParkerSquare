#!/usr/bin/env python3

import itertools

#mods = range(2, 2 ** 16 + 1)

maxmod = 2**16

bestratio = 1.0
bestmod = 1

for mod in range(2, maxmod + 1):
    squareresids = {(i ** 2) % mod for i in range(mod)}
    ratio_lb = len(squareresids) / mod
    if ratio_lb < bestratio: # Only continue if there's a chance
        sumsquareresids = {(i + j) % mod for i,j in itertools.combinations_with_replacement(squareresids, 2)}
        ratio = len(sumsquareresids) / mod
        if ratio < bestratio:
            bestratio = ratio
            bestmod = mod
            print(f"{bestmod}: {bestratio}")



