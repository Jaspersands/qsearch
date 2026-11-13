"""Headline-20 referee: p > 2e6.  (1) plus2.degrees at the least prime > 2e6 in every unit class
mod 5040 (no searches: every threshold is passed); (2) the closed form e = 1,2,2,2,2,2,3,3,3."""
from math import gcd
from plus2 import PlusDegrees, grade_sum
from verify_tl6 import isprime
class NoSearch:
    cache = {}
    def status(self, *a, **k): raise AssertionError("search requested above 2e6")
PD = PlusDegrees(NoSearch(), tierB=lambda p: False)
closed = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3}
best = {c: (0, []) for c in range(2, 10)}; mism = 0
for r in range(1, 5040):
    if gcd(r, 5040) != 1: continue
    p = 2000000 + ((r - 2000000) % 5040)
    while not isprime(p): p += 5040
    e = PD.degrees(p)
    mism += any(e[k] != closed[k] for k in e)
    for c in range(2, 10):
        v = 1 + grade_sum(p, e, c)
        if v > best[c][0]: best[c] = (v, [r])
        elif v == best[c][0]: best[c][1].append(r)
print("classes mod 5040:", sum(1 for r in range(5040) if gcd(r, 5040) == 1), "degree mismatches vs closed form:", mism)
for c in range(2, 10): print(f"c={c}: tail max {best[c][0]} at residues {best[c][1][:8]} ({len(best[c][1])})")
