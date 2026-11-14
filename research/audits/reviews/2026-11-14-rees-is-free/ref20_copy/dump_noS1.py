"""Dump per-(p,kappa) degrees of the 20-referee's plus2.py (allB, S1 forbidden) for p < N.
Run from this folder (copy of the 20-referee code; writes only here)."""
import sys, json
from fp import primes_upto
from rc import RCSearch
from plus2 import PlusDegrees
N = int(sys.argv[1])
S = RCSearch("rc_cache.json")
PD = PlusDegrees(S, use_tl6=True, use_ell=True, no_S1=True, tierB=lambda p: p <= 523)
out = {}
for p in primes_upto(N):
    if p < 3: continue
    e, how = PD.degrees(p, want_trace=True)
    for k, v in e.items():
        if k >= 2: out['%d,%d' % (p, k)] = v
json.dump(out, open('degs_ref20_noS1_%d.json' % N, 'w'))
print('pairs', len(out), 'unknowns', len(PD.unknowns))
