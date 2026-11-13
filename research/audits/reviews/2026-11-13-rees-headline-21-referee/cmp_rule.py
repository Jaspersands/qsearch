"""Compare per-(p,kappa) degrees of rule_ref.py (referee) with the author's rule.py (imported read-only)."""
import os, sys, json
import rule_ref as R
sys.path.insert(0, R.SRC)
import rule as A
A.CERTS = A.load_certs()
raw = json.load(open(os.path.join(R.SRC, 'tierB.json')))
for k, v in raw.items():
    p, kappa, kind = k.split('|'); A.TIERB[(int(p), int(kappa), kind)] = v
lim = int(sys.argv[1]); dis = []; n = 0
for p in R.sieve(lim):
    if p < 3: continue
    e1, _ = R.degrees(p); e2 = A.degrees(p)
    for k in e1:
        n += 1
        if e1[k] != e2[k][0]: dis.append((p, k, e1[k], e2[k]))
print('pairs', n, 'disagreements', len(dis), dis[:20])
