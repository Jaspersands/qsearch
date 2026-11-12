"""Independent second method for tab:fcs-budget entries at the zero-sum depth.

Imports nothing from theorems/ or from recompute_fcs.py. Written from the definitions only:

  eq:Bd (core and full main.tex): B_d(a) = a+1 if kappa_d = 1, else G(kappa_d,a)^{ceil(log2 t)},
      G(k,a) = k^{k(k-1)/2} (a+1)^k, kappa_d = gcd(d,p-1), t = t_{p,kappa} the least t >= 2 with
      a zero sum z_1^k + ... + z_t^k = 0, z_i in F_p not all zero (equivalently all nonzero,
      since dropping zero terms keeps a zero sum).
  rem:combined-schedule (worst-case rule): lin (M = g+1) if kappa = 1; Schedule 2 with
      M = (g+1)((kappa-1)g+1) if kappa >= 2 and p >= 16 kappa^(2kappa+2); else B_d(g).
  Q = c (m + tau) prod_d M_d, tau = ceil(log_p(3/eps)), eps = 1/3.

t is found WITHOUT Lemma lem:zero-sum-length: for p <= 6000 by brute-force breadth-first search
over sums of nonzero kappa-th powers (own code); for large p by an explicit, verified witness:
t = 2 needs y with y^kappa = -1 (found from a random nonresidue and checked), and t > 2 is
certified by (-1)^h = -1 (so -1 is not a kappa-th power); t = 3 by explicit x, y with
x^kappa + y^kappa + 1 = 0 (searched with sympy's nthroot_mod, then checked by pow()).

The block-steered rows (combined column at 2^31-1, 2^61-1, 2^127-1) are NOT rechecked here; for
those rows this script checks the worst-case count printed in the caption.

Also: E_1(9) = 1 + sum_d kappa_d L_d at p = 2521 (the worst residue class of the core), as the
exponent of m in Q, from the same definitions.

Run (repo root):
  nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-full-tables/cross_check.py
"""
from __future__ import annotations

import json
import math
import random
from math import gcd
from pathlib import Path

from sympy import isprime
from sympy.ntheory.residue_ntheory import nthroot_mod

HERE = Path(__file__).resolve().parent
PROFILE = (19, 17, 16, 14, 12, 9, 6, 3, 1)
PRIMES = [("11", 11), ("1031", 1031), ("5281", 5281), ("2^31-1", 2**31 - 1),
          ("2^61-1", 2**61 - 1), ("2^127-1", 2**127 - 1)]
EXPECT = {  # values claimed by recompute_fcs.py (zero-sum depth), worst-case rule
    "11": "118.7", "1031": "83.9", "5281": "271.5",
    "2^31-1": "359.6", "2^61-1": "186.1", "2^127-1": "61.5"}


def G(k, a):
    return k ** (k * (k - 1) // 2) * (a + 1) ** k


def t_bfs(p, k):
    # u_1 + ... + u_t = 0 with u_j in P  <=>  (dividing by -u_t) t-1 elements of P sum to -1,
    # so t = 1 + (graph distance from 0 to -1 in Cay(F_p, P)).
    powers = sorted({pow(x, k, p) for x in range(1, p)})
    reach, frontier, n = {0}, {0}, 0
    while p - 1 not in reach:
        n += 1
        frontier = {(x + y) % p for x in frontier for y in powers} - reach
        reach |= frontier
        if n > k:
            raise AssertionError("Chevalley-Warning violated?")
    return n + 1, None


def t_witness(p, k, rng):
    h = (p - 1) // k
    if pow(p - 1, h, p) == 1:  # -1 is a kappa-th power: find y with y^k = -1
        while True:
            x = rng.randrange(2, p - 1)
            y = pow(x, (p - 1) // (2 * k), p) if (p - 1) % (2 * k) == 0 else None
            if y is not None and pow(y, k, p) == p - 1:
                return 2, [1, y]
            if y is None:  # k odd: y = -1 works
                assert pow(p - 1, k, p) == p - 1
                return 2, [1, p - 1]
    # here (-1)^h = -1, so -1 is not a kappa-th power and t > 2
    assert pow(p - 1, h, p) == p - 1
    for _ in range(100000):
        x = rng.randrange(1, p)
        u = (-1 - pow(x, k, p)) % p
        if u and pow(u, h, p) == 1:
            y = nthroot_mod(u, k, p)
            if y is not None and (pow(x, k, p) + pow(y, k, p) + 1) % p == 0:
                return 3, [x, y, 1]
    raise AssertionError("no length-3 witness found")


def t_of(p, k, rng):
    if k == 1:
        return None, None
    if p <= 6000:
        return t_bfs(p, k)
    return t_witness(p, k, rng)


def ceil_log2(t):
    return (t - 1).bit_length()


def worst_case(p, rng):
    c, m = len(PROFILE), PROFILE[0]
    tau = 0
    while p ** tau < 9:  # 3/eps = 9
        tau += 1
    prod, grades = 1, {}
    for d in range(2, c + 1):
        g = PROFILE[d - 1]
        k = gcd(d, p - 1)
        if k == 1:
            M, how = g + 1, "lin"
        elif p >= 16 * k ** (2 * k + 2):
            M, how = (g + 1) * ((k - 1) * g + 1), "S2"
        else:
            t, wit = t_of(p, k, rng)
            M, how = G(k, g) ** ceil_log2(t), f"S1(k={k},t={t},L={ceil_log2(t)})"
        grades[d] = (how, M)
        prod *= M
    Q = c * (m + tau) * prod
    return Q, grades


def log2_1dp(x):
    return f"{math.log2(x):.1f}"


def main():
    rng = random.Random(20261113)
    out, ok = [], True
    for label, p in PRIMES:
        assert isprime(p)
        Q, grades = worst_case(p, rng)
        v = log2_1dp(Q)
        agree = v == EXPECT[label]
        ok &= agree
        out.append(dict(label=label, log2_Q=v, expected=EXPECT[label], agree=agree,
                        grades={str(d): [h, str(M)] for d, (h, M) in grades.items()}))
        print(f"{label:>8s} worst-case log2 Q = {v} (expected {EXPECT[label]}) agree={agree}")
        for d, (h, M) in grades.items():
            if h.startswith("S1"):
                print(f"           grade {d}: {h}")
    # E_1(9) at p = 2521 from the definition
    p = 2521
    s, parts = 1, {}
    for d in range(2, 10):
        k = gcd(d, p - 1)
        t, _ = t_bfs(p, k) if k > 1 else (None, None)
        L = ceil_log2(t) if t else 0
        contrib = k * L if k > 1 else 1
        parts[d] = (k, t, L, contrib)
        s += contrib
    print("E_1 contributions at p = 2521 (d: kappa, t, L, kappa*L):", parts, "-> 1 + sum =", s)
    ok &= (s == 53)
    (HERE / "cross_check.json").write_text(json.dumps(dict(rows=out, E1_at_2521=s,
                                                           E1_parts={str(d): v for d, v in parts.items()},
                                                           all_agree=ok), indent=1) + "\n")
    print("all agree:", ok)
    return 0 if ok else 1




def ratio_check():
    """Block-steered rows: new combined Q = published combined Q (fcs_budget.json, 2026-11-04)
    times prod over Schedule-1 grades of G^{L_d} / G^{ceil(log2(kappa+1))}, assuming the
    block-steered grades do not move (they lie below every Schedule-1 grade at these rows, so
    their guards (G3) see the same n_d). Own t from t_witness."""
    from fractions import Fraction
    root = HERE.parents[3]
    pub = json.loads((root / "research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json").read_text())
    rng = random.Random(7)
    res = {}
    for r in pub["rows"]:
        if r["label"] not in ("2^31-1", "2^61-1"):
            continue
        p = int(r["p"])
        Q = Fraction(int(r["exact"]["combined_Q"]))
        s1 = [int(d) for d, (s, _) in r["combined"]["arities"].items() if s == "S1"]
        bs = [int(d) for d, (s, _) in r["combined"]["arities"].items() if s.startswith("BS")]
        assert max(bs) < min(s1)
        for d in s1:
            k, g = gcd(d, p - 1), PROFILE[d - 1]
            t, _ = t_witness(p, k, rng)
            Q *= Fraction(G(k, g) ** ceil_log2(t), G(k, g) ** ceil_log2(k + 1))
        assert Q.denominator == 1
        res[r["label"]] = log2_1dp(int(Q))
        print(f"ratio check {r['label']}: combined log2 Q = {res[r['label']]} (S1 grades {s1}, BS grades {bs})")
    return res


if __name__ == "__main__":
    status = main()
    rc = ratio_check()
    data = json.loads((HERE / "cross_check.json").read_text())
    data["block_steered_ratio_check"] = rc
    (HERE / "cross_check.json").write_text(json.dumps(data, indent=1) + "\n")
    raise SystemExit(status)
