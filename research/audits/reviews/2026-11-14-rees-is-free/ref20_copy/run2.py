"""Headline-20 referee: E(c), c = 2..9, for all primes p < PMAX under Schedule 1H++ (own code:
plus2.py = the -21-recompute's plus.py + fragment-v2 candidates (g), (h)).
variant: def (Tier B at the 28 primes of tierB.json, the fragment's definition) or allB (all p <= 523);
flags: noTL6, noELL, none (= 1H+ regression)."""
import sys, time, json
from math import gcd
from fp import primes_upto
from rc import RCSearch
from plus2 import PlusDegrees, grade_sum
PMAX = int(sys.argv[1]); variant = sys.argv[2]; flags = sys.argv[3:]
TB28 = {5, 7, 11, 13, 19, 29, 31, 37, 41, 43, 61, 71, 73, 101, 109, 113, 127, 131, 151, 163, 181, 199, 271, 307, 379, 433, 487, 523}
S = RCSearch("rc_cache.json")
kw = dict(use_tl6="noTL6" not in flags and "none" not in flags, use_ell="noELL" not in flags and "none" not in flags)
kw["no_S1"] = "noS1" in flags
kw["tierB"] = (lambda p: p in TB28) if variant == "def" else (lambda p: p <= 523)
PD = PlusDegrees(S, **kw)
t0 = time.time(); best = {c: (0, []) for c in range(2, 10)}; vec = {}
MISS53 = [7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 199, 211, 223, 241, 271, 277, 283, 307, 331, 349, 367, 373, 379, 409, 421, 433, 439, 463, 487, 499, 523, 547, 577, 619, 631, 643, 661, 673, 691, 751, 757, 787, 859]
WATCH = {13, 19, 29, 37, 43, 73, 127, 181, 433, 631, 673, 1009, 2017, 2521, 7561} | set(MISS53)
noplan = []
for p in primes_upto(PMAX):
    if p < 3: continue
    e, how = PD.degrees(p, want_trace=True)
    if any(v >= 10**6 for v in e.values()): noplan.append(p)
    for c in range(2, 10):
        if p <= c: continue
        v = 1 + grade_sum(p, e, c)
        if v > best[c][0]: best[c] = (v, [p])
        elif v == best[c][0]: best[c][1].append(p)
    if p in WATCH: vec[p] = ([e[gcd(d, p - 1)] for d in range(2, 10)], {k: how[k] for k in sorted(how)})
S.save()
print("variant", variant, flags, "PMAX", PMAX, "no-plan primes", noplan[:10])
print("E =", {c: best[c][0] for c in range(2, 10)})
for c in range(2, 10):
    at = best[c][1]; non2520 = [q for q in at if (q - 1) % 2520]
    print(f"c={c}: max {best[c][0]} at {len(at)} primes; not =1 mod 2520: {non2520[:20]}{'...' if len(non2520) > 20 else ''}")
for p in sorted(vec):
    if p in MISS53 and p not in {13, 19, 37, 43, 73, 127, 181, 631}: continue
    print(p, "e_d(d=2..9) =", vec[p][0], "sum+1 =", 1 + sum(vec[p][0]), vec[p][1])
m53 = {p: 1 + sum(vec[p][0]) for p in MISS53 if p in vec}
print("53 TL6-less primes: E(9) values", m53, "max", max(m53.values()) if m53 else None, "kappa6 plans:", {p: vec[p][1].get(6) for p in MISS53 if p in vec and 6 in vec[p][1]})
print("unknowns", len(PD.unknowns), PD.unknowns[:10], "time", round(time.time() - t0), "s")
