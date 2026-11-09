"""Model certificate threshold for k = 4..10 from the measured laws (a model, not a bound).
PW_pair(p) ~ noise(p) + sys(p):
  noise(p) = (sqrt(pi)/2) A'_*^2 / sqrt(n N_unl(p))   [sigma_RC^2 = n/(orb_R orb_C), measured c = 0.97-1.01
             at k = 5, 6; N_unl = rho T1 k^-(k-1)^2 / (k!^2 n), rho = N1/mu1]
  sys(p)   = sum over bins (a,b) of mult A(a) A(b) Vsys(a,b,p) / n
Vsys (two-sided, m = a+b, r = 3900/p): measured at k = 6 on typical primes (3877, 3931, 5839, 7789),
p-decay exponents from the k = 5 exact envelope fits (decay_fit.py):
  m=4: 1.6;  m=5: 0.087 r^0.7;  (2,4): 0.042 r^1.0;  (3,3): 0.068 r^0.6;  m=7: 0.009 r^1.3;
  m=8: 0.008 r^1.6;  m>=9: V9 * q^(m-9) * r^(s (m-4)).
One-sided (0,b): 1.3 r^0.55 (b=3), 0.26 r (b=4), 0.3 (b>=5, conservative).
Variants: spike factor F on all two-sided bins; s; q; kappa growth g^(m-4) with g = k/6.
Weights from weights_k.npz (weights_k.py)."""
import math, numpy as np
w = np.load('weights_k.npz')
def model(k, F=1.0, s=0.4, q=0.6, V9=0.005, kgrow=False, rho=0.8, at=None):
    A = w['A%d' % k]; Ap = w['Ap%d' % k]
    As = Ap.sum() ** 2 - Ap[0] ** 2 - 2 * Ap[0] * Ap[2]
    kf = math.factorial(k)
    def Nunl(p):
        n = p + 1 - 2 * k
        T1 = math.prod(range(p - k + 1, p - 1)) * math.prod(range(p - 2 * k + 1, p - k + 1))
        return rho * T1 * float(k) ** (-(k - 1) ** 2) / (kf ** 2 * n)
    def Vsys(a, b, p):
        r = 3900.0 / p; m = a + b
        if a == 0:
            return {3: 1.3 * r ** 0.55, 4: 0.26 * r}.get(b, 0.3)
        if m == 4: v = 1.6
        elif m == 5: v = 0.087 * r ** 0.7
        elif (a, b) == (2, 4): v = 0.042 * r
        elif (a, b) == (3, 3): v = 0.068 * r ** 0.6
        elif m == 7: v = 0.009 * r ** 1.3
        elif m == 8: v = 0.008 * r ** 1.6
        else: v = V9 * q ** (m - 9) * r ** (s * (m - 4))
        if kgrow: v *= (k / 6.0) ** (m - 4)
        return F * v
    def noise(p):
        n = p + 1 - 2 * k
        return math.sqrt(math.pi) / 2 * As / math.sqrt(n * Nunl(p))
    def sysp(p):
        n = p + 1 - 2 * k; tot = 0.0
        for a in range(k + 1):
            for b in range(a, k + 1):
                if (a, b) in ((0, 0), (0, 2)) or 1 in (a, b): continue
                tot += (1 if a == b else 2) * A[a] * A[b] * Vsys(a, b, p)
        return tot / n
    def cross(f):
        p = 2 * k + 3
        while f(p) > 1: p = int(p * 1.005) + 1
        return p
    if at is not None:
        return noise(at), sysp(at)
    pn, ps, pt = cross(noise), cross(sysp), cross(lambda p: noise(p) + sysp(p))
    return pn, ps, pt
if __name__ == '__main__':
    import sys
    if sys.argv[1:2] == ['at']:          # python model_threshold.py at k p : model noise and sys PW_pair at p
        k, p = int(sys.argv[2]), int(sys.argv[3])
        for label, kw in [('typical', {}), ('spike x4', {'F': 4.0})]:
            nz, sy = model(k, at=p, **kw)
            print('k=%d p=%d %s: model noise %.3f  sys %.3f  total %.3f' % (k, p, label, nz, sy, nz + sy))
        sys.exit()
    lk = lambda p, k: math.log(p) / math.log(k)
    for label, kw in [('typical', {}), ('spike x4', {'F': 4.0}), ('slow decay s=0.25,q=1', {'s': 0.25, 'q': 1.0}),
                      ('k-growth (k/6)^(m-4)', {'kgrow': True}), ('spike x4 + slow decay', {'F': 4.0, 's': 0.25, 'q': 1.0})]:
        print('== %s' % label)
        print('  k   p_noise (log_k)   p_sys (log_k)   p_total (log_k, lambda)   (k+1)/2')
        for k in range(4, 11):
            pn, ps, pt = model(k, **kw)
            print('%3d  %9d (%5.2f)  %9d (%5.2f)  %9d (%5.2f, %.3f)   %.1f' % (
                k, pn, lk(pn, k), ps, lk(ps, k), pt, lk(pt, k), pt / k ** (k - 1), (k + 1) / 2))
