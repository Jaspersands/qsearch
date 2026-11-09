"""Per-class decay fits of n|Fh|/Fh0 (max and RMS over the class) against p, from analyze2_*.out.
|Fh|/Fh0 ~ p^-(1+s) where s = -slope printed here.  Usage: python class_fit.py pmin [pmax]"""
import sys, os, glob, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
pmin = int(sys.argv[1]); pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
D = {}
for f in glob.glob(os.path.join(HERE, 'analyze2_*.out')):
    for l in open(f):
        if l.startswith('{'):
            d = json.loads(l)
            if not d.get('empty'):
                D[d['p']] = d['classes']
ps = sorted(p for p in D if pmin <= p <= pmax)
print('primes %d..%d (%d)' % (ps[0], ps[-1], len(ps)))
x = np.log(ps)
for c in D[ps[0]]:
    out = []
    for q in ('max', 'rms', 'med'):
        y = np.log([D[p][c][q] for p in ps])
        s, b = np.polyfit(x, y, 1)
        out.append('%s slope %+.2f (value at p=%d: %.3g)' % (q, s, ps[-1], D[ps[-1]][c][q]))
    print('(%s)  ' % c + '   '.join(out))
