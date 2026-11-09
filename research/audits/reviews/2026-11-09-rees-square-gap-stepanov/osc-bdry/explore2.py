import numpy as np, sys
k = 5
d = np.load('class_values_k%d.npz' % k)
ps, ms, V = d['ps'], [tuple(m) for m in d['ms']], d['V']
supp = [sum(1 for x in m if x) for m in ms]
name = lambda m: ''.join(str(x) for x in m if x) or '0'
zero = ms.index(tuple([0]*k))
S3 = [i for i in range(len(ms)) if supp[i] == 3]
S2 = [i for i in range(len(ms)) if supp[i] == 2]
for p in (1021, 1531 if 1531 in ps else 1511, 2011, 2311):
    a = list(ps).index(p)
    print('p=%d' % p)
    print('   f:', '  '.join('%s:%+.2f%+.2fi' % (name(ms[i]), V[a, i, zero].real, V[a, i, zero].imag) for i in S3))
    for i in S3:
        print('  r=%-4s' % name(ms[i]), '  '.join('%+.3f%+.3fi' % (V[a, i, j].real, V[a, i, j].imag) for j in S3))
print('(3,3) mean over p>=1000 and |.| mean')
sel = [a for a, p in enumerate(ps) if p >= 1000]
for i in S3:
    print('  r=%-4s' % name(ms[i]), '  '.join('%+.3f%+.3fi|%.3f' % (V[sel, i, j].mean().real, V[sel, i, j].mean().imag, abs(V[sel, i, j]).mean()) for j in S3))
print('(2,2) mean over p>=1000')
for i in S2:
    print('  r=%-4s' % name(ms[i]), '  '.join('%+.3f%+.3fi|%.3f' % (V[sel, i, j].mean().real, V[sel, i, j].mean().imag, abs(V[sel, i, j]).mean()) for j in S2))
print('(2,3) mean over p>=1000')
for i in S2:
    print('  r=%-4s' % name(ms[i]), '  '.join('%+.3f%+.3fi|%.3f' % (V[sel, i, j].mean().real, V[sel, i, j].mean().imag, abs(V[sel, i, j]).mean()) for j in S3))
