from sage.all import *
from sage.rings import * 

def bsgs(a, b, bounds):
    Z = integer_ring.ZZ
    lb, ub = bounds
    if lb < 0 or ub < lb:
        raise ValueError("bsgs() requires 0<=lb<=ub")

    ran = 1 + ub - lb
    mult = lambda x, y: x ** y
    inverse = lambda x: x ** -1

    c = inverse(b) *  mult(a, lb)

    if ran < 30:    # use simple search for small ranges
        d = c
        # for i,d in multiples(a,ran,c,indexed=True,operation=operation):
        for i0 in range(ran):
            i = lb + i0
            if d == 1:        # identity == b^(-1)*a^i, so return i
                return Z(i)
            d = a * d
        raise ValueError("no solution in bsgs()")

    m = isqrt(ran) + 1  # we need sqrt(ran) rounded up
    table = {}       # will hold pairs (a^(lb+i),lb+i) for i in range(m)

    d = c
    for i0 in xsrange(m):
        i = lb + i0
        if d == 1:        # identity == b^(-1)*a^i, so return i
            return Z(i)
        table[d] = i
        d = d * a

    c = c * inverse(d)    # this is now a**(-m)
    d = 1
    for i in xsrange(m):
        j = table.get(d)
        if j is not None:  # then d == b*a**(-i*m) == a**j
            return Z(i * m + j)
        d = c * d

    raise ValueError("log of %s to the base %s does not exist in %s" % (b, a, bounds))

""" test 1
p = 17
F = GF(p)
g = F(3)

for i in range(p):
    a = F(i)
    b = g ** a 
    print(f"for a = {a}, computed discrete log = {bsgs(g, b, (0, p - 1))}")
"""

""" test 2

p = 65537
F = GF(p)
g = F(3)

for i in range(135, 2136):
    a = F(i)
    b = g ** a 

    dlog = bsgs(g, b, (0, p - 1))
    if a != int(dlog):
        print(f"mismatch found on a = {a}")
"""