"""No-S1 with tier B restricted to the helper's 28 listed primes (only the prime list is taken
from tierB.json; chains are this checker's own).  Also tier B switched off entirely."""
import json, sys
from math import gcd
from fp import primes_upto
from rc import RCSearch
from plus import PlusDegrees, grade_sum
TB = {int(k.split('|')[0]) for k in json.load(open('../2026-11-13-rees-headline-below-38/tierB.json'))}
S = RCSearch("rc_cache.json")
for name, tb in (("tb28", lambda p: p in TB), ("noB", lambda p: False)):
    for noS1 in (False, True):
        P = PlusDegrees(S, tierB=tb, no_S1=noS1)
        best = {c: (0, []) for c in range(2, 10)}; noplan = []
        for p in primes_upto(int(sys.argv[1])):
            if p < 3: continue
            e, how = P.degrees(p, want_trace=True)
            noplan += [(p, k) for k in e if e[k] >= 10**5]
            for c in range(2, 10):
                if p <= c: continue
                v = 1 + grade_sum(p, e, c)
                if v > best[c][0]: best[c] = (v, [p])
                elif v == best[c][0]: best[c][1].append(p)
        print(name, "noS1" if noS1 else "withS1", "NO-PLAN (p,k):", noplan[:12], len(noplan),
              "| E:", [best[c][0] for c in range(2, 10)], "| c=9 at", best[9][1][:8], flush=True)
S.save()
