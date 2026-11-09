"""Exact per-multiset-class values n*Fhat(r,c)/Fhat(0) at kappa = 3 (sep_types) or 4 (C kernel of
../osc-k5), for many primes.  Same object and conventions as class_values.py.
Usage: python small_k_values.py k pmax [pmin]   -> class_values_k<k>_wide.npz"""
import sys, os, itertools, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'osc-k5'))
sys.path.insert(0, os.path.join(HERE, '..', 'types'))
k = int(sys.argv[1]); pmax = int(sys.argv[2]); pmin = int(sys.argv[3]) if len(sys.argv) > 3 else 2 * k * k
def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
ps = [p for p in range(pmin, pmax + 1) if isprime(p) and p % k == 1]
ms = sorted({tuple(sorted(v)) for v in itertools.product(range(k), repeat=k) if sum(v) % k == 0})
def Ft_of(p):
    if k == 4:
        import osc_k5
        acc, info, eps = osc_k5.enumerate_acc(k, p, nthreads=2)
        Ft, _ = osc_k5.build_F(k, acc)
        return Ft
    import sep_types
    cap = {}
    orig = np.fft.fftn
    def fftn(a, *x, **kw):
        cap['Ft'] = np.array(a); return orig(a, *x, **kw)
    np.fft.fftn = fftn
    try:
        sep_types.run(k, p)
    finally:
        np.fft.fftn = orig
    return cap.get('Ft')
out_ps, out_V, out_N1 = [], [], []
for p in ps:
    t0 = time.time()
    Ft = Ft_of(p)
    if Ft is None:
        continue
    Fh = np.fft.fftn(Ft); F0 = Fh.flat[0].real
    if F0 < 0.5:
        continue
    n = p + 1 - 2 * k
    out_ps.append(p); out_N1.append(F0 / k ** 2)
    out_V.append(np.array([[n * Fh[r + c] / F0 for c in ms] for r in ms]))
    print(p, '%.1fs' % (time.time() - t0), flush=True)
    np.savez(os.path.join(HERE, 'class_values_k%d_wide.npz' % k), ps=np.array(out_ps), ms=np.array(ms), V=np.array(out_V), N1=np.array(out_N1))
print('saved', len(out_ps))
