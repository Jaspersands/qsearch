"""p >= 2e6: every contraction of (c)-(e) available by Lemma lem:sm thresholds, tier B absent,
p >= 4*9^4.  Degrees then depend only on p mod 5040; evaluate plus.py at one actual prime
>= 2e6 in every unit class mod 5040 (no searches are triggered: all thresholds exceeded)."""
import json
from math import gcd
from sympy import isprime
from rc import RCSearch
from plus import PlusDegrees, grade_sum
S = RCSearch(None); P = PlusDegrees(S, tierB=lambda p: False)
d = json.load(open("degrees_B_200000.json"))
at21 = sorted(int(p) for p, v in d.items() if 1 + grade_sum(int(p), {int(k): x for k, x in v["e"].items()}, 9) == 21)
expect = [13, 19, 37, 73] + [p for p in range(2521, 200000, 2520) if isprime(p)]
print("p<2e5 attaining 21 at c=9 equals {13,19,37,73} u {p=1 mod 2520}:", at21 == expect, len(at21))
best = {c: (0, []) for c in range(2, 10)}
for r in range(1, 5040):
    if gcd(r, 5040) != 1: continue
    p = 2_000_000 + ((r - 2_000_000) % 5040)
    while not isprime(p): p += 5040
    e = P.degrees(p)
    for c in range(2, 10):
        v = 1 + grade_sum(p, e, c)
        if v > best[c][0]: best[c] = (v, [r])
        elif v == best[c][0]: best[c][1].append(r)
print("searches triggered:", len(S.cache), "unknowns:", len(P.unknowns))
for c in range(2, 10): print(c, best[c][0], "residues mod 5040:", best[c][1][:6], len(best[c][1]))
