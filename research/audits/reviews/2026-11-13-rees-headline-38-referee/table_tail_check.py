# Referee: tail-by-residue check of E_H and of the class-9 Q_q, and the crossover columns of
# tab:query-crossover, recomputed from Prop. classical-query (i),(v) as printed in main-core.tex.
import json, math, sys
from mpmath import mp, mpf, log, sqrt, ceil, binomial
mp.dps = 60
sys.path.insert(0, '.')
from s1h_referee import S1H, primes_upto

def G(k, a): return k ** (k * (k - 1) // 2) * (a + 1) ** k

def A_tail(k, a, r):  # p >= 26244, p = r mod 5040; Lemma zero-sum (ii),(iii): t = 2 if h even else 3
    if k == 1: return a + 1
    L = 1 if ((r - 1) // k) % 2 == 0 else 2   # parity of (p-1)/k determined by r mod 5040 (k | 2520·2? k<=9)
    best = G(k, a) ** L
    if k % 2 == 0: best = min(best, (a + 1) * A_tail(k // 2, a, r))
    return best

def e_tail(k, r):
    if k == 1: return 1
    L = 1 if ((r - 1) // k) % 2 == 0 else 2
    e = k * L
    if k % 2 == 0: e = min(e, e_tail(k // 2, r) + 1)
    return e

units = [r for r in range(1, 5040) if math.gcd(r, 5040) == 1]
out = {}
EHt = {}
for c in range(2, 10):
    vals = {r: 1 + sum(e_tail(math.gcd(d, r - 1), r) for d in range(2, c + 1)) for r in units}
    mx = max(vals.values()); EHt[c] = [mx, [r for r in units if vals[r] == mx][:10]]
out["E_H_tail_by_residue"] = EHt
prof = [17, 16, 14, 12, 9, 6, 3, 1]
def Q9_tail(r):
    Q = 9 * 20
    for d, g in zip(range(2, 10), prof): Q *= A_tail(math.gcd(d, r - 1), g, r)
    return Q
qt = {r: Q9_tail(r) for r in units}
mx = max(qt.values())
out["Q9_tail_max_log2"] = [math.log2(mx), [r for r in units if qt[r] == mx]]
# consistency: exact S1H vs residue formula on primes in [26244, 40000]
bad = 0; n = 0
for p in primes_upto(40000):
    if p < 26244: continue
    o = S1H(p); r = p % 5040; n += 1
    for k in o.info:
        if k > 1 and o.info[k]['e'] != e_tail(k, r): bad += 1
        for a in (0, 1, 3, 9, 17):
            if o.A(k, a) != A_tail(k, a, r): bad += 1
out["exact_vs_residue_formula"] = [n, bad]

# crossover columns
rows = {"heis": (3, 32), "fil": (4, 29160), "free": (5, 209952), "dl": (8, 492075), "c9": (19, mx)}
def N1(p, m): return (mpf(p) ** m - 1) / (mpf(p) - 1)
def subspaces(p, m):
    p = mpf(p); tot = mpf(0)
    for k in range(m + 1):
        num = mpf(1); den = mpf(1)
        for i in range(k):
            num *= (p ** (m - i) - 1); den *= (p ** (i + 1) - 1)
        tot += num / den
    return tot
res = {}
for nm, (m, Q) in rows.items():
    Q = mpf(Q)
    # LB > Q from: smallest p with binom(Q,2) < (2/3)N1 - 1  (then any q <= Q violates (i))
    f = lambda p: (mpf(2) / 3) * N1(p, m) - 1 - Q * (Q - 1) / 2
    def vcl(p, eightl):
        tau = 1; l = log(6)
        return 5 * (m + tau) + 16 * ceil(l) + ceil(sqrt(2 * mpf(p) ** (m - 1) * max(2 * tau + 2, eightl)))
    if nm != "c9":
        ps = [p for p in primes_upto(10 ** 6) if p >= 11]
        lb = next(p for p in ps if f(p) > 0)
        v15 = [p for p in ps if vcl(p, 15) < Q]
        v8l = [p for p in ps if vcl(p, 8 * log(6)) < Q]
        res[nm] = dict(log2Q=float(log(Q, 2)), LB_from=lb, v15_last_prime=(v15[-1] if v15 else None),
                       v8l_last_prime=(v8l[-1] if v8l else None),
                       copies=int(ceil(4 * log(3 * subspaces(lb, m), 2))))
        # real thresholds for v
        lo, hi = mpf(2), mpf(10 ** 6)
        for e8, key in ((15, "v15_real"), (8 * log(6), "v8l_real")):
            lo, hi = mpf(2), mpf(10 ** 6)
            if not (vcl(lo, e8) < Q): res[nm][key] = None; continue
            for _ in range(200):
                mid = (lo + hi) / 2
                if vcl(mid, e8) < Q: lo = mid
                else: hi = mid
            res[nm][key] = float(lo)
    else:
        # real-valued thresholds
        lo, hi = mpf(2) ** 30, mpf(2) ** 40
        for _ in range(300):
            mid = (lo + hi) / 2
            if f(mid) > 0: hi = mid
            else: lo = mid
        lbp = hi
        lo2, hi2 = mpf(2) ** 30, mpf(2) ** 40
        for _ in range(300):
            mid = (lo2 + hi2) / 2
            if (5 * 20 + 32 + sqrt(2 * mid ** 18 * 15)) < Q: lo2 = mid
            else: hi2 = mid
        res[nm] = dict(log2Q=float(log(Q, 2)), log2_LB=float(log(lbp, 2)), log2_v15=float(log(lo2, 2)),
                       copies_at_LB=int(ceil(4 * log(3 * subspaces(lbp, m), 2))))
out["table"] = res
print(json.dumps(out, indent=1, default=str))
