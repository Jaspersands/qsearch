"""Checks of threshold-7 Section 3 (barrier).
(1) Lemma 3.2(b), r = 1, by brute force: |Z_alpha| <= 1 + (p-1)(kappa-1)/kappa over all alpha
    with alpha_0 = 0, alpha != 0, at kappa = 4, p in {17, 37} (both in E_2(4));
    and the stronger form: Z_alpha misses a whole class of t != 0.
(2) m_0(kappa, p, h): least m with the bound of Theorem 3.1 below 1 (log-space, exact formula)."""
import itertools, math
from rc import primitive_root
def lem32(kap, p):
    g = primitive_root(p); cls = [None] * p; x = 1
    for e in range(p - 1): cls[x] = e % kap; x = x * g % p
    ok = lambda v, nu: v == 0 or cls[v] == (-nu) % kap
    worst, allmiss = 0, True
    for rest in itertools.product(range(p), repeat=kap - 1):
        al = (0,) + rest
        if not any(rest): continue
        Z = [t for t in range(p) if any(all(ok((u + t * al[nu]) % p, nu) for nu in range(kap)) for u in range(p))]
        worst = max(worst, len(Z))
        missing = {c for c in range(kap) if not any(t and cls[t] == c for t in Z)}
        if not missing: allmiss = False
    return worst, 1 + (p - 1) * (kap - 1) // kap, allmiss
for p in [17, 37]:  # p = 53, 41 are too slow for this brute force under load
    w, b, am = lem32(4, p)
    print("kappa=4 p=%d: max|Z_alpha|=%d, bound 1+(p-1)(k-1)/k=%d, every Z_alpha misses a class: %s" % (p, w, b, am), flush=True)
def logbound(kap, p, h, m):
    n = m + h; terms = []
    th = lambda r: 1 - (1 - p ** (-r)) / kap
    terms.append(math.log(kap) + h * math.log(p) + n * math.log(th(1)))
    for r in range(2, kap): terms.append(r * (kap - 1 + h) * math.log(p) + n * math.log(th(r)))
    mx = max(terms); return mx + math.log(sum(math.exp(t - mx) for t in terms))
def m0(kap, p, h):
    m = 1
    while logbound(kap, p, h, m) >= 0: m += 1
    return m
for args in [(4, 17, 1), (4, 17, 2), (4, 37, 2), (5, 31, 2), (8, 11689, 4), (8, 12809, 4)]:
    print("m_0%s = %d" % (args, m0(*args)))
