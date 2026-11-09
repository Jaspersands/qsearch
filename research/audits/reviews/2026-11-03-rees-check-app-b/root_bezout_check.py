"""Exact checks of Lemma s3-root and of the Bezout step (eq. s3-bezout).

[R1] For every odd prime p <= PMAX and every pair rho1 != rho2, the number of delta with
     delta+rho1, delta+rho2 both nonzero and of unequal quadratic character is (p-1)/2.
[R2] For p <= 61, every kappa | p-1 with 2 <= kappa <= 8, every y in the kappa-th powers and
     every subset g of >= 2 roots of x^kappa - y: the fraction of delta in F_p for which
     gcd(g, (x+delta)^{(p-1)/2} - 1) is a proper factor is >= (p-1)/(2p).
[R3] The splitting procedure (polynomial arithmetic implemented here) returns a kappa-th root
     on every y for p in a list, kappa | p-1, with at most ceil(log2 kappa) splitting steps.
[R4] Bezout: for every prime p <= 400 and d <= 16, with kappa = gcd(d,p-1) and
     alpha d + beta (p-1) = kappa, every t != 0 gives (t^alpha)^d = t^kappa; and the image of
     x -> x^d on F_p^* is exactly the kappa-th powers.

Run: /opt/anaconda3/bin/python -I root_bezout_check.py
"""
import random
from math import gcd

PMAX = 401


def primes(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = [False] * len(s[i * i::i])
    return [i for i, v in enumerate(s) if v]


def chi(x, p):
    x %= p
    if x == 0:
        return 0
    return 1 if pow(x, (p - 1) // 2, p) == 1 else -1


fails = []
# [R1]
for p in primes(PMAX):
    if p == 2:
        continue
    ch = [chi(x, p) for x in range(p)]
    for diff in range(1, p):
        rho1, rho2 = diff, 0  # the count depends only on rho1 - rho2 (shift delta)
        cnt = sum(1 for dl in range(p)
                  if ch[(dl + rho1) % p] and ch[dl] and ch[(dl + rho1) % p] != ch[dl])
        if cnt != (p - 1) // 2:
            fails.append(("R1", p, diff, cnt))
print("[R1] done")


# polynomial helpers over F_p, coefficient lists low -> high
def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def pmod(a, b, p):
    a = a[:]
    inv = pow(b[-1], p - 2, p)
    while len(a) >= len(b):
        f = a[-1] * inv % p
        s = len(a) - len(b)
        for i, bi in enumerate(b):
            a[s + i] = (a[s + i] - f * bi) % p
        trim(a)
    return a


def pmul(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return trim(r)


def pdivexact(a, b, p):
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    inv = pow(b[-1], p - 2, p)
    while len(a) >= len(b) and a:
        f = a[-1] * inv % p
        s = len(a) - len(b)
        q[s] = f
        for i, bi in enumerate(b):
            a[s + i] = (a[s + i] - f * bi) % p
        trim(a)
    assert not a
    return trim(q)


def pgcd(a, b, p):
    a, b = trim(a[:]), trim(b[:])
    while b:
        a, b = b, pmod(a, b, p)
    inv = pow(a[-1], p - 2, p)
    return [x * inv % p for x in a]


def ppowmod(base, e, m, p):
    r = [1]
    base = pmod(base, m, p)
    while e:
        if e & 1:
            r = pmod(pmul(r, base, p), m, p)
        base = pmod(pmul(base, base, p), m, p)
        e >>= 1
    return r


def splits(g, delta, p):
    w = ppowmod([delta % p, 1], (p - 1) // 2, g, p)
    w = trim([(w[0] - 1) % p] + w[1:]) if w else [p - 1]
    g1 = pgcd(g, w, p) if w else g[:]
    return 0 < len(g1) - 1 < len(g) - 1, g1


# [R2]
from itertools import combinations
for p in primes(61):
    if p == 2:
        continue
    for kappa in range(2, 9):
        if (p - 1) % kappa:
            continue
        for y in {pow(x, kappa, p) for x in range(1, p)}:
            roots = [t for t in range(1, p) if pow(t, kappa, p) == y]
            assert len(roots) == kappa
            for k in range(2, kappa + 1):
                for sub in combinations(roots, k):
                    g = [1]
                    for r in sub:
                        g = pmul(g, [(-r) % p, 1], p)
                    good = sum(1 for dl in range(p) if splits(g, dl, p)[0])
                    if 2 * good * p < (p - 1) * p:  # good/p >= (p-1)/(2p)  <=> 2 good >= p-1
                        fails.append(("R2", p, kappa, y, sub, good))
print("[R2] done")


# [R3]
def extract_root(y, kappa, p, rng, R=200):
    g = [(-y) % p] + [0] * (kappa - 1) + [1]
    steps = 0
    while len(g) - 1 >= 2:
        for _ in range(R):
            ok, g1 = splits(g, rng.randrange(p), p)
            if ok:
                break
        else:
            raise RuntimeError("timeout")
        g2 = pdivexact(g, g1, p)
        g = g1 if len(g1) <= len(g2) else g2
        steps += 1
    return (-g[0]) % p, steps


rng = random.Random(20261103)
for p in (67, 73, 97, 151, 193, 257, 401, 1009, 65537):
    for kappa in range(2, 17):
        if (p - 1) % kappa:
            continue
        L = (kappa - 1).bit_length()  # ceil(log2 kappa)
        ys = {pow(rng.randrange(1, p), kappa, p) for _ in range(30)}
        for y in ys:
            t, steps = extract_root(y, kappa, p, rng)
            if pow(t, kappa, p) != y or steps > L:
                fails.append(("R3", p, kappa, y, t, steps))
print("[R3] done")


# [R4]
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


for p in primes(PMAX):
    if p == 2:
        continue
    for d in range(1, 17):
        kappa = gcd(d, p - 1)
        g, alpha, beta = egcd(d, p - 1)
        assert g == kappa and alpha * d + beta * (p - 1) == kappa
        imd = {pow(x, d, p) for x in range(1, p)}
        imk = {pow(x, kappa, p) for x in range(1, p)}
        h = (p - 1) // kappa
        if imd != imk or imk != {y for y in range(1, p) if pow(y, h, p) == 1}:
            fails.append(("R4-image", p, d))
        for t in range(1, p):
            s = pow(t, alpha % (p - 1), p)
            if pow(s, d, p) != pow(t, kappa, p):
                fails.append(("R4", p, d, t))
print("[R4] done")
print("failures:", len(fails))
for f in fails[:20]:
    print("FAIL", f)
