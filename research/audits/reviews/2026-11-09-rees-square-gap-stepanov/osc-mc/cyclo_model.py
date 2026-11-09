"""Size-biased-bucket model for one-sided support-3 classes.

For c supported on three S-points with values (a, b, -a-b), the c-mode of x depends only on its
class (ind w, ind(w-1)) mod k, w the Moebius image sending the three points to 0, 1, inf.  Class
sizes are the cyclotomic numbers A_ij of order k (S-independent up to relabelling).  If the full
T-bucket sits in class (i,j) with probability proportional to (A_ij)_k, then
    V(0,c) = sum_ij (A_ij)_k [sum_i'j' A_i'j' zeta^{a(i'-i)+b(j'-j)}] / sum_ij (A_ij)_k - k - b_S.
At k = 3 (support = k) this is exact with b_S = 0.  For k > 3 the weight (A_ij)_k is a heuristic
(the other k-3 profile coordinates treated as independent and uniform).
Compares with the exact class values in ../osc-bdry/class_values_k*.npz (b_S omitted)."""
import sys, numpy as np, itertools
sys.path.insert(0, '../osc-bdry')
from gauss_fit_lib import load  # noqa: E402
sys.path.insert(0, '../osc-k5')
from osc_k5 import primroot  # noqa: E402


def cyclo(p, k):
    g = primroot(p)
    ind = np.zeros(p, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e
        x = x * g % p
    w = np.arange(2, p)
    A = np.zeros((k, k))
    np.add.at(A, (ind[w] % k, ind[w - 1] % k), 1)
    return A


def ff(x, k):
    return np.prod([x - i for i in range(k)], axis=0)


def model(p, k, a, b):
    A = cyclo(p, k)
    W = ff(A, k)
    zeta = np.exp(2j * np.pi / k)
    I = np.arange(k)
    ph = zeta ** ((a * I[:, None] + b * I[None, :]) % k)        # zeta^{a i + b j}
    mode = (A * ph).sum()                                       # sum_i'j' A zeta^{a i' + b j'}
    return (W * np.conj(ph)).sum() * mode / W.sum() - k


files = {3: 'class_values_k3_wide.npz', 4: 'class_values_k4_wide.npz', 5: 'class_values_k5.npz'}
for k in map(int, sys.argv[1:] or ['3', '4', '5']):
    d = np.load('../osc-bdry/' + files[k])
    ps, ms, V = d['ps'], [tuple(m) for m in d['ms']], d['V']
    name = lambda m: ''.join(str(x) for x in m if x) or '0'
    names = [name(m) for m in ms]
    s3 = [i for i, m in enumerate(ms) if sum(1 for x in m if x) == 3]
    z0 = names.index('0')
    errs, mags = [], []
    rows = []
    for t, p in enumerate(ps):
        for i in s3:
            nzv = [x for x in ms[i] if x]
            best = None
            for a, b in itertools.permutations(nzv, 2):
                pass
            # mode values (a, b, -a-b) on (s1, s2, s3): use the first two nonzero values in a fixed order
            a, b = nzv[0], nzv[1]
            mv = model(int(p), k, a, b)
            ve = V[t, z0, i]
            # the class is symmetric in the three points; try the conjugate/permutation conventions
            cands = [model(int(p), k, x, y) for x, y in itertools.permutations(nzv, 2)]
            err = min(abs(c - ve) for c in cands + [np.conj(c) for c in cands])
            errs.append(err); mags.append(abs(ve))
            rows.append((int(p), names[i], ve, cands[0]))
    errs, mags = np.array(errs), np.array(mags)
    print('k=%d: %d (prime, class) pairs; median |V_exact| %.3f, median |model-exact| %.3g, max %.3g' % (
        k, len(errs), np.median(mags), np.median(errs), errs.max()))
    for r in rows[:6] + rows[-6:]:
        print('   p=%d %-4s exact %+.3f%+.3fi  model %+.3f%+.3fi' % (r[0], r[1], r[2].real, r[2].imag, r[3].real, r[3].imag))
