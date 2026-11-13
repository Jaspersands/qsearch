"""v2: second check of v2/certs_tl6.json with the membership test of verify_all.py (coset test
(x g^{-m})^{(p-1)/D} = 1, generator recomputed), plus 3 perturbed negative controls."""
import json, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, '..'))
src = open('verify_all.py').read().split("C = json.load")[0]
exec(src)                                   # defines lpr, in_coset, ok (read-only reuse)
C = json.load(open(os.path.join(HERE, 'certs_tl6.json')))['two-level 6 (p=1 mod 2520)']
good = bad = 0
for ps, w in C['found'].items():
    p = int(ps); beta = {int(i): v for i, v in w['beta'].items()}
    if ok(p, w['g'], 6, list(range(6)), [0], w['alpha'], beta): good += 1
    else: bad += 1; print('REJECTED', p)
print('TL6 certificates (p = 1 mod 2520, p < 837384):', good, 'accepted,', bad, 'rejected; missing', C['missing'])
random.seed(7); caught = 0
items = list(C['found'].items())[:3]
for ps, w in items:
    p = int(ps); beta = {int(i): v for i, v in w['beta'].items()}; al = list(w['alpha'])
    al[random.randrange(6)] = (al[0] + 1) % p
    caught += not ok(p, w['g'], 6, list(range(6)), [0], al, beta)
print('perturbed controls caught:', caught, '/ 3')
