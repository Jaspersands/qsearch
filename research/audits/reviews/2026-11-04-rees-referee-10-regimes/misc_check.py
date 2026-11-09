import sys, itertools
from fractions import Fraction as Fr
from math import gcd, log2, ceil, log
sys.path.insert(0, '/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad')
from regimes_check import beta, ceil_log, lg, B_IS, ceil_log2_frac

eps = Fr(1, 3)
prof = [19, 17, 16, 14, 12, 9, 6, 3, 1]
gs = {i + 1: g for i, g in enumerate(prof)}

# 1. explicit choice of lem:fc-choice vs least arities
def explicit(p, k, g, tau):
    h = (p - 1) // k; q = Fr(h + 1, p)
    target = Fr(8) / (tau * q ** g)
    kk = 0; v = Fr(1)
    while v < target:
        v *= h; kk += 1
    n0 = 1 + kk
    M = n0 + g + ceil_log(p, Fr(2) / tau)
    assert beta(p, k, M, n0, g) <= tau
    return M

from regimes_check import least_fcs
for p in [11, 1031, 5281, 2**31-1, 2**61-1, 2**127-1]:
    c = 9; m = 19; S = m + ceil_log(p, Fr(9))
    n_l = 1; n_e = 1; diffs = []
    for d in range(2, c+1):
        k = gcd(d, p-1); g = gs[d]
        if k == 1:
            Ml = Me = g + 1
        else:
            Ml, _ = least_fcs(p, k, g, eps / (9*(c-1)*S*n_l))
            Me = explicit(p, k, g, eps / (9*(c-1)*S*n_e))
            diffs.append(Me - Ml)
        n_l *= Ml; n_e *= Me
    print('explicit vs least p bits=%d: dlogQ=%.2f arity diffs=%s' % (p.bit_length(), lg(n_e) - lg(n_l), diffs))

# 2. RC(ii) trial counts at u=18 at the six primes of app:fc-numbers(b)
u = 18; M = 4*u; B = ceil_log2_frac(Fr(64) * M**8)
print('B=', B)
for p in [5281, 105019, 2**31-1, 2**61-1, 194522647344910884721, 2**127-1]:
    kmax = max(gcd(d, p-1) for d in range(2, 10))
    print(' p=%d kmax=%d log2(4 k^M B)=%.1f' % (p.bit_length(), kmax, log2(4*B) + M*log2(kmax)), 'p>=16u^2', p >= 16*u*u)

# 3. x^r <= max(r^{2r}, 2^16, 2^x) for integer r>=1, real x>=1 (grid)
bad = []
for r in range(1, 60):
    x = 1.0
    while x < 4000:
        lhs = r*log2(x); rhs = max(2*r*log2(r) if r > 1 else 0, 16, x)
        if lhs > rhs + 1e-9: bad.append((r, x))
        x *= 1.001
print('x^r claim violations:', bad[:5], len(bad))

# 4. block-split example 69/325
p = 5; P = {1, 4}; D = {0, 1, 4}
num = 0; den = 0
F = range(p)
for l1 in itertools.product(F, F):
    for l2 in itertools.product(F, F):
        a1, a2 = l1[0], l2[0]
        acc = []
        for y in itertools.product(range(p), repeat=2):
            # acceptable per (F2)/(F3) on the 1x2 sub-bank [a1 a2]
            if a1 == 0 and a2 == 0:
                ok = y[0] in P and y[1] in P
            elif a1 != 0:
                R12 = a2 * pow(a1, -1, p) % p
                ok = y[1] in P and y[0] in D and (y[0] + R12 * y[1]) % p == 0
            else:
                ok = False  # n' = 0 < n0
            if ok: acc.append(y)
        if not acc: continue
        acc.sort()
        def z(y): return ((y[0]*l1[0] + y[1]*l2[0]) % p, (y[0]*l1[1] + y[1]*l2[1]) % p)
        good = [y for y in acc if z(y)[1] == 0]
        y = good[0] if good else acc[0]
        den += 1
        if z(y) == (0, 0): num += 1
print('block split example:', Fr(num, den), num, den)

# 5. g6 algebra: Jacobi, class, centralizer, ideal construction
import numpy as np
n = 6
br = {}
def setb(i, j, vec):
    br[(i, j)] = vec; br[(j, i)] = {k: -v for k, v in vec.items()}
for i in range(2, 6): setb(1, i, {i+1: 1})
setb(2, 3, {5: 1}); setb(2, 4, {6: 1}); setb(2, 5, {6: -1}); setb(3, 4, {6: 1})
def bracket(x, y):
    out = [0]*(n+1)
    for i in range(1, n+1):
        for j in range(1, n+1):
            if x[i] and y[j] and (i, j) in br:
                for k, v in br[(i, j)].items(): out[k] += x[i]*y[j]*v
    return out
def e(i):
    v = [0]*(n+1); v[i] = 1; return v
jac_ok = True
for a, b, c3 in itertools.product(range(1, n+1), repeat=3):
    s = [x+y+z for x, y, z in zip(bracket(e(a), bracket(e(b), e(c3))), bracket(e(b), bracket(e(c3), e(a))), bracket(e(c3), bracket(e(a), e(b))))]
    if any(s): jac_ok = False
print('g6 Jacobi over Z:', jac_ok)
# lower central series ranks over Q
import sympy
def span_rank(vs):
    if not vs: return 0
    return sympy.Matrix([v[1:] for v in vs]).rank()
gam = [e(i) for i in range(1, n+1)]
ranks = [span_rank(gam)]
for _ in range(7):
    gam = [bracket(e(i), g) for i in range(1, n+1) for g in gam]
    ranks.append(span_rank(gam))
print('g6 lower central ranks:', ranks)
