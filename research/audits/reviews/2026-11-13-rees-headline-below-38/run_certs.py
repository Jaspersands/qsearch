"""Stage 1: certificates for the steps used at every prime below the existence thresholds.
Run: nice -n 19 /opt/anaconda3/bin/python run_certs.py   (writes certs_stage1.json)"""
import json, sys, time
from certs import find_rc, primes_upto, prim_root
TASKS = [  # name, D, R, K list (alternatives), bound (exclusive)
    ('two-level 3', 3, [0, 1, 2], [[0]], 430),
    ('two-level 4', 4, [0, 1, 2, 3], [[0]], 9395),
    ('two-level 5', 5, [0, 1, 2, 3, 4], [[0]], 99745),
    ('tower (9;{0,3,6})', 9, [0, 3, 6], [[0]], 1124521),
    ('union (7;Z7->{0,m})', 7, list(range(7)), [[0, m] for m in range(1, 7)], 1995734),
]
out = {}
t0 = time.time()
for name, D, R, Ks, bound in TASKS:
    res, missing = {}, []
    for p in primes_upto(bound - 1):
        if p < 3 or (p - 1) % D: continue
        got = None
        for K in Ks:
            got = find_rc(p, D, R, K)
            if got and got[0] != 'undecided':
                res[p] = {'g': prim_root(p), 'K': K, 'alpha': got[0], 'beta': {str(i): v for i, v in got[1].items()}, 'how': got[2]}
                break
        if p not in res: missing.append((p, None if got is None else 'undecided'))
    out[name] = {'D': D, 'R': R, 'bound': bound, 'found': res, 'missing': missing}
    print(name, 'found', len(res), 'missing', missing[:60], len(missing), f'{time.time()-t0:.0f}s', flush=True)
json.dump(out, open('certs_stage1.json', 'w'))
