"""Separable-type (margin-class) statistics on the open stratum.

Open stratum: labeled (alpha, beta) in F_p^{2k}, beta distinct, alpha distinct, every cell
alpha_j + beta_i nonzero.  A configuration is "C1" (multiplicatively rank one) iff its index
pattern P_ij = ind(alpha_j + beta_i) is separable: P_ij = U_i + V_j (mod k).

Normalisation: beta_0 = 0, beta_1 = 1 (translation x scaling act freely; unnormalised count
N(U,V) = p * h * F(U,V) with F(U,V) = sum_a M1(U + a, V)).

Outputs per prime:
  T1     = number of normalised open configurations (all patterns)
  C1tot  = number of normalised open C1 configurations
  Rees   = F(-iota, -iota)  (so Rees > 0 iff p notin E_2'(k), the all-nonzero exceptional set)
  muF    = k * T1 / k^(k^2)  (mean of F over all patterns, same normalisation)
  maxF/muF, F(const)/muF, Rees/muF
  margin L1 certificate ratio  sum_{rho != 0} |Fhat(rho)| / Fhat(0)    (< 1 => every separable type realised)
  permanent-weighted Rees certificate ratio  sum_{rho!=0}|Fhat||P(r)||P(c)| / (Fhat(0) (k!)^2)
  RMS of |Fhat(rho)|, rho != 0, relative to sqrt(Fhat(0))
Usage: python sep_types.py k p1 p2 ...
"""
import sys, itertools, math
import numpy as np


def primroot(p):
    fac = []
    n = p - 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g


def run(k, p):
    assert (p - 1) % k == 0
    g = primroot(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e % k
        x = x * g % p
    K = k ** k
    # all bases beta = (0, 1, b2, ..., b_{k-1}) distinct
    rest = [b for b in range(2, p)]
    bases = np.array(list(itertools.permutations(rest, k - 2)), dtype=np.int64) if k > 2 else np.zeros((1, 0), dtype=np.int64)
    nb = bases.shape[0]
    beta = np.concatenate([np.zeros((nb, 1), dtype=np.int64), np.ones((nb, 1), dtype=np.int64), bases], axis=1)
    xs = np.arange(p, dtype=np.int64)
    pw = k ** np.arange(k, dtype=np.int64)
    # U-profile indexing: profile w in Z_k^k -> sum w_i k^i
    allw = np.array(list(itertools.product(range(k), repeat=k)), dtype=np.int64)[:, ::-1]  # w[i]
    widx = (allw * pw).sum(1)
    order = np.argsort(widx)
    allw = allw[order]  # allw[n] is the profile with index n
    shift_perm = []
    for a in range(k):
        sw = (allw + a) % k
        shift_perm.append((sw * pw).sum(1))
    # multiplicity vectors m (compositions of k into k parts) with their V-count
    comps = [m for m in itertools.product(range(k + 1), repeat=k) if sum(m) == k]
    A = np.zeros((K, len(comps)), dtype=np.float64)  # sum over bases of prod_a FF_{m_a}(H[U+a])
    T1 = 0.0
    chunk = max(1, 4000000 // (p * k))
    for s in range(0, nb, chunk):
        bt = beta[s:s + chunk]
        cells = (xs[None, :, None] + bt[:, None, :]) % p  # (nb, p, k)
        ic = ind[cells]
        ok = (ic >= 0).all(axis=2)
        prof = (np.where(ic < 0, 0, ic) * pw).sum(axis=2)
        prof = np.where(ok, prof, K)  # bin K = discarded
        nbc = bt.shape[0]
        flat = prof + (K + 1) * np.arange(nbc)[:, None]
        H = np.bincount(flat.ravel(), minlength=nbc * (K + 1)).reshape(nbc, K + 1)[:, :K].astype(np.float64)
        tot = H.sum(1)
        ff = np.ones_like(tot)
        for t in range(k):
            ff = ff * (tot - t)
        T1 += ff.sum()
        FF = [np.ones_like(H)]
        cur = np.ones_like(H)
        for t in range(k):
            cur = cur * (H - t)
            FF.append(cur.copy())
        for ci, m in enumerate(comps):
            P = np.ones_like(H)
            for a in range(k):
                if m[a]:
                    P = P * FF[m[a]][:, shift_perm[a]]
            A[:, ci] += P.sum(0)
    # expand to M1(U, V) over labeled V
    allV = list(itertools.product(range(k), repeat=k))
    compidx = {m: i for i, m in enumerate(comps)}
    Vcomp = np.array([compidx[tuple(sum(1 for v in V if v == a) for a in range(k))] for V in allV])
    M1 = A[:, Vcomp]  # (K over U, K over V); M1[U, V] counts configs with pattern U_i + V_j
    # F(U,V) = sum_a M1(U+a, V)
    F = sum(M1[shift_perm[a], :] for a in range(k))
    # each config counted k times among (U+a, V-a) representatives in M1; F also sums the scaling shift
    C1tot = M1.sum() / k
    # Fourier over Z_k^{2k}: reshape to (k,)*2k with axis order U_0..U_{k-1}, V_0..V_{k-1}
    # index n = sum w_i k^i -> numpy C-order needs reversed axes
    Ft = F.reshape((k,) * k + (k,) * k)
    Ft = np.transpose(Ft, list(range(k - 1, -1, -1)) + list(range(2 * k - 1, k - 1, -1)))
    Fh = np.fft.fftn(Ft)  # Fh[r, c] = sum F(U,V) e^{-2 pi i (<r,U> + <c,V>)/k}
    absF = np.abs(Fh)
    F0 = absF.flat[0]
    if F0 < 0.5:
        return None
    # support check: Sigma r = Sigma c = 0 mod k
    grids = np.indices((k,) * (2 * k))
    sr = grids[:k].sum(0) % k
    sc = grids[k:].sum(0) % k
    supp = (sr == 0) & (sc == 0)
    leak = absF[~supp].max() / F0 if (~supp).any() else 0.0
    nz = supp.copy()
    nz.flat[0] = False
    L1 = absF[nz].sum() / F0
    rms = math.sqrt((absF[nz] ** 2).mean())
    # permanent weights P(r) = sum_sigma exp(-2 pi i <r, Ustar o sigma>/k), Ustar = -iota
    om = np.exp(-2j * np.pi / k)
    perms = list(itertools.permutations(range(k)))
    allr = np.array(list(itertools.product(range(k), repeat=k)))  # r tuples in C-order of axes r_0..r_{k-1}
    Pr = np.zeros(len(allr), dtype=complex)
    for sg in perms:
        Us = np.array([(-sg[i]) % k for i in range(k)])
        Pr += om ** ((allr * Us).sum(1) % k)
    Pr = np.abs(Pr).reshape((k,) * k)
    W = Pr.reshape((k,) * k + (1,) * k) * Pr.reshape((1,) * k + (k,) * k)
    PW = (absF * W)[nz].sum() / (F0 * math.factorial(k) ** 2)
    iota = tuple((-i) % k for i in range(k))
    def Fval(U, V):
        return Ft[U + V]
    Rees = Fval(iota, iota)
    zero = tuple([0] * k)
    muF = k * T1 / k ** (k * k)
    nreal = (F > 0.5).sum()
    return dict(p=p, T1=T1, C1=C1tot, Rees=Rees, muF=muF, maxF=F.max() / muF, Fconst=Fval(zero, zero) / muF,
                Rees_mu=Rees / muF, minF=F.min() / muF, L1=L1, PW=PW, rms_rel=rms / math.sqrt(F0), leak=leak,
                frac_real=nreal / F.size, absF=absF, nz=nz, F0=F0, W=W)


if __name__ == '__main__':
    k = int(sys.argv[1])
    print('k p  Rees  Rees/muF  maxF/muF  minF/muF  Fconst/muF  fracTypesRealised  marginL1  permWeightedL1  rms|Fhat|/sqrt(Fhat0)  C1/T1*k^((k-1)^2)')
    for p in map(int, sys.argv[2:]):
        d = run(k, p)
        if d is None:
            print(k, p, 'no C1 configurations', flush=True); continue
        print(k, p, int(round(d['Rees'])), '%.3g' % d['Rees_mu'], '%.3g' % d['maxF'], '%.3g' % d['minF'],
              '%.3g' % d['Fconst'], '%.4f' % d['frac_real'], '%.4g' % d['L1'], '%.4g' % d['PW'],
              '%.3g' % d['rms_rel'], '%.3g' % (d['C1'] / d['T1'] * k ** ((k - 1) ** 2)), 'leak=%.1e' % d['leak'], flush=True)
