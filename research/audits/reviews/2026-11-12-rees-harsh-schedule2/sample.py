"""Random sample of primes p = 1 mod k in a range; prints them one per line (seeded)."""
import random, sys
from sympy import isprime
k, lo, hi, n, seed = map(int, sys.argv[1:6])
r = random.Random(seed)
out = set()
while len(out) < n:
    p = r.randrange(lo, hi)
    p -= (p - 1) % k
    if p > lo and isprime(p):
        out.add(p)
print('\n'.join(map(str, sorted(out))))
