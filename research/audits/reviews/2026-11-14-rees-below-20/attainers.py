#!/usr/bin/env python3
"""Per-attainer bookkeeping for E_+(9) = 20 (core lem:plus-exponent, rem:plus-profile).
Grade vectors e_d (d = 2..9) are copied from rem:plus-profile / v2/rule_v2.out (read-only).
For each attainer it lists kappa_d = gcd(d, p-1), the X-lower bound of each grade
(2 for kappa >= 2, 1 for kappa = 1) and which grades could drop (e_d above that floor)."""
from math import gcd
E = {37: [2, 2, 3, 1, 3, 1, 3, 4], 43: [2, 2, 2, 1, 4, 4, 2, 2], 73: [2, 2, 2, 1, 3, 1, 4, 4],
     127: [2, 2, 2, 1, 3, 3, 2, 4], 181: [2, 2, 2, 3, 3, 1, 2, 4], 631: [2, 2, 2, 2, 3, 3, 2, 3],
     '1 mod 2520': [2, 2, 2, 2, 2, 3, 3, 3]}
for p, e in E.items():
    if p == '1 mod 2520':
        kap = list(range(2, 10))
    else:
        kap = [gcd(d, p - 1) for d in range(2, 10)]
    floor = [1 if k == 1 else 2 for k in kap]
    drops = sorted({(k, x) for k, x, f in zip(kap, e, floor) if x > f})
    print(f"p={p}: kappa_d={kap} e_d={e} sum={sum(e)} E={1+sum(e)} floor-sum={sum(floor)}; "
          f"grades above floor (kappa, e): {drops}")
