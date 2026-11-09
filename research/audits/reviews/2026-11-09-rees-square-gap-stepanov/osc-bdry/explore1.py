import numpy as np, sys
k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
d = np.load('class_values_k%d.npz' % k)
ps, ms, V, N1 = d['ps'], [tuple(m) for m in d['ms']], d['V'], d['N1']
supp = [sum(1 for x in m if x) for m in ms]
name = lambda m: ''.join(str(x) for x in m if x) or '0'
zero = ms.index(tuple([0]*k))
sel = [i for i, p in enumerate(ps) if p >= 1000] if k == 5 else list(range(len(ps)))
print('primes', [int(ps[i]) for i in sel][:5], '...', len(sel))
print('--- one-sided f(r) = n Fh(r,0)/Fh0, mean over p>=1000 and spread')
for i, m in enumerate(ms):
    if i == zero: continue
    v = V[sel, i, zero]
    print('%-6s s=%d mean=%+.3f%+.3fi  |.|mean=%.3f  std=%.3f  last=%+.3f%+.3fi' % (name(m), supp[i], v.mean().real, v.mean().imag, abs(v).mean(), v.std(), v[-1].real, v[-1].imag))
