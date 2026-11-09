"""Lemma tb-sylow(c) edge cases, Lemma tb-kernel span bound, and the numbers
quoted in Remark tb-scope and thm:bb-envelope.

(1) p <= c: exponent of G_p can exceed the largest generator order.
    D_8 = <two reflections> (p=2,c=2) and C_3 wr C_3 = <(012),(036)(147)(258)>
    (p=3,c=3) as permutation groups.
(2) Exact P[t uniform vectors fail to span F_p^k] vs the bound p^{k-t} and
    t = k + ceil(log_p(2/delta)) => <= delta/2.
(3) Witt sums, d(4,9) = 40584, 9*143 = 1287, Schedule-1 exponent 145 at c=9,
    log2(9 K_9), superadditivity of x(x+t)(x+1)^{E-1}.
"""
from fractions import Fraction
from math import ceil, log, log2, gcd

def perm_mul(a, b):  # apply a then b
    return tuple(b[a[i]] for i in range(len(a)))

def closure(gens):
    idp = tuple(range(len(gens[0])))
    S, fr = {idp}, [idp]
    while fr:
        nf = []
        for s in fr:
            for g in gens:
                t = perm_mul(s, g)
                if t not in S:
                    S.add(t); nf.append(t)
        fr = nf
    return S

def order(g):
    idp, x, n = tuple(range(len(g))), g, 1
    while x != idp:
        x = perm_mul(x, g); n += 1
    return n

def lcs_class(G):
    idp = tuple(range(len(next(iter(G)))))
    inv = {g: next(h for h in G if perm_mul(g, h) == idp) for g in G}
    cur, cls = set(G), 0
    while cur != {idp}:
        cls += 1
        comm = {perm_mul(perm_mul(inv[g], inv[h]), perm_mul(g, h)) for g in G for h in cur}
        cur = closure(list(comm)) if comm - {idp} else {idp}
    return cls

def from_cycles(n, cycles):
    p = list(range(n))
    for c in cycles:
        for i, x in enumerate(c):
            p[x] = c[(i + 1) % len(c)]
    return tuple(p)

print("(1) Lemma tb-sylow(c) needs p > c:")
D8 = [from_cycles(4, [(1, 3)]), from_cycles(4, [(0, 1), (2, 3)])]
G = closure(D8)
print(f"  D8: |G|={len(G)} class={lcs_class(G)} gen orders={[order(g) for g in D8]} exponent={max(order(g) for g in G)}")
W = [from_cycles(9, [(0, 1, 2)]), from_cycles(9, [(0, 3, 6), (1, 4, 7), (2, 5, 8)])]
G = closure(W)
print(f"  C3 wr C3: |G|={len(G)} class={lcs_class(G)} gen orders={[order(g) for g in W]} exponent={max(order(g) for g in G)}")

print("(2) Lemma tb-kernel span bound:")
worst = 0
for p in (2, 3, 5, 7, 11):
    for k in range(0, 9):
        for t in range(k, k + 12):
            exact = 1 - eval_prod if False else None
            prod = Fraction(1)
            for i in range(k):
                prod *= 1 - Fraction(p**i, p**t)
            fail = 1 - prod
            hyper = Fraction(p**k - 1, p - 1) / p**t
            assert fail <= hyper <= Fraction(p**k, p**t)
            worst = max(worst, float(fail / Fraction(p**k, p**t)) if k else 0)
    for delta in (Fraction(1, 2), Fraction(1, 10), Fraction(1, 1000)):
        for k in range(0, 9):
            # ceil(log_p(2/delta)) computed exactly
            j = 0
            while p**j < 2 / delta:
                j += 1
            t = k + j
            prod = Fraction(1)
            for i in range(k):
                prod *= 1 - Fraction(p**i, p**t)
            assert 1 - prod <= delta / 2
print(f"  fail <= #hyperplanes * p^-t <= p^(k-t) everywhere; max ratio fail/p^(k-t) = {worst:.4f}; t=k+ceil(log_p(2/delta)) gives <= delta/2")

print("(3) counts:")
def mobius(n):
    res, m, q = 1, n, 2
    while q * q <= m:
        if m % q == 0:
            m //= q
            if m % q == 0:
                return 0
            res = -res
        q += 1
    return -res if m > 1 else res
def witt(s, k):
    return sum(mobius(j) * s**(k // j) for j in range(1, k + 1) if k % j == 0) // k
print("  d(4,9) =", sum(witt(4, k) for k in range(1, 10)))
print("  d(2,2) =", sum(witt(2, k) for k in range(1, 3)), " (Hall basis X1,X2,[X1,X2])")
for s in range(1, 6):
    for c in range(1, 8):
        d = sum(witt(s, k) for k in range(1, c + 1))
        assert d <= sum(s**k for k in range(1, c + 1))
print("  d <= sum s^k checked s<=5, c<=7; 9*143 =", 9 * 143)
e1 = 1 + sum(d * ceil(log2(d + 1)) for d in range(2, 10))
print("  Schedule-1 exponent at c=9:", e1)
lk = sum(d * (d - 1) * ceil(log2(d + 1)) / 2 * log2(d) for d in range(2, 10))
print(f"  log2(9 K_9) = {log2(9) + lk:.1f}")
E, t = 143, 40
f = lambda x: x * (x + t) * (x + 1)**(E - 1)
assert all(f(x) + f(y) <= f(x + y) for x in range(0, 60) for y in range(0, 60))
print("  x(x+t)(x+1)^(E-1) superadditive on 0..59 (E=143, t=40)")
print("  L <= l/log2(c+1): needs p >= c+1, true for p > c")
