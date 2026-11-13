"""2e5 <= p < 2e6: degrees are the large-p formula except that TW9 (p < 1124521) and U7
(p < 1995734) need a certificate (TL3/4/5 are past threshold).  We search certificates only
where a missing one could change max status at any c (sum+penalty >= value that would tie/exceed);
for safety we search at every prime where the c=9 sum with the step missing would be >= 20, or
the c<=8 sums would reach their claimed maxima."""
import sys, json, time
from math import gcd
from fp import primes_upto
from rc import RCSearch
CL = {2: 3, 3: 5, 4: 9, 5: 10, 6: 14, 7: 16, 8: 19, 9: 21}
def evec(p, tw, u7):
    ks = [k for k in range(1, 10) if (p - 1) % k == 0]
    e = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 3, 8: 3}
    e[7] = 3 if u7 else 7
    e[9] = 3 if tw else 9
    return e
def sums(p, e): return {c: 1 + sum(e[gcd(d, p - 1)] for d in range(2, c + 1)) for c in range(2, 10)}
S = RCSearch("rc_cache_gap.json")
lo, hi = int(sys.argv[1]), int(sys.argv[2])
need = []; best = {c: (0, []) for c in range(2, 10)}; t0 = time.time(); nsearch = 0
for p in primes_upto(hi):
    if p < lo: continue
    n9 = (p - 1) % 9 == 0 and p < 1124521; n7 = (p - 1) % 7 == 0 and p < 1995734
    tw = u7 = True
    if n9 or n7:
        worst = sums(p, evec(p, not n9, not n7))
        if any(worst[c] > CL[c] for c in CL) or worst[9] >= 21 or (p - 1) % 2520 == 0:
            if n9:
                st, _ = S.status(p, 9, [0, 3, 6], [0], rtrials=200, exhaustive=False); tw = st == "FOUND"; nsearch += 1
            if n7:
                u7 = False
                for m in range(1, 7):
                    st, _ = S.status(p, 7, list(range(7)), [0, m], rtrials=200, exhaustive=False); nsearch += 1
                    if st == "FOUND": u7 = True; break
            if not (tw and u7): need.append((p, tw, u7))
    s = sums(p, evec(p, tw, u7))
    for c in range(2, 10):
        if s[c] > best[c][0]: best[c] = (s[c], [p])
        elif s[c] == best[c][0]: best[c][1].append(p)
    if nsearch and nsearch % 500 == 0: S.save()
S.save()
print("range", lo, hi, "searches", nsearch, "missing certs", need[:20], len(need), "time", round(time.time() - t0))
for c in range(2, 10):
    print(c, best[c][0], best[c][1][:5], len(best[c][1]), "all =1 mod 2520" if c == 9 and all((q - 1) % 2520 == 0 for q in best[c][1]) else "")
