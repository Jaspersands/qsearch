"""Scratch: fit log N1/mu1 = a + b log symR + c log lambda on the finished runs; predict the rest (written before they finish)."""
import sys, glob, re, datetime
import numpy as np
sys.path.insert(0, '.')
sym = {}
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): sym[int(w[0])] = (float(w[1]), float(w[3]))
meas = {}
for f in glob.glob('survey/mc_k6_p*_s13.log') + ['mc_k6_p1933_s11.log', 'mc_k6_p2347_s11.log', 'mc_k6_p3877_sb.log', 'mc_k6_p4219_s11.log']:
    try:
        for line in open(f):
            m = re.search(r'p=(\d+) lambda=([\d.]+) S=(\d+) conf=(\d+).*N1/mu1=([\d.]+)', line)
            if m: meas[int(m.group(1))] = float(m.group(5))
    except FileNotFoundError: pass
fit = sorted(q for q in meas if q in sym)
X = np.array([[1, np.log(sym[q][1]), np.log(sym[q][0])] for q in fit]); y = np.log([meas[q] for q in fit])
coef, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ coef
print(datetime.datetime.now().isoformat(timespec='minutes'), 'fit on %d primes: log N1/mu1 = %.3f %+.3f log symR %+.3f log lambda; residual sd %.3f' % (len(fit), *coef, r.std()))
print('in-sample: ' + ' '.join('%d:%.2f/%.2f' % (q, meas[q], np.exp(X[i] @ coef)) for i, q in enumerate(fit)))
todo = sorted(q for q in sym if q not in meas)
pred = {q: float(np.exp(np.array([1, np.log(sym[q][1]), np.log(sym[q][0])]) @ coef)) for q in todo}
print('predicted N1/mu1 for the %d unfinished survey primes:' % len(todo))
print(' '.join('%d:%.2f' % (q, pred[q]) for q in todo))
