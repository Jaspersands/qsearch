"""Exact checks of the counting steps of App. tb-counts and Cor. fpt-r / codim.
AI-checked, pending human review.  Exact integer/rational arithmetic where it matters.
"""
from fractions import Fraction
from math import comb, ceil, log, log2, floor, gcd
from itertools import combinations_with_replacement
from sympy import primerange, isprime
from sympy.utilities.iterables import partitions

def clog(x):
    return (x - 1).bit_length()

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# 1. superadditivity of phi(x) = x (x+t) (x+1)^(E-1)
phi = lambda x, t, E: x * (x + t) * (x + 1) ** (E - 1)
for E in (1, 2, 5, 11, 23, 38, 143):
    for t in range(0, 30):
        for a in range(0, 25):
            for b in range(0, 25):
                check(phi(a, t, E) + phi(b, t, E) <= phi(a + b, t, E), ("superadd", E, t, a, b))
print("1. phi superadditive on integer grid: ok" if ok else "1. FAIL")

# 2. (i) chain: sum_p phi(n_p) <= phi(L) <= (L+t)(L+1)^E, and the exponent-p chain
for E in (5, 11, 23):
    for t in range(0, 15):
        for L in range(1, 13):
            for part in partitions(L):
                ns = [k for k, m in part.items() for _ in range(m)]
                s = sum(phi(n, t, E) for n in ns)
                check(s <= phi(L, t, E) <= (L + t) * (L + 1) ** E, ("chain", E, t, ns))
                s1 = sum((n + t) * (n + 1) ** (E - 1) for n in ns)
                check(s1 <= 2 ** E * (L + t) * (L + 1) ** (E - 1), ("exp-p chain", E, t, ns))
                # Lemma tb-count-prime: sum_j Qcore(n-j) <= n Qcore(n)
                for n in ns:
                    Q = lambda m: (m + t) * (m + 1) ** (E - 1)
                    check(sum(Q(n - j) for j in range(n)) <= n * Q(n), ("count-prime", n))
print("2. (i) summation chains on all partitions L<=12: ok" if ok else "2. FAIL")

# 3. K_c and log2(9 K_9)
K = 1
for d in range(2, 10):
    K *= d ** (d * (d - 1) * clog(d + 1) // 2)  # d(d-1) even, so exact
print("3. log2(9 K_9) = %.2f (paper: about 1206)" % (log2(9) + sum(d * (d - 1) * clog(d + 1) / 2 * log2(d) for d in range(2, 10))))

# 4. Hoeffding vote: R = ceil(18 ln(1/eps)) runs, each correct w.p. >= 2/3;
#    exact binomial tail Pr[X <= R/2] at success prob exactly 2/3 (worst case).
def tail(R, q=Fraction(2, 3)):
    return sum(comb(R, j) * q ** j * (1 - q) ** (R - j) for j in range(0, R // 2 + 1))
worst = 0.0
for eps in [0.33, 0.3, 0.2, 0.1, 0.05, 0.01, 1e-3, 1e-4, 1e-6]:
    R = ceil(18 * log(1 / eps))
    tl = tail(R)
    check(tl <= eps, ("hoeffding", eps))
    check(float(tl) <= __import__("math").exp(-R / 18) + 1e-15, ("hoeffding2", eps))
    worst = max(worst, float(tl) / eps)
    R2 = ceil(18 * log(2 / eps))  # codim appendix
    check(tail(R2) <= eps / 2, ("hoeffding codim", eps))
print("4. Hoeffding vote: exact tails below eps (max tail/eps = %.3g)" % worst)

# 5. Cor fpt-r(i) inequalities.
#  (a) log2(4 alpha c) <= alpha for alpha = (1+2log2 c) r + 3 log2(216 c S) + 3
for c in range(2, 200):
    for r in range(max(1, c - 1), c + 40):  # c <= r+1
        for S in (2, 3, 10, 10**3, 10**6, 10**12):
            alpha = (1 + 2 * log2(c)) * r + 3 * log2(216 * c * S) + 3
            check(log2(4 * alpha * c) <= alpha, ("log2(4 alpha c)", c, r, S))
#  (b) x^r <= max(r^(2r), 2^16, 2^x), integers r>=1, reals x>=1 (grid)
for r in range(1, 60):
    for i in range(0, 4000):
        x = 1 + i * 0.05
        lhs = r * log2(x)
        rhs = max(2 * r * log2(r) if r > 1 else 0.0, 16.0, x)
        check(lhs <= rhs + 1e-12, ("x^r", r, x))
#  (c) induction M_d <= alpha + 3 log2 n_d with M_d chosen at the bound gives
#      log2 n_d <= (d-2) log2(4 alpha c) and M_d <= (1+3c) alpha <= 4 alpha c
for c in range(2, 40):
    for r in (c - 1, c, 2 * c):
        for S in (2, 50, 10**6):
            alpha = (1 + 2 * log2(c)) * r + 3 * log2(216 * c * S) + 3
            ln = 0.0
            for d in range(2, c + 1):
                M = alpha + 3 * ln
                check(ln <= (d - 2) * log2(4 * alpha * c) + 1e-9, ("induct n_d", c, d))
                check(M <= (1 + 3 * c) * alpha + 1e-9 and M <= 4 * alpha * c, ("induct M", c, d))
                ln += log2(M)
print("5. Cor fpt-r(i) inequalities: ok" if ok else "5. FAIL")

#  (d) Lemma fc-choice: beta(M, n0; g) <= tau and the size bound, exact rationals
def beta(M, n0, a, p, kap):
    h = (p - 1) // kap
    q = Fraction(h + 1, p)
    return Fraction(4) / (Fraction(h) ** (n0 - 1) * q ** a) + Fraction(p ** a - 1, (p - 1) * p ** (M - n0))
def choice(g, p, kap, tau):
    h = (p - 1) // kap
    q = Fraction(h + 1, p)
    target = Fraction(8) / tau / q ** g
    k = 0
    while Fraction(h) ** k < target:
        k += 1
    j = 0
    while p ** j < Fraction(2) / tau:
        j += 1
    n0 = 1 + k
    return n0 + g + j, n0
cnt = 0
for p in list(primerange(5, 200)) + [1031, 5281]:
    for kap in sorted({gcd(d, p - 1) for d in range(2, 12)}):
        if kap < 2 or kap >= p - 1:
            continue
        for g in (1, 3, 8, 19):
            for tau in (Fraction(1, 3), Fraction(1, 1000), Fraction(1, 10**9)):
                M, n0 = choice(g, p, kap, tau)
                check(beta(M, n0, g, p, kap) <= tau, ("fc-choice beta", p, kap, g, tau))
                bound = g * (1 + 2 * log(kap) / log(p / kap)) + 3 * log(8 / tau) / log(p / kap) + 3
                check(M <= bound + 1e-9, ("fc-choice size", p, kap, g, tau, M, bound))
                cnt += 1
print("5d. Lemma fc-choice on %d cases: ok" % cnt if ok else "5d. FAIL")

# 6. Prop tb-count-gates(d)/(b): k <= 2 Lambda / log2 p and b_M <= 2 e log2 p
for ell in range(2, 400, 7):
    for p in primerange(3, 2 ** min(ell, 20)):
        if log2(p) > ell:
            break
        for epsinv in (3, 10**3, 10**9):
            eps = 1 / epsinv
            k = floor(ell / log2(p)) + ceil(log(8 * ell / eps) / log(p) - 1e-12)
            Lam = ell + log2(8 * ell / eps)
            check(k <= 2 * Lam / log2(p) + 1e-9, ("k bound", ell, p, epsinv))
        for e in range(1, max(2, int(ell / log2(p))) + 1):
            bM = clog(p ** e)
            check(bM <= 2 * e * log2(p), ("bM bound", p, e))
print("6. k <= 2 Lambda/log2 p and b_M <= 2 e log2 p: ok" if ok else "6. FAIL")

# 7. Counterexample to "O_c(n_p(2b_M+A_c)) = O_c(ell)" in Prop tb-count-gates(a):
#    G = C_{3^e} x (C_3)^e, abelian (class 1 < 3), minimal ell = ceil(log2 |G|).
print("7. per-query multiplications vs ell for G = C_{3^e} x C_3^e:")
for e in (5, 10, 20, 40, 80):
    n = 2 * e
    ell = clog(3 ** n)
    m_cyc = e + 1                     # cyclic factors = chart basis size m
    bM = clog(3 ** e)
    lower = 4 * m_cyc * 2 * bM        # >= 4 m (2 b_M) even with A_c = 0
    print("   e=%3d ell=%4d  4m(2b_M) = %6d  ratio to ell = %.1f  ratio to ell^2 = %.3f"
          % (e, ell, lower, lower / ell, lower / ell ** 2))

# 8. Counterexample to "then k >= n" in Lemma tb-chart: G = C_{3^20}, s = 1, d = 1.
p, n, ell, eps = 3, 20, 32, Fraction(1, 3)
assert 3 ** 20 < 2 ** 32
delta = eps / (4 * ell)
t = min(1, floor(ell / log2(p))) + ceil(log(float(2 / delta)) / log(p))
print("8. C_{3^20}, ell=32, eps=1/3: Lemma tb-kernel sample count t = %d < n = %d" % (t, n))
check(t < n, "k>=n counterexample")
print("ALL OK" if ok else "SOME CHECK FAILED")
