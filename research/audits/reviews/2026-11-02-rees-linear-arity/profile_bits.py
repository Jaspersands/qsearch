"""Class-9 reference profile (a_d = 17,16,14,12,9,6,3,1 for d = 2..9, kappa_d = d):
log2 of the product of per-grade arities under each scheme.  Exact integer arithmetic."""
from math import log2, log, floor

prof = dict(zip(range(2, 10), [17, 16, 14, 12, 9, 6, 3, 1]))

def L_cw(k):
    L = 1
    while k ** L <= k * (k - 1) ** L:
        L += 1
    return L

def old_L(k, a, L):
    out = 1
    for l in range(L):
        out *= (k - 1) ** l * a + 1
    return out

def new_L_product(k, a, L):
    out = 1
    for t in range(1, L + 1):
        r = min((k - 1) ** (t - 1), k ** (L - t))
        out *= r * a + 1
    return out

def new_L_tri(k, a, L):
    tot = 1
    for q in range(1, a + 1):
        t = 1
        for s in range(1, L):
            r = min((k - 1) ** (s - 1), k ** (L - s))
            t *= r * q + 1
        tot += t
    return tot

rows = []
tot = {k: 0.0 for k in ["S2", "prod2", "tri2", "oldLcw", "newLprod", "newLtri"]}
for d, a in prof.items():
    k = d
    L = L_cw(k)
    vals = {
        "S2": (a + 1) * ((k - 1) * a + 1),
        "prod2": (a + 1) ** 2,
        "tri2": (a + 1) * (a + 2) // 2,
        "oldLcw": old_L(k, a, L),
        "newLprod": new_L_product(k, a, L),
        "newLtri": new_L_tri(k, a, L),
    }
    for key, v in vals.items():
        tot[key] += log2(v)
    rows.append((d, a, L, vals))
print("d a L_CW | S2 (a+1)((k-1)a+1) | (a+1)^2 | (a+1)(a+2)/2 | old L_CW | new L_CW product | new L_CW triangular")
for d, a, L, v in rows:
    print(d, a, L, "|", v["S2"], v["prod2"], v["tri2"], "|", f"2^{log2(v['oldLcw']):.1f}", f"2^{log2(v['newLprod']):.1f}", f"2^{log2(v['newLtri']):.1f}")
print("total bits:", {k: round(v, 1) for k, v in tot.items()})
