"""Exact depth J(h,p) of the digit chain D_0 = mu_h u {0}, D_{j+1} = D_j - D_j, with the bounds
of the report (Cauchy-Davenport, Weil/Jacobi, l1-ball lower bound, Minkowski upper bound).

Usage: python run_depth.py out.json
"""
import json
import math
import sys
from sympy import primerange, totient

from wh_lib import depth_fft, chain_sets, power_basis_coeffs, l1_ball_count, weil_ok

out = {}

# 1. consistency: FFT depth == set depth on small cases; h = 1 gives ceil(log2(p-1)) (Theorem P)
cons = []
for h in [1, 2, 3, 4, 5, 6]:
    for p in primerange(3, 200):
        if (p - 1) % h:
            continue
        J1 = len(chain_sets(h, p)) - 1
        J2, sizes = depth_fft(h, p)
        ok = J1 == J2
        if h == 1:
            ok = ok and J1 == math.ceil(math.log2(p - 1))
        if h == 2:
            ok = ok and J1 == math.ceil(math.log2(p - 1)) - 1
        cons.append((h, p, J1, J2, ok))
out["consistency_all_ok"] = all(c[-1] for c in cons)
out["consistency_cases"] = len(cons)

# 2. per-h tables up to a bound, with the analytic bounds
def bounds(h, p):
    phi, coef = power_basis_coeffs(h)
    ch = max(sum(abs(c) for c in co) for co in coef)
    kappa = (p - 1) // h
    cd = max(0, math.ceil(math.log2(kappa))) if kappa >= 1 else 0
    # lower bound: least J with #l1-ball(phi, ch*2^J) >= p
    Jlb = 0
    while l1_ball_count(phi, ch * 2 ** Jlb) < p:
        Jlb += 1
    rho = ch * phi * phi * p ** (1.0 / phi) / 2
    Jub = (0 if h % 2 == 0 else 1) + max(0, math.ceil(math.log2(rho)))
    return phi, ch, kappa, cd, Jlb, Jub

tables = {}
viol = []
for h, pmax in [(3, 60000), (4, 60000), (5, 30000), (6, 60000), (7, 20000), (8, 20000),
                (10, 20000), (12, 20000)]:
    rows = []
    for p in primerange(h + 2, pmax):
        if (p - 1) % h:
            continue
        J, sizes = depth_fft(h, p)
        phi, ch, kappa, cd, Jlb, Jub = bounds(h, p)
        w1 = weil_ok(kappa, p)
        if not (Jlb <= J <= Jub and J <= cd and (not w1 or J == 1)):
            viol.append((h, p, J, Jlb, Jub, cd, w1))
        rows.append({"p": p, "kappa": kappa, "J": J, "sizes": sizes, "J_lb": Jlb, "J_ub": Jub,
                     "cd": cd, "weil_J1": w1})
    tables[str(h)] = rows
out["violations"] = viol

# compact summary per h: J against log2(p)/phi(h)
summ = {}
for h, rows in tables.items():
    phi = int(totient(int(h)))
    byJ = {}
    for r in rows:
        byJ.setdefault(r["J"], []).append(r["p"])
    summ[h] = {"phi": phi, "primes": len(rows),
               "J_range_by_value": {J: [min(v), max(v), len(v)] for J, v in sorted(byJ.items())},
               "max_J_minus_log2p_over_phi": max(r["J"] - math.log2(r["p"]) / phi for r in rows),
               "min_J_minus_log2p_over_phi": min(r["J"] - math.log2(r["p"]) / phi for r in rows)}
out["summary_by_h"] = summ
out["test_primes"] = {f"h={r_h},p={r['p']}": {"kappa": r["kappa"], "J": r["J"], "sizes": r["sizes"]}
                      for r_h in ["3", "4"] for r in tables[r_h] if r["p"] in (7, 13, 19, 31, 5, 17)}

# 3. per-kappa: primes p = 1 mod kappa (h = (p-1)/kappa >= 2) with J >= 2, exhaustively up to
#    the Weil threshold ((kappa-1)(kappa-2)+3)^2 beyond which J = 1 is proved
perk = {}
for kappa in range(2, 21):
    thr = ((kappa - 1) * (kappa - 2) + 3) ** 2
    bad = []
    hist = {}
    for p in primerange(2 * kappa + 1, thr + 1):
        if (p - 1) % kappa:
            continue
        h = (p - 1) // kappa
        J, _ = depth_fft(h, p)
        hist[J] = hist.get(J, 0) + 1
        if J >= 2:
            bad.append((p, J))
    perk[kappa] = {"weil_threshold": thr, "J_hist": hist, "primes_with_J_ge_2": bad,
                   "largest_J_ge_2": max([b[0] for b in bad], default=None),
                   "cd_bound": math.ceil(math.log2(kappa))}
out["per_kappa"] = perk

# the paper's exceptional sets E_2(4), E_2(5), and 11689 in E_2(8): depth there
ex = {}
for kappa, ps in [(4, [5, 13, 17, 29, 37, 53]), (5, [11, 31, 41, 61, 71, 101, 131, 151, 181]),
                  (8, [11689]), (9, [17911])]:
    for p in ps:
        h = (p - 1) // kappa
        if h >= 1:
            ex[f"kappa={kappa},p={p}"] = {"h": h, "J": depth_fft(h, p)[0]}
out["E2_primes"] = ex

with open(sys.argv[1], "w") as f:
    json.dump(out, f, indent=1)
print("consistency", out["consistency_all_ok"], out["consistency_cases"], "violations", len(viol))
for h, s in summ.items():
    print(h, s)
for k, v in perk.items():
    print(k, v["J_hist"], v["largest_J_ge_2"], "cd", v["cd_bound"])
print(ex)
