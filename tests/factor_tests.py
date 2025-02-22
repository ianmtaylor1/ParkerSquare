import factors

NUMTESTS=100

for n in range(1, NUMTESTS+1):
    fac = factors.factorize(n)
    numss = factors.countsumsquares(fac)
    pairs = factors.getsumsquares(fac)
    print(f"{n} = {factors.tostring(fac)}, \t{numss} sums of squares")
    assert n == factors.getnum(fac)
    assert numss == len(pairs)
    assert len(pairs) == len(set(pairs))
    assert all(a**2 + b**2 == n for a,b in pairs)

