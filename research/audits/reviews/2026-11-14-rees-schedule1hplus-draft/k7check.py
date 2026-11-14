# Run from a COPY of research/audits/reviews/2026-11-13-rees-headline-20-referee/ (imports its plus2.py, rc.py, fp.py and reads its rc_cache.json, certs_accepted.json; never saves the cache).
# Draft-helper check: at kappa = 7, is the computed degree 3 at every prime p = 1 (mod 7), 523 < p < 9604?
# and which m are available at the U7 gap primes 29, 43, 113 (search cache, exhaustive at p <= 600)?
from fp import primes_upto
from rc import RCSearch
from plus2 import PlusDegrees
S = RCSearch("rc_cache.json")
PD = PlusDegrees(S, tierB=lambda p: p <= 523)
bad = []
for p in primes_upto(9604):
    if p <= 523 or (p - 1) % 7: continue
    e, how = PD.degrees(p, want_trace=True)
    if e[7] != 3: bad.append((p, e[7], how[7]))
print("kappa=7, 523<p<9604, p=1 mod 7: primes with e7 != 3:", bad)
for p in (29, 43, 113):
    print(p, [(m, PD.avail(p, 7, range(7), [0, m], std="U7")) for m in range(1, 7)])
print("unknowns", PD.unknowns[:10])
