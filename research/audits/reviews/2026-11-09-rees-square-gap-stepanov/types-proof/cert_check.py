"""Independent check of the permanent-weighted type certificate of ../types/sep_types.py.

Runs sep_types.run(k, p) unchanged, captures the complex Fourier array Fh it computes (by
wrapping numpy.fft.fftn), and checks, per prime:

  (I)  exact orbit-average identity
         F(-iota,-iota) = k^(-2k) (k!)^(-2) sum_rho Fh(rho) P(r) P(c),
       P(r) = sum_sigma exp(2 pi i <r, -sigma>/k)  (complex, correct sign);
  (II) the original ratio PW = sum_{rho!=0} |Fh||P(r)||P(c)| / (Fh(0) (k!)^2)   (as sep_types);
  (III) the signed (forced-term) certificate of REPORT.md Sec. 3:
         PW' = [ sum_{one-sided rho!=0} |Fh(rho) + k Fh(0)/n| |P||P|
                + sum_{two-sided} |Fh||P||P| ] / (Fh(0) (k!)^2 (p+1)/n),   n = p + 1 - 2k;
  (IV) per support class (|supp r|, |supp c|): max of n|Fh|/Fh(0) against the proved per-orbit
       Weil bound (m-2) sqrt(p) + 2k - m, and for one-sided classes max |n Fh/Fh(0) + k| against
       (m-2) sqrt(p) + k - m; mean of n Fh/Fh(0) over the class (pair classes: exact -k - R).
Usage: python cert_check.py k p1 p2 ...
"""
import sys, os, math, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'types'))
import sep_types  # noqa: E402

_captured = {}
_orig_fftn = np.fft.fftn


def _fftn(a, *args, **kw):
    out = _orig_fftn(a, *args, **kw)
    _captured['Fh'] = out
    _captured['Ft'] = a
    return out


np.fft.fftn = _fftn


def perm_weights(k):
    allr = np.array(list(itertools.product(range(k), repeat=k)))  # C-order axes r_0..r_{k-1}
    P = np.zeros(len(allr), dtype=complex)
    for sg in itertools.permutations(range(k)):
        Us = np.array([(-sg[i]) % k for i in range(k)])
        P += np.exp(2j * np.pi * ((allr * Us).sum(1) % k) / k)
    return P.reshape((k,) * k)


def check(k, p):
    d = sep_types.run(k, p)
    Fh = _captured['Fh']
    Ft = _captured['Ft']
    n = p + 1 - 2 * k
    kf = math.factorial(k)
    P = perm_weights(k)
    PP = P.reshape((k,) * k + (1,) * k) * P.reshape((1,) * k + (k,) * k)
    F0 = Fh.flat[0].real
    iota = tuple((-i) % k for i in range(k))
    rees = Ft[iota + iota]
    ident = (Fh * PP).sum() / (k ** (2 * k) * kf ** 2)
    nz = d['nz']
    absPP = np.abs(PP)
    PW = (np.abs(Fh) * absPP)[nz].sum() / (F0 * kf ** 2)
    g = np.indices((k,) * (2 * k))
    mr = (g[:k] != 0).sum(0)
    mc = (g[k:] != 0).sum(0)
    one = nz & ((mr == 0) | (mc == 0))
    two = nz & (mr > 0) & (mc > 0)
    corr = np.where(one, np.abs(Fh + k * F0 / n), np.abs(Fh))
    PWs = (corr * absPP)[nz].sum() / (F0 * kf ** 2 * (p + 1) / n)
    # forced-term sum check: sum_{c != 0} P(c) = -k!
    sP = P.sum() - P.flat[0]
    # (V) pair-only signed certificate: subtract the proved main term -k Fh0/n only on pair one-sided classes
    gr = np.indices((k,) * k)
    pairr = ((gr != 0).sum(0) == 2)
    S_pair = P[pairr].sum().real
    pair1 = nz & (((mr == 0) & (mc == 2)) | ((mc == 0) & (mr == 2)))
    corr2 = np.where(pair1, np.abs(Fh + k * F0 / n), np.abs(Fh))
    den2 = F0 * kf ** 2 - 2 * k * F0 * kf * S_pair / n
    PWp = (corr2 * absPP)[nz].sum() / den2
    # (VI) empirical constants of Conjecture OSC (REPORT Sec. 5)
    L = nz & (np.minimum(mr, mc) <= 2)
    H = nz & (np.minimum(mr, mc) >= 3)
    B_L = (p * np.abs(Fh[L]) / (k * F0)).max()
    B_H = (np.abs(Fh[H]) / (k * np.sqrt((mr + mc)[H] * F0))).max() if H.any() else float('nan')
    N1_mu1 = d['C1'] / (d['T1'] * float(k) ** (-(k - 1) ** 2))
    # (VII) row/column permutation invariance of F (transposition and k-cycle on both sides)
    cyc = list(range(1, k)) + [0]
    inv = 0.0
    for ax in ([1, 0] + list(range(2, k)), cyc):
        Fp = np.transpose(Ft, ax + [k + a for a in ax[::-1][::-1]])
        inv = max(inv, np.abs(Fp - Ft).max())
        Fp = np.transpose(Ft, list(range(k)) + [k + a for a in ax])
        inv = max(inv, np.abs(Fp - Ft).max())
    print('   PW_pair=%.4f  B_L=%.3f  B_H=%.3f  N1/mu1=%.3f  max|F(perm)-F|=%.1e' % (PWp, B_L, B_H, N1_mu1, inv))
    print('k=%d p=%d  Rees=%d  identity=%.6f%+.1ei  PW=%.4f  PW_signed=%.4f  sum_{c!=0}P(c)/k!=%.6f'
          % (k, p, round(rees), ident.real, ident.imag, PW, PWs, (sP / kf).real), flush=True)
    sq = math.sqrt(p)
    worst = 0.0
    for a in range(k + 1):
        for b in range(k + 1):
            sel = nz & (mr == a) & (mc == b)
            if not sel.any():
                continue
            m = a + b
            vals = n * Fh[sel] / F0
            amax = np.abs(vals).max()
            bnd = (m - 2) * sq + 2 * k - m
            line = '   (|r|,|c|)=(%d,%d) #=%5d  max n|Fh|/Fh0=%8.3f  [Weil bound %7.2f]' % (a, b, sel.sum(), amax, bnd)
            worst = max(worst, amax / bnd)
            if a == 0 or b == 0:
                dev = np.abs(vals + k).max()
                line += '  max|nFh/Fh0+k|=%7.3f [bound %6.2f]' % (dev, (m - 2) * sq + k - m)
                worst = max(worst, dev / ((m - 2) * sq + k - m) if (m - 2) * sq + k - m > 0 else (0 if dev < 1e-9 else np.inf))
            if m <= 4:
                mv = vals.mean()
                line += '  mean nFh/Fh0=%.4f%+.4fi' % (mv.real, mv.imag)
            wsh = (corr * absPP)[sel].sum() / (F0 * kf ** 2 * (p + 1) / n)
            line += '  PW_signed share %.4f' % wsh
            print(line)
    print('   worst ratio to proved bound: %.4f' % worst, flush=True)


if __name__ == '__main__':
    k = int(sys.argv[1])
    for p in map(int, sys.argv[2:]):
        check(k, p)
