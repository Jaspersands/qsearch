"""Brute-force two-level contractions and check the Stepanov polynomial F.

Normalisation: beta_0 = 0, alpha_0 = 1 (translation + Q_0 scaling).
xi = primitive root g, Q_m = {x : log_g x = m mod kappa}, zeta = g^h.
Usage: python stepanov_check.py kappa pmax [max_report]
"""
import sys
from collections import Counter
from math import comb

def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

def prim_root(p):
    fac = []
    n = p - 1; d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g

def contractions(p, k, g):
    h = (p - 1) // k
    lg = {}
    x = 1
    for e in range(p - 1):
        lg[x] = e % k; x = x * g % p
    def cls(x):  # None for 0
        return None if x % p == 0 else lg[x % p]
    def inQo(x, m):
        c = cls(x); return c is None or c == (m % k)
    # beta_i candidates: beta_0=0 ; beta_i+1 in Qo_{-i}
    bc = [[0]] + [[b for b in range(p) if inQo(b + 1, -i)] for i in range(1, k)]
    ac = [[1]] + [[a for a in range(p) if inQo(a, -j)] for j in range(1, k)]
    # masks over candidate index lists
    def mask(j, a, i):
        m = 0
        for t, b in enumerate(bc[i]):
            if inQo(a + b, -(i + j)): m |= 1 << t
        return m
    out = []
    def dfs(j, alph, masks):
        if j == k:
            # enumerate beta products
            lists = [[bc[i][t] for t in range(len(bc[i])) if masks[i] >> t & 1] for i in range(k)]
            def rec(i, bet):
                if i == k:
                    out.append((tuple(alph), tuple(bet))); return
                for b in lists[i]:
                    rec(i + 1, bet + [b])
            rec(0, [])
            return
        for a in ac[j]:
            nm = [masks[i] & mask(j, a, i) for i in range(k)]
            if all(nm):
                dfs(j + 1, alph + [a], nm)
    init = [(1 << len(bc[i])) - 1 for i in range(k)]
    init = [init[i] & mask(0, 1, i) for i in range(k)]
    if all(init):
        dfs(1, [1], init)
    return out, cls

def polymul_lin_pow(a, N, p):
    # coefficients of (x+a)^N, index = degree
    return [comb(N, s) * pow(a, N - s, p) % p for s in range(N + 1)]

def mult(coeffs, b, p):
    # multiplicity of root b of polynomial (coeff list low->high)
    c = coeffs[:]
    while len(c) > 1 and c[-1] == 0: c.pop()
    if all(v == 0 for v in c): return None
    m = 0
    while True:
        # synthetic division by (x-b)
        n = len(c) - 1
        if n < 0: break
        q = [0] * n
        r = c[n]
        for d in range(n - 1, -1, -1):
            q[d] = r
            r = (c[d] + r * b) % p
        if r != 0 or n == 0: break
        m += 1; c = q
    return m

def check(p, k, alpha, beta, cls, g):
    h = (p - 1) // k
    zeta = pow(g, h, p)
    # cell checks
    for i in range(k):
        for j in range(k):
            v = (alpha[j] + beta[i]) % p
            c = cls(v)
            assert c is None or c == (-(i + j)) % k
            if v: assert pow(v, h, p) == pow(zeta, (-(i + j)) % k, p)
    assert (alpha[0] + beta[0]) % p
    assert len(set(alpha)) == k and len(set(beta)) == k
    m = k - 1; N = h + m - 1
    c = []
    for j in range(k):
        pr = 1
        for jj in range(k):
            if jj != j: pr = pr * (alpha[j] - alpha[jj]) % p
        c.append(pow(pr, p - 2, p))
    for s in range(k - 1):
        assert sum(c[j] * pow(alpha[j], s, p) for j in range(k)) % p == 0
    F = [0] * (N + 1)
    for j in range(k):
        w = c[j] * pow(zeta, j, p) % p
        for s, v in enumerate(polymul_lin_pow(alpha[j], N, p)):
            F[s] = (F[s] + w * v) % p
    deg = max(d for d in range(N + 1) if F[d])
    zeros_rows = [i for i in range(k) if any((alpha[j] + beta[i]) % p == 0 for j in range(k))]
    z = sum(1 for i in range(k) for j in range(k) if (alpha[j] + beta[i]) % p == 0)
    orders = []
    for i in range(k):
        o = mult(F, beta[i] % p, p)
        want = m - 1 if i in zeros_rows else m
        assert o >= want, (p, alpha, beta, i, o, want)
        if i in zeros_rows: assert o == m - 1, (o, m)
        orders.append(o)
    total = sum(orders)
    assert k * (k - 1) - z <= total <= deg <= N
    return dict(z=z, deg=deg, N=N, orders=tuple(orders), total=total)

if __name__ == "__main__":
    k = int(sys.argv[1]); pmax = int(sys.argv[2])
    for p in range(k + 1, pmax + 1):
        if not is_prime(p) or (p - 1) % k: continue
        g = prim_root(p)
        cons, cls = contractions(p, k, g)
        h = (p - 1) // k
        if not cons:
            print(f"kappa={k} p={p} h={h}: no contraction (E_2)"); continue
        zc = Counter(); slack = Counter(); tight = 0; ordc = Counter()
        for (a, b) in cons:
            r = check(p, k, a, b, cls, g)
            zc[r['z']] += 1
            slack[(r['z'], r['N'] - r['total'], r['deg'])] += 1
            ordc[r['orders']] += 1
        bound_ok = all(k * (k - 1) - z <= h + k - 2 for z in zc)
        print(f"kappa={k} p={p} h={h}: {len(cons)} normalised contractions; z-dist={dict(zc)}; "
              f"(z, N-sum_orders, degF) dist={dict(slack)}; orders={dict(ordc)}; bound_ok={bound_ok}")
        sys.stdout.flush()
