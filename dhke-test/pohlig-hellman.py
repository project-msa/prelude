from sage.all import *
from sage.groups.generic import *  ## both work
from bsgs import bsgs  ## both work 

def factorise(n):
    primes_list = ecm.factor(n)
    primes = {} 

    for i in primes_list:
        if i in primes:
            primes[i] += 1
        else:
            primes[i] = 1
        
    return list(primes.items())

def pohlig_hellman(p, g, b):
    group_order = p - 1
    primes = factorise(p - 1)
    dlp = [0] * (len(primes))

    decomposition = []
    for i, (p_i, e_i) in enumerate(primes):
        for j in range(e_i):
            dlp[i] += bsgs(g ** (group_order // p_i), (b * g ** (-dlp[i])) ** (group_order // (p_i ** (j + 1))), (0, p_i - 1)) * p_i ** j
            
    return crt(dlp,[p_i ** e_i for (p_i, e_i) in primes])

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