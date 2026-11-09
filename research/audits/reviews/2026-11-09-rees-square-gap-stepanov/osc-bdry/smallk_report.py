import numpy as np, sys, itertools
sys.path.insert(0, '.')
from gauss_fit_lib import gammas
k = int(sys.argv[1]); fn = sys.argv[2]; pmin = int(sys.argv[3]) if len(sys.argv) > 3 else 0
d = np.load(fn); ps, ms, V = d['ps'], [tuple(m) for m in d['ms']], d['V']
name = lambda m: ''.join(str(x) for x in m if x) or '0'
supp = [sum(1 for x in m if x) for m in ms]
sel = [a for a, p in enumerate(ps) if p >= pmin]
print('k=%d primes %d..%d (%d)' % (k, ps[sel[0]], ps[sel[-1]], len(sel)))
# per class: mean |v| in lower and upper half of the prime range -> slope
half = len(sel) // 2
lo, hi = sel[:half], sel[half:]
plo, phi = np.exp(np.log(ps[lo]).mean()), np.exp(np.log(ps[hi]).mean())
rows = []
for i, r in enumerate(ms):
    for j, c in enumerate(ms):
        if i == j == ms.index(tuple([0] * k)): continue
        if (supp[i], name(r)) > (supp[j], name(c)): continue
        a, b = np.sqrt((abs(V[lo, i, j]) ** 2).mean()), np.sqrt((abs(V[hi, i, j]) ** 2).mean())
        slope = np.log(b / a) / np.log(phi / plo) if a > 0 and b > 0 else float('nan')
        rows.append((supp[i] + supp[j], supp[i], supp[j], name(r), name(c), a, b, slope, V[hi, i, j].mean()))
rows.sort()
for row in rows:
    print('m=%d (%d,%d) %-5s/%-5s rms_lo=%.3f rms_hi=%.3f slope=%+.2f mean_hi=%+.3f%+.3fi' % (row[:7] + (row[7], row[8].real, row[8].imag)))
