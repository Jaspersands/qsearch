"""Permanent weights of the type certificate by support, for k = 3..kmax.
For each sum-zero multiset R of size k over Z_k (a class), orb_R = k!/prod(mult!), and
W_R = |per(zeta^{R_i l})_{i,l}| / k!  (rainbow column l = 0..k-1; Glynn's formula, vectorised).
Per support j (number of nonzero entries) prints A(j) = sum orb_R W_R and A'(j) = sum sqrt(orb_R) W_R.
Bin weights of PW are A(m_R) A(m_C); the noise-only PW uses A'(m_R) A'(m_C) (sigma_RC^2 ~ n/(orb_R orb_C)).
Writes weights_k.npz.  Usage: python weights_k.py kmax"""
import sys, math, itertools, numpy as np
kmax = int(sys.argv[1])
out = {}
for k in range(3, kmax + 1):
    zeta = np.exp(2j * np.pi / k)
    cls = [c for c in itertools.combinations_with_replacement(range(k), k) if sum(c) % k == 0]
    Rm = np.array(cls, dtype=np.int64)                       # (ncls, k)
    l = np.arange(k)
    D = np.array([(1,) + d for d in itertools.product((1, -1), repeat=k - 1)], dtype=np.float64)
    sgn = D.prod(1)
    per = np.empty(len(cls), dtype=complex)
    B = max(1, int(4e7 // (len(D) * k * 16)))
    for s in range(0, len(cls), B):
        M = zeta ** ((Rm[s:s + B, :, None] * l[None, None, :]) % k)   # (b, k, k)
        A = np.einsum('di,bil->bdl', D, M)
        per[s:s + B] = (A.prod(2) * sgn[None, :]).sum(1) / 2 ** (k - 1)
    W = np.abs(per) / math.factorial(k)
    orb = np.array([math.factorial(k) / math.prod(math.factorial(c.count(v)) for v in set(c)) for c in cls])
    supp = (Rm != 0).sum(1)
    Aj = np.array([(orb * W)[supp == j].sum() for j in range(k + 1)])
    Apj = np.array([(np.sqrt(orb) * W)[supp == j].sum() for j in range(k + 1)])
    out['A%d' % k] = Aj; out['Ap%d' % k] = Apj
    tot = Aj.sum() ** 2 - Aj[0] ** 2
    print('k=%d classes=%d  W_tot=%.4g  A(j): %s' % (k, len(cls), tot, ' '.join('%.3g' % x for x in Aj)), flush=True)
    print('      A\'(j): %s' % ' '.join('%.3g' % x for x in Apj), flush=True)
np.savez('weights_k.npz', **out)
