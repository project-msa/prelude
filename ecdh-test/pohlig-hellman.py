from sage.all import *
from sage.groups.generic import *

def factorise(n):
    primes_list = ecm.factor(n)
    primes = {}

    for i in primes_list:
        if i in primes:
            primes[i] += 1
        else:
            primes[i] = 1
    
    return list(primes.items())

def pohlig_hellman(G, B):
    group_order = G.order()
    primes = factorise(group_order)
    dlp = [0] * len(primes)

    decomposition = []
    for i, (p_i, e_i) in enumerate(primes):
        for j in range(e_i):
            dlp[i] += bsgs(G * (group_order // p_i), (B - G * dlp[i]) * (group_order // (p_i ** (j + 1))), (0, p_i - 1), operation='+') * p_i ** j

    return crt(dlp, [p_i ** e_i for (p_i, e_i) in primes])

""" test1
p = 65537
E = EllipticCurve(GF(p), [0, 7])
G = E.gens()[0]

import random
a = random.randint(1, p - 1)
B = a * G
dlog = pohlig_hellman(G, B)

print(f"a = {a} and computed dlog = {dlog}")
"""