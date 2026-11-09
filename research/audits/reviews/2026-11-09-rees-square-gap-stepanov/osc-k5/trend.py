"""Drift fits over p >= pmin (default 421) from the osc_k5.py *.out files in this folder.
For each quantity Q(p), least-squares slope of log Q against log p, plus min / median / max.
H constants per total support m: B_H(m) = max over non-pair classes with |r|+|c| = m of
|Fh| sqrt(N1) / (sqrt(m) Fh0);  L-type: n|Fh|/(k Fh0) maximised over the same classes.
Usage: python trend.py [pmin]"""
import sys, os, glob, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
pmin = int(sys.argv[1]) if len(sys.argv) > 1 else 421
rows, cls = {}, {}
for f in sorted(glob.glob(os.path.join(HERE, '*.out'))):
    last = None
    for line in open(f):
        line = line.strip()
        if line.startswith('{"k": 5'):
            d = json.loads(line)
            last = d['p']
            if d['N1'] > 0:
                rows[last] = d
                cls[last] = []
            else:
                last = None
        elif line.startswith('CLASS') and last:
            cls[last].append(json.loads(line[6:]))
ps = sorted(p for p in rows if p >= pmin)
print('primes used (%d): %s' % (len(ps), ps))


def fit(name, vals):
    x = np.log(np.array(ps, float))
    y = np.log(np.array(vals, float))
    s = np.polyfit(x, y, 1)[0]
    print('%-34s slope d log/d log p = %+.2f   min %.4g  median %.4g  max %.4g' % (name, s, min(vals), np.median(vals), max(vals)))


for key in ('PW', 'PW_pair', 'N1_mu1', 'B_L', 'B_H'):
    fit(key, [rows[p][key] for p in ps])
for m in range(5, 11):
    bh = [max(r['max_H'] for r in cls[p] if r['r'] + r['c'] == m and sorted((r['r'], r['c'])) != [0, 2]) for p in ps]
    bl = [max(r['max_n_absF'] / 5 for r in cls[p] if r['r'] + r['c'] == m and sorted((r['r'], r['c'])) != [0, 2]) for p in ps]
    fit('B_H(m=%d)' % m, bh)
    fit('max n|Fh|/(k Fh0), m=%d' % m, bl)
bh7 = [max(r['max_H'] for r in cls[p] if r['r'] + r['c'] >= 7) for p in ps]
fit('B_H restricted to m>=7', bh7)
ball = [max(r['max_n_absF'] / 5 for r in cls[p] if sorted((r['r'], r['c'])) != [0, 2]) for p in ps]
fit('B_all (all non-pair, n-normalised)', ball)
print()
below = [p for p in sorted(rows) if rows[p]['PW'] < 1]
belowp = [p for p in sorted(rows) if rows[p]['PW_pair'] < 1]
print('PW < 1 at:', below)
print('PW >= 1 at p >= 600:', [p for p in sorted(rows) if p >= 600 and rows[p]['PW'] >= 1])
print('PW_pair < 1 at:', belowp)
print('PW_pair >= 1 at p >= 600:', [p for p in sorted(rows) if p >= 600 and rows[p]['PW_pair'] >= 1])
print('Rees = 0 at:', [p for p in sorted(rows) if rows[p]['Rees'] == 0], '; no C1 configuration at:',
      sorted(set(int(json.loads(l)['p']) for f in glob.glob(os.path.join(HERE, '*.out')) for l in open(f)
                 if l.startswith('{"k": 5') and json.loads(l)['N1'] == 0)))
