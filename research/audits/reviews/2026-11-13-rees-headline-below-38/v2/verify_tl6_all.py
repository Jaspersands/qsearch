"""v2: second check of v2/certs_tl6_all.json (membership test of verify_all.py, generator recomputed)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, '..'))
exec(open('verify_all.py').read().split("C = json.load")[0])
C = json.load(open(os.path.join(HERE, 'certs_tl6_all.json')))
good = bad = 0
for ps, w in C['found'].items():
    p = int(ps); beta = {int(i): v for i, v in w['beta'].items()}
    if ok(p, w['g'], 6, list(range(6)), [0], w['alpha'], beta): good += 1
    else: bad += 1; print('REJECTED', p)
m2520 = [p for p, _ in C['missing'] if p % 2520 == 1]
print('TL6 all p = 1 mod 6 below 837384:', good, 'accepted,', bad, 'rejected;', len(C['missing']), 'missing (max', max(p for p, _ in C['missing']), '); missing = 1 mod 2520:', m2520)
