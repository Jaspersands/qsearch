"""Small exact checks: Lemma lem:bezout conversion, example counts, base-d vs base-kappa exponent,
the SUM remark, and Fermat-curve point counts behind the Weil threshold.
Run: nice -n 19 /opt/anaconda3/bin/python misc_checks.py
"""
import itertools, math
from math import gcd, ceil, log2
import numpy as np
from sympy import primerange
from exponents import t_min

rng = np.random.default_rng(7)

# 1. Lemma bezout: x -> x^u turns kappa-solutions into d-solutions with the same support
bad = 0; cnt = 0
for p in primerange(3, 60):
    for d in range(1, 10):
        k = gcd(d, p - 1)
        # u >= 0 with u d = k mod (p-1)
        u = next(u for u in range(0, p - 1 if p > 2 else 2) if (u * d - k) % (p - 1) == 0) if True else None
        for trial in range(30):
            M = 5; a = 2
            lam = rng.integers(0, p, (M, a))
            x = rng.integers(0, p, M)
            # force sum x^k lam = 0 by adjusting: just test the identity s^d = x^k for every x
            s = np.array([0 if xi == 0 else pow(int(xi), u, p) for xi in x])
            cnt += 1
            if any((pow(int(si), d, p) - (0 if xi == 0 else pow(int(xi), k, p))) % p for si, xi in zip(s, x)):
                bad += 1
            if any((si == 0) != (xi == 0) for si, xi in zip(s, x)):
                bad += 1
print("1. bezout conversion: tests=%d failures=%d" % (cnt, bad))

# 2. class-3 example claim (Section example-class3): at p = 7 the five labels
#    (0,1),(1,0),(1,2),(1,4),(3,1) admit only s = 0 for sum s_i^3 lambda_i = 0.
p = 7
labs = [(0, 1), (1, 0), (1, 2), (1, 4), (3, 1)]
sols = [s for s in itertools.product(range(p), repeat=5) if any(s) and all(sum(pow(si, 3, p) * l[j] for si, l in zip(s, labs)) % p == 0 for j in range(2))]
print("2. p=7 five-label cubic example: nonzero solutions =", len(sols))
#    stage two: labels e_i and -nu e_i, nu nonsquare, admit only s = 0 for quadratics
for p in (5, 7, 11):
    nu = next(v for v in range(2, p) if pow(v, (p - 1) // 2, p) == p - 1)
    L6 = [tuple(int(i == j) for j in range(3)) for i in range(3)] + [tuple((-nu * (i == j)) % p for j in range(3)) for i in range(3)]
    sols = [s for s in itertools.product(range(p), repeat=6) if any(s) and all(sum(si * si * l[j] for si, l in zip(s, L6)) % p == 0 for j in range(3))]
    print("   p=%d six-label quadratic example: nonzero solutions = %d" % (p, len(sols)))
#    Heisenberg remark: three labels always admit a nonzero solution of sum s_i^2 lambda_i = 0
for p in (3, 5, 7, 11):
    ok = all(any(any(s) and sum(si * si * l for si, l in zip(s, lab)) % p == 0 for s in itertools.product(range(p), repeat=3)) for lab in itertools.product(range(p), repeat=3))
    print("   p=%d: every 3 scalar labels admit a nonzero quadratic witness: %s" % (p, ok))

# 3. SUM remark: SUM(|chi_a>|chi_b>) = |chi_{a-b}>|chi_b>, p = 5, a = 1, b = 4
p = 5; om = np.exp(2j * np.pi / p)
chi = lambda a: np.array([om ** (a * x) for x in range(p)]) / math.sqrt(p)
st = np.kron(chi(1), chi(4))
out = np.zeros(p * p, complex)
for x in range(p):
    for y in range(p):
        out[x * p + (x + y) % p] += st[x * p + y]
print("3. SUM remark holds:", np.allclose(out, np.kron(chi(1 - 4), chi(4))))

# 4. exponent of the "shorter zero sums" variant if the base stayed G(d, g_d) (as in B_d) instead of G(kappa_d, g_d)
def Ld(k, p):
    return 1 if k == 1 else ceil(log2(t_min(k, p)))
best = (0, None)
for p in primerange(11, 6000):
    e = 1 + sum(d * Ld(gcd(d, p - 1), p) for d in range(2, 10))
    if e > best[0]:
        best = (e, p)
print("4. c=9 exponent with base G(d,.) and L_d = ceil(log2 t_d): max over 11<=p<6000 is %d at p=%d" % best)
best = (0, None)
for p in primerange(11, 6000):
    e = 1 + sum(gcd(d, p - 1) * Ld(gcd(d, p - 1), p) for d in range(2, 10))
    if e > best[0]:
        best = (e, p)
print("   with base G(kappa_d,.) (Schedule 1 runs IS at degree kappa_d): max %d at p=%d" % best)
#    the theorem's own arity B_d at each prime vs B_{kappa_d}: exponent with standard depth at base kappa
best = (0, None)
for p in primerange(11, 6000):
    e = 1 + sum((lambda k: k * ceil(log2(k + 1)) if k > 1 else 1)(gcd(d, p - 1)) for d in range(2, 10))
    best = max(best, (e, p))
print("   standard depth at base kappa_d (B_{kappa_d}): max %d at p=%d (theorem charges B_d: 145)" % best)

# 5. Fermat curve x^k+y^k+z^k=0 projective point counts vs Weil, and points with a zero coordinate
viol = []
for k in (2, 4, 6, 8):
    for p in primerange(3, 400):
        if (p - 1) % k:
            continue
        P = {}
        kp = [pow(x, k, p) for x in range(p)]
        N = 0; Nzero = 0
        # projective points: normalise first nonzero coordinate to 1
        pts = [(1, y, z) for y in range(p) for z in range(p)] + [(0, 1, z) for z in range(p)] + [(0, 0, 1)]
        for (x, y, z) in pts:
            if (kp[x] + kp[y] + kp[z]) % p == 0:
                N += 1
                if 0 in (x, y, z):
                    Nzero += 1
        g2 = (k - 1) * (k - 2)
        if abs(N - (p + 1)) > g2 * math.sqrt(p) + 1e-9 or Nzero > 3 * k:
            viol.append((k, p, N, Nzero))
        if ((p - 1) // k) % 2 == 1 and Nzero:
            viol.append(("zero-coord point although -1 not a k-th power", k, p))
print("5. Weil bound / zero-coordinate count violations (k in 2,4,6,8; p<400):", viol)
