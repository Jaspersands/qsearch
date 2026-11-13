"""Recompute E_1(c) (Schedule 1, lem:exponent) and E_H(c) (Schedule 1H, def:schedule1h,
lem:halved-exponent) from the written definitions."""
import sys, json
from math import gcd, ceil, log2
from fp import Field, primes_upto, t_pk, T_sets

def clog2(t): return (t - 1).bit_length()   # ceil(log2 t) for t >= 1

def degrees_core(p, F=None):
    """dict kappa -> (e1, eH) for kappa | p-1, kappa <= 9."""
    ks = [k for k in range(1, 10) if (p - 1) % k == 0]
    exact = p < 4 * 9 ** 4
    t = {}
    for k in ks:
        if k == 1: continue
        if F is not None and (exact or True):
            t[k] = t_pk(F, k)
        else:
            t[k] = 2 if ((p - 1) // k) % 2 == 0 else 3
    e1, eH = {1: 1}, {1: 1}
    for k in ks:
        if k == 1: continue
        L = clog2(t[k]); e1[k] = k * L
        best = k * L
        if k % 2 == 0:
            Dh = k // 2
            if p >= 4 * k ** 4:
                best = min(best, eH[Dh] + 1)
            else:
                T = T_sets(F, k, Dh, k + 2)
                for s in range(1, k + 3):
                    if T[s].zero: best = min(best, s * eH[Dh])
                    if len(T[s].cls) == k: best = min(best, s * eH[Dh] + 1)
        eH[k] = best
    return t, e1, eH

def grade_sum(p, e, c):
    return sum(e[gcd(d, p - 1)] for d in range(2, c + 1))

if __name__ == "__main__":
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 26244
    res = {c: {"E1": 0, "EH": 0, "E1p": [], "EHp": []} for c in range(2, 10)}
    tcheck_bad = []
    for p in primes_upto(PMAX):
        if p < 3: continue
        F = Field(p) if p < 26244 else None
        if F is None:
            # above 4*9^4: t from Lemma zero-sum-length(ii)-(iii); verify exactly on a sample
            pass
        t, e1, eH = degrees_core(p, F)
        for c in range(2, 10):
            if p <= c: continue
            for key, e in (("E1", e1), ("EH", eH)):
                v = 1 + grade_sum(p, e, c)
                if v > res[c][key]: res[c][key] = v; res[c][key + "p"] = [p]
                elif v == res[c][key]: res[c][key + "p"].append(p)
    # residue-class part for p >= 26244: degrees depend on p mod 5040 only
    for r in range(1, 5040, 2):
        if gcd(r, 5040) != 1: continue
        p = r + 5040 * 100   # representative label; formula only
        ks = [k for k in range(1, 10) if (p - 1) % k == 0]
        _, e1, eH = degrees_core(p, None)
        for c in range(2, 10):
            for key, e in (("E1", e1), ("EH", eH)):
                v = 1 + grade_sum(p, e, c)
                if v > res[c][key]: res[c][key] = v; res[c][key + "p"] = [f"r{r}mod5040"]
                elif v == res[c][key]: res[c][key + "p"].append(f"r{r}mod5040")
    for c in range(2, 10):
        r = res[c]
        print(c, "E1", r["E1"], r["E1p"][:8], len(r["E1p"]), "| EH", r["EH"], r["EHp"][:8], len(r["EHp"]))
