"""v2: certificates for the two-level kappa = 6 contraction RC(6; Z_6 -> {0}) at every prime
p = 1 (mod 2520) below T_exist(TL6) = 837384 (thresholds.out).  Above that, Lemma SM.
AI-written 2026-11-13, pending human review.  Finite search; every witness passes check_rc.
Run: nice -n 19 /opt/anaconda3/bin/python v2/run_tl6.py  (writes v2/certs_tl6.json)"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from certs import find_rc, primes_upto, prim_root
BOUND = 837384
res, missing = {}, []
t0 = time.time()
for p in primes_upto(BOUND - 1):
    if p % 2520 != 1: continue
    got = None
    for tr in (300, 3000, 30000):
        got = find_rc(p, 6, list(range(6)), [0], trials=tr, seed=tr)
        if got and got[0] != 'undecided': break
    if got and got[0] != 'undecided':
        res[p] = {'g': prim_root(p), 'K': [0], 'alpha': got[0], 'beta': {str(i): v for i, v in got[1].items()}, 'how': got[2]}
    else:
        missing.append((p, None if got is None else 'undecided'))
    print(p, 'found' if p in res else 'MISSING', res.get(p, {}).get('how'), f'{time.time()-t0:.0f}s', flush=True)
json.dump({'two-level 6 (p=1 mod 2520)': {'D': 6, 'bound': BOUND, 'found': res, 'missing': missing}},
          open(os.path.join(HERE, 'certs_tl6.json'), 'w'))
print('found', len(res), 'missing', missing, f'{time.time()-t0:.0f}s')
