"""Post-process halflines7.out: for every set, does it carry a nonzero S-valued linear functional
(then 'SAT' is only an S-witness, no gain)? Tally SAT-without-S-functional by (full, half) lines."""
import sys, os, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bt import setup, has_S_functional, powers
p = int(sys.argv[1]); f = sys.argv[2]
P = powers(p, 2); r = next(x for x in range(2, p) if x not in P)
pts = [(1, x) for x in range(p)] + [(0, 1)]
reps = {}
for i, u in enumerate(pts):
    reps[2 * i] = u; reps[2 * i + 1] = tuple((r * x) % p for x in u)
ctx = setup(p, 2, 2, 2)
tally = {}; maxlines = {}
for line in open(f):
    m = re.match(r'\s+m=(\d+) halflines=(\d+) classes=\[(.*?)\] orbit=(\d+): (\w+)', line)
    if not m: continue
    full, half, cl, osz, res = int(m[1]), int(m[2]), [int(x) for x in m[3].split(',') if x.strip()], int(m[4]), m[5]
    L = [tuple((lam * x) % p for x in reps[c]) for c in cl for lam in P]
    sf = has_S_functional(ctx, L) is not None if L else False
    key = (full, half, res, 'Sfunc' if sf else 'noSfunc')
    tally[key] = tally.get(key, 0) + 1
    if res == 'SAT' and not sf:
        maxlines[full] = max(maxlines.get(full, -1), full + half)
for k in sorted(tally): print(k, tally[k])
print('max total lines (full+half) among SAT sets without S-functional, by #full:', maxlines)
