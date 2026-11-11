#!/usr/bin/env python3
"""Cheap structural statistics of the k-set orbit classification (feas.c output F_k.txt):
projective-point count, pairs {l, 2l}, collinearity profile of the projective points, and
for each functional g the number of labels with <g,l> = +-2 ("bad" values), split by verdict.
usage: analyze10.py F_k.txt"""
import sys, itertools, collections
p = 5
def pnorm(v):
    f = next(x for x in v if x); i = pow(f, p - 2, p); return tuple(x * i % p for x in v)
PTS = sorted(set(pnorm(v) for v in itertools.product(range(p), repeat=3) if any(v)))
LINES = [frozenset(q for q in PTS if sum(a * b for a, b in zip(g, q)) % p == 0) for g in PTS]
def feats(L):
    P = [pnorm(l) for l in L]; cnt = collections.Counter(P)
    npts = len(cnt); pairs = sum(1 for c in cnt.values() if c == 2)
    prof = tuple(sorted((len(set(cnt) & ln) for ln in LINES), reverse=True))
    coll = tuple(x for x in prof if x >= 3)
    bad = [sum(1 for l in L if sum(a * b for a, b in zip(g, l)) % p in (2, 3)) for g in PTS]
    return npts, pairs, coll, min(bad)
by = collections.defaultdict(collections.Counter); tot = collections.Counter()
for line in open(sys.argv[1]):
    tag = line.split()[0]; L = [tuple(int(c) for c in w) for w in line.split('|')[0].split()[1:]]
    npts, pairs, coll, mb = feats(L); tot[tag] += 1
    by['npts', tag][npts] += 1; by['collinear lines (>=3 pts)', tag][coll] += 1; by['min #bad over g', tag][mb] += 1
print('verdicts', dict(tot))
for key in sorted(set(k for k, _ in by)):
    print('==', key)
    vals = sorted(set(v for (k, t), c in by.items() if k == key for v in c), key=str)
    for v in vals:
        print('  %-28s' % (v,), '  '.join('%s %d' % (t, by[key, t][v]) for t in ('INF', 'M', 'SF')))
