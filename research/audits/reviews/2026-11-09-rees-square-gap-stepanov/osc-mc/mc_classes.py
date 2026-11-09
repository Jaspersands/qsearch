"""Monte Carlo class values V(R,C) = n*Fhat(R,C)/Fhat(0) of the Schedule 2 separable-type
distribution, with per-configuration statistics.  Works for any k (tested k = 5 against the exact
osc-k5 arrays).

C1 measure (uniform on (C1) pairs): S a uniform k-subset of F_p; T any k-subset of a full S-bucket
(points with equal S-profile ind(s_j - x) mod k, modulo the diagonal).  By PGL_2 invariance this is
the orbit average of osc-k5 (z runs over P^1 minus S u T, including infinity).
Normalised types: U_i(z) = ind(t_i - z) - ind(t_i - s_ref), V_j(z) = ind(s_j - z) - ind(s_j - t_ref)
(mod k); at z = inf, U_i = -ind(t_i - s_ref), V_j = -ind(s_j - t_ref).  For sum-zero R the mode
zeta^<R,U> does not depend on s_ref (C1), and the labelled average over relabellings of T is
Sym_R(U) = per(zeta^{R_i U_j}) / k!, a function of the multiset of U.  So for one configuration
Q(R,C) = sum_z Sym_R(U(z)) Sym_C(V(z)) and V(R,C) = E_C1 Q(R,C).
Convention check: V_here(R,C) matches the osc-k5 values V_exact(R,C) directly (k = 5, p = 401).

Usage: python mc_classes.py k p nconf [--seed s] [--batches B] [--out file.npz]
Writes an npz with the classes, orbit sizes, permanent weights, the batch sums of Q, sum |Q|^2,
counts, N1 estimate, and prints PW / PW_pair estimates (naive and split-batch debiased).
"""
import sys, math, itertools, time, argparse
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


def tables(k):
    classes = sorted({tuple(sorted(v)) for v in itertools.combinations_with_replacement(range(k), k) if sum(v) % k == 0})
    comps = [a for a in itertools.product(range(k + 1), repeat=k) if sum(a) == k]
    base = (k + 1) ** np.arange(k)
    code = lambda a: int(np.dot(a, base))
    canon_of = {}
    reps = []
    for a in comps:
        rots = [tuple(a[(v + s) % k] for v in range(k)) for s in range(k)]
        c = min(rots)
        if c not in canon_of:
            canon_of[c] = len(reps)
            reps.append(c)
        canon_of[a] = canon_of[c]
    canon = np.full((k + 1) ** k, -1, dtype=np.int64)
    for a in comps:
        canon[code(a)] = canon_of[a]
    reps = np.array(reps)
    R = np.array(classes)
    zeta = np.exp(2j * np.pi / k)
    dl = np.array(list(itertools.product([1, -1], repeat=k - 1)))
    dl = np.hstack([np.ones((len(dl), 1)), dl])
    sgn = dl.prod(1)
    E = zeta ** ((R[:, :, None] * np.arange(k)[None, None, :]) % k)     # nR x i x v
    A = np.einsum('di,riv->drv', dl, E)                                  # nD x nR x v
    per = np.zeros((len(R), len(reps)), dtype=complex)
    for d in range(len(dl)):
        t = np.ones((len(R), len(reps)), dtype=complex)
        for v in range(k):
            t *= A[d][:, v][:, None] ** reps[None, :, v]
        per += sgn[d] * t
    per /= 2 ** (k - 1)
    P = per / math.factorial(k)
    orb = np.array([math.factorial(k) // math.prod(math.factorial(list(c).count(v)) for v in range(k)) for c in classes])
    rb = canon_of[tuple([1] * k)]
    supp = np.array([sum(1 for x in c if x) for c in classes])
    return classes, R, P, orb, rb, supp, canon, base, reps


def pw_estimates(k, n, Vh, Vabs, P, orb, rb, supp):
    """PW and PW_pair from class values (|V| supplied separately, e.g. debiased)."""
    kf = math.factorial(k)
    W = np.abs(P[:, rb])
    w2 = (orb * W)[:, None] * (orb * W)[None, :]
    z0 = int(np.flatnonzero(supp == 0)[0])
    nz = np.ones_like(w2, dtype=bool)
    nz[z0, z0] = False
    PW = (w2 * Vabs)[nz].sum() / n
    pair = supp == 2
    S_pair = (orb[pair] * (P[pair, rb] * kf)).sum().real          # sum over pair vectors of per
    corr = Vabs.copy()
    pr = np.zeros_like(nz)
    pr[pair, z0] = True
    pr[z0, pair] = True
    corr[pr] = np.abs(Vh[pr] + k)
    den = 1 - 2 * k * S_pair / (n * kf)
    PWp = (w2 * corr)[nz].sum() / n / den
    return PW, PWp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('k', type=int)
    ap.add_argument('p', type=int)
    ap.add_argument('nconf', type=int)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--batches', type=int, default=16)
    ap.add_argument('--out', default=None)
    ap.add_argument('--keep', default='', help='comma list of class-pair names r/c to keep per config')
    a = ap.parse_args()
    k, p = a.k, a.p
    assert (p - 1) % k == 0
    t0 = time.time()
    classes, R, P, orb, rb, supp, canon, base, reps = tables(k)
    nR, nA = P.shape
    name = lambda c: ''.join(str(x) for x in c if x) or '0'
    names = [name(c) for c in classes]
    keep = [tuple(names.index(x) for x in s.split('/')) for s in a.keep.split(',') if s]
    g = primroot(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e
        x = x * g % p
    chi = ind % k
    chi[0] = -1
    xs = np.arange(p)
    kp = k ** np.arange(k - 1)
    M = k ** (k - 1)
    rng = np.random.default_rng(a.seed)
    B = a.batches
    S1 = np.zeros((B, nR, nR), dtype=complex)
    cnt = np.zeros(B)
    S2 = np.zeros((nR, nR))
    Hsum = np.zeros((nA, nA))
    kept = []
    nS = 0
    nconf = 0
    rainbow = 0
    zsum = 0
    while nconf < a.nconf:
        S = rng.choice(p, k, replace=False)
        nS += 1
        D = (S[None, :] - xs[:, None]) % p
        prof = chi[D]
        inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp
        key[inS] = -1
        bc = np.bincount(key[~inS], minlength=M)
        full = np.flatnonzero(bc >= k)
        for Bk in full:
            pts = np.flatnonzero(key == Bk)
            for Tt in itertools.combinations(pts, k):
                T = np.array(Tt)
                mask = np.ones(p, dtype=bool)
                mask[S] = False
                mask[T] = False
                z = xs[mask]
                uref = chi[(T - S[0]) % p]
                vref = chi[(S - T[0]) % p]
                U = (chi[(T[None, :] - z[:, None]) % p] - uref[None, :]) % k
                Vv = (chi[(S[None, :] - z[:, None]) % p] - vref[None, :]) % k
                U = np.vstack([U, (-uref)[None, :] % k])
                Vv = np.vstack([Vv, (-vref)[None, :] % k])
                cu = np.zeros(len(U), dtype=np.int64)
                cv = np.zeros(len(U), dtype=np.int64)
                for v in range(k):
                    cu += (U == v).sum(1) * base[v]
                    cv += (Vv == v).sum(1) * base[v]
                iu = canon[cu]
                iv = canon[cv]
                Hc = np.bincount(iu * nA + iv, minlength=nA * nA).reshape(nA, nA).astype(float)
                Q = P @ Hc @ P.T
                b = nconf % B
                S1[b] += Q
                cnt[b] += 1
                S2 += np.abs(Q) ** 2
                Hsum += Hc
                rainbow += int(Hc[rb, rb])
                zsum += len(U)
                if keep:
                    kept.append([Q[i, j] for i, j in keep])
                nconf += 1
        if nS % 20000 == 0:
            print('  S %d conf %d  %.0fs' % (nS, nconf, time.time() - t0), flush=True)
    N = cnt.sum()
    Vh = S1.sum(0) / N
    Vb = S1 / cnt[:, None, None]
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
    Vdb = np.sqrt(np.maximum(sq, 0))
    sig = np.sqrt(np.maximum(S2 / N - np.abs(Vh) ** 2, 0))
    n = p + 1 - 2 * k
    PW_n, PWp_n = pw_estimates(k, n, Vh, np.abs(Vh), P, orb, rb, supp)
    PW_d, PWp_d = pw_estimates(k, n, Vh, Vdb, P, orb, rb, supp)
    ET = nconf / nS
    Nunl = math.comb(p, k) * ET / (p * (p * p - 1)) * (p + 1) / (p + 1 - 2 * k)
    N1 = Nunl * math.factorial(k) ** 2 * (p + 1 - 2 * k)   # = Fhat(0)/k^2 of osc-k5
    T1 = math.prod(range(p - k + 1, p - 1)) * math.prod(range(p - 2 * k + 1, p - k + 1))
    mu1 = T1 * float(k) ** (-(k - 1) ** 2)
    print('k=%d p=%d lambda=%.3f S=%d conf=%d (%.4f per S)  N1_est=%.4g N1/mu1=%.3f  N_unl=%.4g' % (
        k, p, p / M, nS, nconf, ET, N1, N1 / mu1, Nunl))
    print('  rainbow z per conf %.4g (Rees est = N1 * that / k!^2 * k^2 ... see npz)' % (rainbow / nconf))
    print('  PW naive %.3f  debiased %.3f   PW_pair naive %.3f  debiased %.3f   elapsed %.0fs' % (
        PW_n, PW_d, PWp_n, PWp_d, time.time() - t0), flush=True)
    out = a.out or 'mc_k%d_p%d_s%d.npz' % (k, p, a.seed)
    np.savez(out, k=k, p=p, classes=np.array(classes), names=np.array(names), orb=orb, P=P, rb=rb, supp=supp,
             S1=S1, cnt=cnt, S2=S2, Hsum=Hsum, nS=nS, nconf=nconf, rainbow=rainbow, zsum=zsum, N1=N1, mu1=mu1,
             Nunl=Nunl, kept=np.array(kept), keep=np.array([a.keep]))


if __name__ == '__main__':
    main()
