# Check Cor 3: direct difference-set test vs cyclotomic A(u,v) criterion, two generators, pigeonhole, Weil (iii).
import sys, math
from sympy import primerange, primitive_root
from common import setup

def direct(p, k, ind):
    # S_b = Q0° - Qb°  ⊇ F_p^x for all b != 0 ?
    bad = []
    for b in range(1, k):
        X = [0] + [x for x in range(1, p) if ind[x] == 0]
        Y = [0] + [y for y in range(1, p) if ind[y] == b]
        S = set((x - y) % p for x in X for y in Y)
        if any(z not in S for z in range(1, p)):
            bad.append(b)
    return bad

def Acrit(p, k, ind):
    e = ind[p-1]
    A = [[0]*k for _ in range(k)]
    for w in range(2, p):
        A[ind[w]][ind[w-1]] += 1
    P = [(u, v) for u in range(k) for v in range(k) if u != 0 and v != e and u != v]
    zero = [(u, v) for (u, v) in P if A[u][v] == 0]
    dev = max(abs(k*k*A[u][v] - (p-2)) for u in range(k) for v in range(k))
    return zero, len(P), e, dev

def W2(k):
    a = (k-1)*(k-2); c = 3*(k-1)
    s = (a + math.sqrt(a*a + 4*(2 + c))) / 2   # s^2 - a s - (2+c) > 0
    return s*s

out = []
for k in range(3, 13):
    w2 = W2(k)
    lim = int(w2) + 1
    E = []; Edir = []; Ealt = []
    for p in primerange(3, lim + 1):
        if (p - 1) % k: continue
        ind, g = setup(p, k)
        zero, nP, e, dev = Acrit(p, k, ind)
        bound = 3*(k-1) + (k-1)*(k-2)*math.sqrt(p)
        assert dev <= bound + 1e-9, (k, p, dev, bound)
        if p - 2 > bound: assert not zero, (k, p)
        nP_formula = (k-1)*(k-2) if e == 0 else k*k - 3*k + 3
        assert nP == nP_formula
        if p <= k*k - 3*k + 3: assert zero, ("pigeonhole fails", k, p)
        d = direct(p, k, ind) if p < 1200 else None
        if d is not None:
            assert (len(d) > 0) == (len(zero) > 0), ("Cor3(1) equivalence fails", k, p, d, zero)
        # second generator: g^u with u another unit mod k
        units = [u for u in range(2, k) if math.gcd(u, k) == 1]
        if units:
            gen2 = pow(g, units[-1], p) * pow(g, k, p) % p
            ind2, _ = setup(p, k, gen2)
            z2, _, _, _ = Acrit(p, k, ind2)
            assert (len(z2) > 0) == (len(zero) > 0), ("generator dependence", k, p)
        if zero: E.append(p)
    out.append(f"k={k} W2(real)={w2:.2f} E2row={E}")
print("\n".join(out))
