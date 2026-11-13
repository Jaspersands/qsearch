"""v2: TL6 certificates RC(6; Z_6 -> {0}) at every prime p = 1 (mod 6), p < 837384 (all residue
classes; run_tl6.py did p = 1 mod 2520 only).  Missing = not found (NOT a non-existence proof unless
the complete DFS says 0).  Writes v2/certs_tl6_all.json.  AI-written 2026-11-13, pending review."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from certs import find_rc, primes_upto, prim_root
BOUND = 837384
res, missing = {}, []
t0 = time.time()
for p in primes_upto(BOUND - 1):
    if p < 7 or p % 6 != 1: continue
    got = None
    for tr in (300, 3000, 30000):
        got = find_rc(p, 6, list(range(6)), [0], trials=tr, seed=tr)
        if got and got[0] != 'undecided': break
        if p <= 12000: break          # DFS already run inside find_rc (complete up to its node limit)
    if got and got[0] != 'undecided':
        res[p] = {'g': prim_root(p), 'alpha': got[0], 'beta': {str(i): v for i, v in got[1].items()}, 'how': got[2]}
    else:
        missing.append((p, 'dfs:none' if got is None and p <= 12000 else ('undecided' if got else 'not found')))
    if len(res) % 2000 == 0: print(p, len(res), len(missing), f'{time.time()-t0:.0f}s', flush=True)
json.dump({'D': 6, 'bound': BOUND, 'found': res, 'missing': missing}, open(os.path.join(HERE, 'certs_tl6_all.json'), 'w'))
print('found', len(res), 'missing', missing, f'{time.time()-t0:.0f}s')
