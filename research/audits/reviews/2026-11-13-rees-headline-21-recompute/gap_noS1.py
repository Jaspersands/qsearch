"""No-S1 variant on 2e5 <= p < 2e6: every p = 1 mod 9 below 1124521 needs a TW9 certificate
and every p = 1 mod 7 below 1995734 a U7 certificate (some m); else kappa = 9 (resp. 7) has no
plan without S1 at large p (candidates there: (a), (d)/(e) only; tier B absent; p >= 4 kappa^4).
kappa = 3,4,5: TL past threshold; kappa = 2,6,8: halving over GE/H3/H4 (no S1)."""
import sys, time
from math import gcd
from fp import primes_upto
from rc import RCSearch
S = RCSearch("rc_cache_gap.json"); lo, hi = int(sys.argv[1]), int(sys.argv[2])
fail = []; t0 = time.time(); n = 0; best = {c: (0, []) for c in range(2, 10)}
for p in primes_upto(hi):
    if p < lo: continue
    tw = u7 = True
    if (p - 1) % 9 == 0 and p < 1124521:
        st, _ = S.status(p, 9, [0, 3, 6], [0], rtrials=200, exhaustive=False); tw = st == "FOUND"; n += 1
    if (p - 1) % 7 == 0 and p < 1995734:
        u7 = False
        for m in range(1, 7):
            st, _ = S.status(p, 7, list(range(7)), [0, m], rtrials=200, exhaustive=False); n += 1
            if st == "FOUND": u7 = True; break
    if not (tw and u7): fail.append((p, tw, u7))
    e = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3, 9: 3}
    s = {c: 1 + sum(e[gcd(d, p - 1)] for d in range(2, c + 1)) for c in range(2, 10)}
    for c in range(2, 10):
        if s[c] > best[c][0]: best[c] = (s[c], [p])
        elif s[c] == best[c][0]: best[c][1].append(p)
    if n and n % 1000 == 0: S.save()
S.save()
print("range", lo, hi, "queries", n, "NO-PLAN primes (tw,u7):", fail[:20], len(fail), "time", round(time.time() - t0))
for c in range(2, 10): print(c, best[c][0], len(best[c][1]))
