import sys, math, itertools
sys.path.insert(0, '.')
import cert
from fractions import Fraction as Fr
coef = {}
def Edev(k, p, m, mode):
    if mode == 'theirs':
        return (1 - Fr(1, k ** (m - 1))) * (m - 1) * math.sqrt(p)
    if (k, m) not in coef:
        a = b = 0
        for r in itertools.product(range(k), repeat=m - 1):
            if not any(r): continue
            e = [(-sum(r)) % k] + list(r); l = sum(1 for x in e if x)
            a += l - 1; b += m - l
        coef[(k, m)] = (a / k ** (m - 1), b / k ** (m - 1))
    a, b = coef[(k, m)]
    return a * math.sqrt(p) + b
cert.Edev = Edev
k = 6
for mode in ('theirs', 'ref'):
    first = None; fails_after = []
    for p in range(18000, 40000):
        if p % k == 1 and cert.isprime(p):
            r, mM = cert.best(k, p, mode)
            if r > 1 and first is None: first = (p, mM, r)
            elif r <= 1 and first is not None: fails_after.append(p)
    print(mode, 'first certified', first, 'failures after first:', fails_after[:10], flush=True)
