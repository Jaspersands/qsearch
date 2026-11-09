"""Separable-type statistics via the PGL_2 (cross-ratio) normal form.

Every labeled open configuration (alpha, beta) in the affine chart is a labeled point
configuration (S, T, z) on P^1 with z = infinity, s_j = alpha_j, t_i = -beta_i.  Modulo PGL_2 we
normalise s_0 = inf, s_1 = 0, s_2 = 1.  Then (Lemma, report Sec. 2):
  C1 (pattern separable)  <=>  for each j >= 1, ind(s_j - t) is the same for all t in T
                           <=>  T lies in one bucket of t -> (ind(s_j - t))_{j>=1}.
The pattern in the chart z (z -> infinity) is U_i + V_j with
  U_i = -ind(t_i - z),  V_0 = eps,  V_j = eps + g_j - ind(s_j - z),   eps = ind(-1), g_j = ind(s_j - t).
F(U,V) = #{(labeled orbit, z) with pattern = U_i + V_j mod constants}; this equals the F of
sep_types.py (cross-check at k = 3, 4).  T is enumerated unlabeled (sorted) and F is symmetrised
over permutations of U at the end.
Usage: python orbit_types.py k p1 p2 ...
"""
import sys, itertools, math
import numpy as np


def primroot(p):
    fac, n, d = [], p - 1, 2
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


def run(k, p, want_arrays=False):
    g = primroot(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e % k
        x = x * g % p
    eps = int(ind[p - 1])
    K = k ** k
    pw = k ** np.arange(k, dtype=np.int64)
    Facc = np.zeros(K * K, dtype=np.float64)  # index Uidx*K + Vidx (U_i digit i, V_j digit j)
    allz = np.arange(p, dtype=np.int64)
    pts_iter = itertools.permutations(range(2, p), k - 3) if k > 3 else [()]
    for rest in pts_iter:
        S = (0, 1) + tuple(rest)  # s_1..s_{k-1}
        Sarr = np.array(S, dtype=np.int64)
        # profiles of all t
        diff = (Sarr[None, :] - allz[:, None]) % p  # (p, k-1)
        idt = ind[diff]
        okt = (idt >= 0).all(1)
        key = (np.where(idt < 0, 0, idt) * pw[:k - 1]).sum(1)
        key = np.where(okt, key, -1)
        order = np.argsort(key, kind='stable')
        ks = key[order]
        # runs
        bounds = np.flatnonzero(np.diff(ks)) + 1
        starts = np.concatenate([[0], bounds])
        ends = np.concatenate([bounds, [len(ks)]])
        for a, b in zip(starts, ends):
            if ks[a] < 0 or b - a < k:
                continue
            members = order[a:b]  # t values (= index since allz = arange)
            gvec = idt[members[0]]  # g_j for j = 1..k-1
            for T in itertools.combinations(members.tolist(), k):
                Tarr = np.array(T, dtype=np.int64)
                bad = np.zeros(p, dtype=bool)
                bad[Sarr] = True
                bad[Tarr] = True
                zs = allz[~bad]
                Uz = (-ind[(Tarr[None, :] - zs[:, None]) % p]) % k  # (nz, k)
                Vz = np.empty((len(zs), k), dtype=np.int64)
                Vz[:, 0] = eps
                Vz[:, 1:] = (eps + gvec[None, :] - ind[(Sarr[None, :] - zs[:, None]) % p]) % k
                # canonical rep mod shifts: subtract U_0 from U, add to V; subtract V_0 from V (global)
                sh = Uz[:, :1]
                Uc = (Uz - sh) % k
                Vc = (Vz + sh) % k
                Vc = (Vc - Vc[:, :1]) % k
                idx = (Uc * pw).sum(1) * K + (Vc * pw).sum(1)
                Facc += np.bincount(idx, minlength=K * K)
    Fm = Facc.reshape(K, K)
    # symmetrise over permutations of U (T was unlabeled), re-canonicalising U_0 = 0
    allw = np.array(list(itertools.product(range(k), repeat=k)), dtype=np.int64)[:, ::-1]
    Fsym = np.zeros_like(Fm)
    for sg in itertools.permutations(range(k)):
        Up = allw[:, list(sg)]  # U o sigma
        sh = Up[:, :1]
        Upc = (Up - sh) % k
        # moving shift into V: V -> V + sh, then V_0 normalised -> shift cancels globally
        newU = (Upc * pw).sum(1)
        np.add.at(Fsym, newU, Fm)
    # expand to full function on Z_k^{2k}: F(U,V) = Fsym[canon(U,V)]
    U = allw
    Uc = (U - U[:, :1]) % k
    Ui = (Uc * pw).sum(1)
    V = allw
    Vc = (V - V[:, :1]) % k
    Vi = (Vc * pw).sum(1)
    F = Fsym[Ui][:, Vi]
    Ft = F.reshape((k,) * k + (k,) * k)
    Ft = np.transpose(Ft, list(range(k - 1, -1, -1)) + list(range(2 * k - 1, k - 1, -1)))
    Fh = np.fft.fftn(Ft)
    absF = np.abs(Fh)
    F0 = absF.flat[0]
    if F0 < 0.5:
        return None
    rs = (np.indices((k,) * k).sum(0) % k == 0)
    supp = rs.reshape((k,) * k + (1,) * k) & rs.reshape((1,) * k + (k,) * k)
    leak = absF[~supp].max() / F0
    nz = supp.copy()
    nz.flat[0] = False
    L1 = absF[nz].sum() / F0
    om = np.exp(-2j * np.pi / k)
    allr = np.array(list(itertools.product(range(k), repeat=k)))
    Pr = np.zeros(len(allr), dtype=complex)
    for sg in itertools.permutations(range(k)):
        Us = np.array([(-sg[i]) % k for i in range(k)])
        Pr += om ** ((allr * Us).sum(1) % k)
    Pr = np.abs(Pr).reshape((k,) * k)
    W = Pr.reshape((k,) * k + (1,) * k) * Pr.reshape((1,) * k + (k,) * k)
    PW = (absF * W)[nz].sum() / (F0 * math.factorial(k) ** 2)
    iota = tuple((-i) % k for i in range(k))
    Rees = Ft[iota + iota]
    meanF = F.mean()
    out = dict(p=p, Rees=Rees, Rees_mean=Rees / meanF, max_mean=F.max() / meanF, min_mean=F.min() / meanF,
               frac_real=(F > 0.5).mean(), L1=L1, PW=PW, leak=leak, total=F.sum() / k ** 2)
    if want_arrays:
        out.update(absF=absF, nz=nz, F0=F0, W=W)
    return out


if __name__ == '__main__':
    k = int(sys.argv[1])
    print('k p Rees Rees/meanSepType max/mean min/mean fracTypesRealised marginL1 permWeightedL1 leak')
    for p in map(int, sys.argv[2:]):
        d = run(k, p)
        if d is None:
            print(k, p, 'no C1 configurations', flush=True)
            continue
        print(k, p, int(round(d['Rees'])), '%.3g' % d['Rees_mean'], '%.3g' % d['max_mean'], '%.3g' % d['min_mean'],
              '%.4f' % d['frac_real'], '%.4g' % d['L1'], '%.4g' % d['PW'], 'leak=%.1e' % d['leak'], flush=True)
