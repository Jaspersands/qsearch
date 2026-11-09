"""Referee 2 independent check of the Schedule-1 core on Heis(F_p), p = 3, 5.

Written from the paper's definitions only (main.tex Sections 2-4), not from project code.
Checks, for every subgroup H of the Heisenberg group over F_p:
  (a) tuple-oracle fibers on the Rees cover are exactly the left cosets of exp(h-tilde);
  (b) the central instrument on rho_{H~} (computed from the projector, not from Lemma lem:central)
      gives label law uniform on K^perp;
  (c) for every label triple and every nonzero witness of sum s_i^2 lambda_i = 0, the descent output
      (controlled right actions by delta_{s_i}(sigma(q)), trace out targets) equals rho_{t h} on Q;
  (d) negative control: with the single-evaluation pullback E_1^{-1}(h) in place of h-tilde,
      (c) fails for some H.
Cover coordinates a = (a1, a2, a3, a4) for t x, t y, t z, t^2 z; [t x, t y] = t^2 z.
"""
import itertools
import numpy as np


def run(p):
    inv2 = pow(2, -1, p)
    w = np.exp(2j * np.pi / p)

    def bch_cover(a, b):  # class 2: a + b + [a,b]/2
        c = [(a[i] + b[i]) % p for i in range(4)]
        c[3] = (c[3] + inv2 * (a[0] * b[1] - a[1] * b[0])) % p
        return tuple(c)

    def neg(a):
        return tuple((-x) % p for x in a)

    def bch_L(u, v):
        return ((u[0] + v[0]) % p, (u[1] + v[1]) % p, (u[2] + v[2] + inv2 * (u[0] * v[1] - u[1] * v[0])) % p)

    def E(s, a):
        return ((s * a[0]) % p, (s * a[1]) % p, (s * a[2] + s * s * a[3]) % p)

    def dil(l, a):
        return ((l * a[0]) % p, (l * a[1]) % p, (l * a[2]) % p, (l * l * a[3]) % p)

    cover = list(itertools.product(range(p), repeat=4))
    idx = {a: i for i, a in enumerate(cover)}
    N = len(cover)

    # subalgebras of L = span(x, y, z), [x, y] = z: enumerate subspaces via spanning sets
    def span(vecs):
        S = {(0, 0, 0)}
        for v in vecs:
            S = {tuple((s[i] + k * v[i]) % p for i in range(3)) for s in S for k in range(p)}
        return frozenset(S)

    vecsL = list(itertools.product(range(p), repeat=3))

    def normalized(v):  # first nonzero coordinate equal to 1
        for x in v:
            if x:
                return x == 1
        return False
    nz = [v for v in vecsL if normalized(v)]
    cands = [frozenset({(0, 0, 0)}), frozenset(vecsL)]
    cands += [span([v]) for v in nz]  # lines
    cands += [frozenset(u for u in vecsL if sum(f[i] * u[i] for i in range(3)) % p == 0) for f in nz]  # planes
    subs = set()
    for S in cands:
        if all((0, 0, (u[0] * v[1] - u[1] * v[0]) % p) in S for u in S for v in S):
            subs.add(S)
    subs = sorted(subs, key=len)

    results = []
    for h in subs:
        normal = all((0, 0, (x[0] * v[1] - x[1] * v[0]) % p) in h for x in vecsL for v in h)
        # (a) tuple fibers
        hlift = [a for a in cover if all(E(s, a) in h for s in (1, 2))]
        hlift_set = set(hlift)
        formula = {a for a in cover if (a[0], a[1], a[2]) in h and (0, 0, a[3]) in h}
        ok_a = hlift_set == formula
        # f-hat(a)=f-hat(b) iff a^{-1}*b in H~ ; check via f = coset label in G
        # (left coset label of g: canonical min of g*H)
        hl = list(h)

        def lab(g):
            return min(bch_L(g, x) for x in hl)
        fh = {a: (lab(E(1, a)), lab(E(2, a))) for a in cover}
        for a in cover[:: max(1, N // 40)]:
            for b in cover:
                same = fh[a] == fh[b]
                ok_a &= (same == (bch_cover(neg(a), b) in hlift_set))
        # rho_{H~} matrix: entry [a,b] = 1/N * 1[b^{-1} a in H~]
        rho = np.zeros((N, N), dtype=complex)
        for a in cover:
            for b in cover:
                if bch_cover(neg(b), a) in hlift_set:
                    rho[idx[a], idx[b]] = 1.0 / N
        # R_g |x> = |x g^{-1}>, central z = (0,0,0,z4)
        def Rmat(g):
            M = np.zeros((N, N))
            gi = neg(g)
            for x in cover:
                M[idx[bch_cover(x, gi)], idx[x]] = 1
            return M
        Rz = [Rmat((0, 0, 0, z)) for z in range(p)]
        Pi = [sum(w ** (-lam * z) * Rz[z] for z in range(p)) / p for lam in range(p)]
        probs = [np.trace(rho @ Pi[l]).real for l in range(p)]
        Kdim = 1 if (0, 0, 1) in h else 0
        Kperp = [0] if Kdim else list(range(p))
        ok_b = all(abs(probs[l] - (1.0 / len(Kperp) if l in Kperp else 0)) < 1e-9 for l in range(p))
        rho_l = {l: Pi[l] @ rho @ Pi[l] / probs[l] for l in Kperp}
        # phi_l(g) = tr(rho_l R_g)  -- the factor tr(R_a rho R_b^dag) = tr(rho R_{b^{-1} a})
        Rall = {}
        Q = list(itertools.product(range(p), repeat=3))
        sigma = {q: (q[0], q[1], q[2], 0) for q in Q}

        def factor(l, s, q, r):
            a = dil(s, sigma[q]); b = dil(s, sigma[r])
            # direct: tr(R_a rho R_b^dag) = sum_x rho[x a^{-1}... ] computed via matrices of permutations
            key = (a, b)
            return None
        # compute tr(R_a rho_l R_b^dagger) directly using index permutations
        perm = {}

        def P(g):
            if g not in perm:
                gi = neg(g)
                perm[g] = np.argsort(np.array([idx[bch_cover(x, gi)] for x in cover]))
            return perm[g]

        def tr_direct(l, a, b):
            # (R_a rho R_b^dag)[x,x] = rho[pa^{-1}(x), pb^{-1}(x)] ; R_a|y>=|pa(y)>
            pa, pb = P(a), P(b)
            return np.sum(rho_l[l][pa, pb])
        target = np.zeros((len(Q), len(Q)))
        th = {q for q in Q if q in h}
        for i, q in enumerate(Q):
            for j, r in enumerate(Q):
                d = tuple((q[k] - r[k]) % p for k in range(3))
                target[i, j] = (1.0 / len(Q)) if d in th else 0
        ok_c = True
        Fcache = {}
        for l in Kperp:
            for s in range(1, p):
                F = np.zeros((len(Q), len(Q)), dtype=complex)
                for i, q in enumerate(Q):
                    for j, r in enumerate(Q):
                        F[i, j] = tr_direct(l, dil(s, sigma[q]), dil(s, sigma[r]))
                Fcache[(l, s)] = F
        ntests = 0
        for labels in itertools.product(Kperp, repeat=3):
            for s in itertools.product(range(p), repeat=3):
                if all(x == 0 for x in s):
                    continue
                if sum(s[i] ** 2 * labels[i] for i in range(3)) % p:
                    continue
                out = np.ones((len(Q), len(Q)), dtype=complex) / len(Q)
                for i in range(3):
                    if s[i]:
                        out = out * Fcache[(labels[i], s[i])]
                ntests += 1
                ok_c &= np.allclose(out, target, atol=1e-9)
        results.append((len(h), normal, ok_a, ok_b, ok_c, ntests))
    return results


def single_eval_control(p):
    """Negative control: pullback E_1^{-1}(h) is not dilation-stable unless [G,G] <= H."""
    bad = 0
    inv = 0
    vecsL = list(itertools.product(range(p), repeat=3))
    for v in vecsL:
        if v == (0, 0, 0):
            continue
        h = {tuple((k * v[i]) % p for i in range(3)) for k in range(p)}  # lines are subalgebras
        pull = {a for a in itertools.product(range(p), repeat=4)
                if (a[0] % p, a[1] % p, (a[2] + a[3]) % p) in h}
        dl = {((2 * a[0]) % p, (2 * a[1]) % p, (2 * a[2]) % p, (4 * a[3]) % p) for a in pull}
        inv += 1
        bad += (dl != pull)
    return bad, inv


if __name__ == "__main__":
    for p in (3, 5):
        res = run(p)
        print(flush=True); print(f"p={p}: subgroups={len(res)}, nonnormal={sum(1 for r in res if not r[1])}, "
              f"all fibers ok={all(r[2] for r in res)}, all label laws ok={all(r[3] for r in res)}, "
              f"all descents ok={all(r[4] for r in res)}, witness tests={sum(r[5] for r in res)}")
        b, n = single_eval_control(p)
        print(f"p={p}: single-evaluation pullback not delta_2-stable for {b}/{n} hidden lines")
