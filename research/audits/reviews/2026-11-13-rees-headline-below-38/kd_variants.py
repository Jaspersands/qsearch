"""Maxima with and without Lemmas K, D (2026-11-13-rees-linear-arity.md, proved pending referee).
Variants: core+KD (Schedule 1H plus K and D only), ours (fragment), ours+KD."""
import json, math, os
import rule
from certs import primes_upto
rule.CERTS = rule.load_certs()
raw = json.load(open('tierB.json'))
for k, v in raw.items():
    p, kappa, kind = k.split('|'); rule.TIERB[(int(p), int(kappa), kind)] = v
LIM = 30000
def run(new, kd):
    rule.USE_KD = kd
    best = {c: [0, []] for c in range(2, 10)}
    for p in primes_upto(LIM):
        if p < 3: continue
        e = rule.degrees(p, new=new, tierB=new)
        for c in range(2, 10):
            if p <= c: continue
            v = rule.E_of(e, p, c)
            if v > best[c][0]: best[c] = [v, [p]]
            elif v == best[c][0]: best[c][1].append(p)
    return best
for name, new, kd in (('core+K+D', False, True), ('ours', True, False), ('ours+K+D', True, True)):
    b = run(new, kd)
    print(name, 'p <', LIM, {c: (v[0], v[1][:10]) for c, v in b.items()}, flush=True)
# tails (p > 26244 and above all thresholds): degree per kappa depends only on kappa
for name, tail in (('core+K+D', {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 3, 7: 4, 8: 4, 9: 5}),
                   ('ours / ours+K+D', rule.TAIL)):
    out = {}
    for c in range(2, 10):
        vals = [(1 + sum(tail[math.gcd(d, (r - 1) or 2520)] for d in range(2, c + 1)), r)
                for r in range(1, 2521) if math.gcd(r, 2520) == 1]
        m = max(v for v, _ in vals); out[c] = (m, [r for v, r in vals if v == m][:4])
    print('tail', name, out)
