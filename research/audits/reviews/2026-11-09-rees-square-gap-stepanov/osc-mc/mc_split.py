"""Class values of the (C1) measure split by partial involution symmetry (companion of mc_classes.py and pairsym.py).
Same sampler, batching and per-configuration Q(R,C) as mc_classes.py (identical random stream: with the same k, p,
nconf and seed the 'all' part reproduces the mc_classes.py run configuration by configuration).  Each configuration
(S, T) is flagged 'structured' if some involution iota of P^1 that swaps two disjoint pairs of S (an involution is
fixed by two of its 2-cycles; C(k,2)C(k-2,2)/2 of them) also has at least two iota-pairs {t, iota(t)} inside T.
Writes three npz files with the keys of mc_classes.py (so k6_spike_survey.analyse reads them): <out>_all.npz,
<out>_str.npz (structured configurations only) and <out>_uns.npz (the rest).  For a part, N1/mu1 is the part's
rate and N_unl the part's share of the unlabelled count (the finite ensemble the noise law refers to).
The share of structured configurations is printed with its S-batch standard error.
Usage: python mc_split.py k p nconf [--seed s] [--batches B] --out prefix"""
import sys, math, itertools, time, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot, tables, pw_estimates
from sym_confs_lib import mob_from, act_factory


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('k', type=int); ap.add_argument('p', type=int); ap.add_argument('nconf', type=int)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--batches', type=int, default=16)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(); k, p = a.k, a.p
    assert (p - 1) % k == 0
    t0 = time.time()
    classes, R, P, orb, rb, supp, canon, base, reps = tables(k)
    nR, nA = P.shape
    name = lambda c: ''.join(str(x) for x in c if x) or '0'
    names = [name(c) for c in classes]
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    chi = ind % k; chi[0] = -1
    xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1)
    act = act_factory(p)
    rng = np.random.default_rng(a.seed)
    B = a.batches
    parts = ('all', 'str', 'uns')
    S1 = {q: np.zeros((B, nR, nR), dtype=complex) for q in parts}
    cnt = {q: np.zeros(B) for q in parts}
    S2 = {q: np.zeros((nR, nR)) for q in parts}
    nS = 0; nconf = 0
    while nconf < a.nconf:
        S = rng.choice(p, k, replace=False)
        nS += 1
        D = (S[None, :] - xs[:, None]) % p
        prof = chi[D]; inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
        bc = np.bincount(key[~inS], minlength=M)
        full = np.flatnonzero(bc >= k)
        if len(full):
            Sl = [int(s) for s in S]
            invs = []
            for (i, j), (u, v) in itertools.combinations(itertools.combinations(range(k), 2), 2):
                if len({i, j, u, v}) == 4:
                    invs.append(mob_from((Sl[i], Sl[j], Sl[u]), (Sl[j], Sl[i], Sl[v])))
        for Bk in full:
            pts = np.flatnonzero(key == Bk)
            pl = [int(t) for t in pts]; sp = set(pl)
            pairsets = []                       # for each involution: the iota-pairs inside the bucket
            for gm in invs:
                im = act(gm, pl)
                prs = {frozenset((t, u)) for t, u in zip(pl, im) if u in sp and u != t}
                if len(prs) >= 2: pairsets.append(prs)
            for Tt in itertools.combinations(pts, k):
                T = np.array(Tt); sT = set(int(t) for t in Tt)
                structured = any(sum(1 for pr in prs if pr <= sT) >= 2 for prs in pairsets)
                mask = np.ones(p, dtype=bool); mask[S] = False; mask[T] = False
                z = xs[mask]
                uref = chi[(T - S[0]) % p]; vref = chi[(S - T[0]) % p]
                U = (chi[(T[None, :] - z[:, None]) % p] - uref[None, :]) % k
                Vv = (chi[(S[None, :] - z[:, None]) % p] - vref[None, :]) % k
                U = np.vstack([U, (-uref)[None, :] % k]); Vv = np.vstack([Vv, (-vref)[None, :] % k])
                cu = np.zeros(len(U), dtype=np.int64); cv = np.zeros(len(U), dtype=np.int64)
                for v in range(k):
                    cu += (U == v).sum(1) * base[v]; cv += (Vv == v).sum(1) * base[v]
                iu = canon[cu]; iv = canon[cv]
                Hc = np.bincount(iu * nA + iv, minlength=nA * nA).reshape(nA, nA).astype(float)
                Q = P @ Hc @ P.T
                b = (nS - 1) % B
                for q in ('all', 'str' if structured else 'uns'):
                    S1[q][b] += Q; cnt[q][b] += 1; S2[q] += np.abs(Q) ** 2
                nconf += 1
        if nS % 200000 == 0:
            print('  S %d conf %d (structured %d)  %.0fs' % (nS, nconf, int(cnt['str'].sum()), time.time() - t0), flush=True)
    n = p + 1 - 2 * k
    ET = nconf / nS
    Nunl = math.comb(p, k) * ET / (p * (p * p - 1)) * (p + 1) / (p + 1 - 2 * k)
    N1 = Nunl * math.factorial(k) ** 2 * (p + 1 - 2 * k)
    T1 = math.prod(range(p - k + 1, p - 1)) * math.prod(range(p - 2 * k + 1, p - k + 1))
    mu1 = T1 * float(k) ** (-(k - 1) ** 2)
    sh_b = cnt['str'] / np.maximum(cnt['all'], 1)
    share = cnt['str'].sum() / nconf
    print('k=%d p=%d lambda=%.3f S=%d conf=%d N1/mu1=%.3f N_unl=%.4g  structured share %.3f (S-batch se %.3f)  elapsed %.0fs' % (
        k, p, p / M, nS, nconf, N1 / mu1, Nunl, share, sh_b.std(ddof=1) / math.sqrt(B), time.time() - t0))
    for q in parts:
        N = cnt[q].sum()
        if N == 0: continue
        sh = N / nconf
        Vh = S1[q].sum(0) / N; Vb = S1[q] / np.maximum(cnt[q], 1)[:, None, None]
        sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
        PWp_d = pw_estimates(k, n, Vh, np.sqrt(np.maximum(sq, 0)), P, orb, rb, supp)[1]
        print('  part %s: %d configurations (share %.3f), N1/mu1 %.3f, PW_pair debiased %.3f' % (q, N, sh, N1 * sh / mu1, PWp_d))
        np.savez('%s_%s.npz' % (a.out, q), k=k, p=p, classes=np.array(classes), names=np.array(names), orb=orb, P=P, rb=rb,
                 supp=supp, S1=S1[q], cnt=cnt[q], S2=S2[q], Hsum=np.zeros((nA, nA)), nS=nS, nconf=int(N), rainbow=0, zsum=0,
                 N1=N1 * sh, mu1=mu1, Nunl=Nunl * sh, kept=np.array([]), keep=np.array(['']))


if __name__ == '__main__':
    main()
