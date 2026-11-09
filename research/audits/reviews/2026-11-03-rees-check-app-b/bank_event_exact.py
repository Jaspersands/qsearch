"""Exact bank-event law at admissible Schedule-3 parameters, rank a = 1.

At a node with a_d = 1 the intrinsic bank is one uniform row x in F_p^M. Multiplying x_i by an
element of Q = (kappa-th powers) permutes P = Q u {0}, so N(x) depends only on how many x_i are
zero and how many lie in each coset xi^j Q. This script enumerates those class counts with their
exact multinomial probabilities, computes N by a dynamic program over F_p, and reports exactly:
  - Pr[bad bank] = Pr[x = 0 or N < EN/2] against beta = 4/mu + 2 p^{a-M};
  - the least per-trial acceptance N/p^{M-1} on a good bank against 1/(4 kappa^M);
  - the two counts N = 34^7 - 1 and 34^6 - 1 of Remark rem:s3-caveat (p = 67, M = 8, kappa = 2).
Every u = 2 node has a_d <= 1, so for u = 2 this is the full bank law of every node.

Run: /opt/anaconda3/bin/python -I bank_event_exact.py
"""
from fractions import Fraction as Fr
from math import factorial, gcd


def is_prime(n):
    return n > 1 and all(n % q for q in range(2, int(n ** 0.5) + 1))


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def generator(p):
    fac = [q for q in range(2, p) if (p - 1) % q == 0 and is_prime(q)]
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g


def coset_sum_dist(ns, p, cosetP, memo):
    if ns in memo:
        return memo[ns]
    if sum(ns) == 0:
        dist = [0] * p
        dist[0] = 1
    else:
        j = max(i for i, k in enumerate(ns) if k)
        prev = coset_sum_dist(ns[:j] + (ns[j] - 1,) + ns[j + 1:], p, cosetP, memo)
        dist = [0] * p
        for s, cnt in enumerate(prev):
            if cnt:
                for v in cosetP[j]:
                    dist[(s + v) % p] += cnt
    memo[ns] = dist
    return dist


def analyse(p, kappa, M):
    h = (p - 1) // kappa
    P = sorted({0} | {pow(x, kappa, p) for x in range(1, p)})
    xi = generator(p)
    cosetP = [sorted({(pow(xi, j, p) * v) % p for v in P}) for j in range(kappa)]
    a = 1
    mu = Fr((h + 1) ** M - 1, h * p ** a)
    EN = h * mu
    bad = Fr(1, p ** M)  # x = 0: rank 0 < a
    memo = {}
    min_acc = None
    for comp in compositions(M, kappa + 1):
        nz, ns = comp[0], comp[1:]
        if nz == M:
            continue
        multi = factorial(M)
        for k in comp:
            multi //= factorial(k)
        prob = Fr(multi * h ** (M - nz), p ** M)
        # DP (memoized over coset counts): number of (z_i), z_i in coset_j P, summing to 0
        dist = coset_sum_dist(ns, p, cosetP, memo)
        N = (h + 1) ** nz * dist[0] - 1
        if Fr(N) < EN / 2:
            bad += prob
        else:
            acc = Fr(N, p ** (M - 1))
            if min_acc is None or acc < min_acc:
                min_acc = acc
    beta = 4 / mu + 2 * Fr(p ** a, p ** M)
    return bad, beta, min_acc, Fr(1, 4 * kappa ** M)


fails = []
# Remark rem:s3-caveat
p, M, kappa = 67, 8, 2
h = (p - 1) // kappa
P = {0} | {pow(x, 2, p) for x in range(1, p)}
assert len(P) == 34 and pow(p - 1, h, p) != 1  # -1 is a nonsquare mod 67
pairs = sum(1 for y1 in P for y2 in P if (y1 + y2) % p == 0)
N_e1 = 34 ** 7 - 1
N_e12 = 34 ** 6 * pairs - 1
print("caveat: N(e1) =", N_e1, "N(e1+e2) =", N_e12, "pairs with y1+y2=0:", pairs,
      "ratio:", float(Fr(N_e1, N_e12)))
if pairs != 1 or N_e12 != 34 ** 6 - 1:
    fails.append("caveat")

rows = []
for u in (2, 3, 4):
    M = 4 * u
    ps = [q for q in range(16 * u * u, 16 * u * u + 160) if is_prime(q)][:(6 if u < 4 else 3)]
    for p in ps:
        for d in range(2, u + 1):
            kappa = gcd(d, p - 1)
            bad, beta, min_acc, acc_bd = analyse(p, kappa, M)
            ok = bad <= beta and (min_acc is None or min_acc >= acc_bd)
            if not ok:
                fails.append((u, p, d, kappa))
            rows.append((u, p, d, kappa, float(bad), float(beta), float(min_acc), float(acc_bd), ok))
print("u   p  d kap  Pr[bad]      beta        min_acc     1/(4k^M)  ok")
for r in rows:
    print("%d %4d %d %d  %.3e  %.3e  %.3e  %.3e  %s" % r)
print("failures:", fails)
