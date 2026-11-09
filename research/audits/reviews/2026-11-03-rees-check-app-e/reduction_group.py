"""Group-level exact check of Appendix E from oracle access alone.

Groups (L, *) with the truncated BCH product (class <= 4 < p, p in {5, 7}).
For each hidden subgroup H = exp(h) an ordinary left-coset oracle f is built by
enumerating cosets. The reduction then uses only f:
  * Lemma lem:app-codim-restrict: F = f o iota on the ideal hides W exactly
    (every fibre of F is a coset of W, W read from F).
  * Lemma lem:app-codim-sample: the exact Fourier law (float, small b) is
    uniform on W^perp; the basis test accepts exactly W.
  * Lemma lem:app-codim-transport: f o tau hides pi(H) on (s/k, *) for random
    sections tau that are neither linear nor homomorphic (every fibre is a left
    coset q0 * pi(H), computed with the BCH product of s/k).
  * Prop prop:app-codim-complete: the terminal / abelian end, read from the
    transported oracle, unwinds (linear sections) to h.
  * Prop prop:app-codim-birthday, uniformity step: for every coset gH the
    multiset {x^{-1} * y : x, y in gH} covers H uniformly (nonnormal H included).
  * Heisenberg remark: no subgroup of order p^2 of Heis(F_p) meets the centre
    trivially (so no homomorphic section of Heis -> F_p^2).
Run: /opt/anaconda3/bin/python reduction_group.py
"""
import itertools
import sys
import numpy as np
import lie_fp as L

rng = np.random.default_rng(1103)


# ---------------------------------------------------------------- BCH (class <= 4)
def bbr(C, X, Y, p):
    return np.einsum('ki,kj,ijl->kl', X, Y, C) % p


def bch(C, X, Y, p):
    """Truncated BCH, exact for class <= 4, rows of X, Y are elements."""
    X = np.atleast_2d(X) % p
    Y = np.atleast_2d(Y) % p
    if X.shape[0] == 1 and Y.shape[0] > 1:
        X = np.repeat(X, Y.shape[0], 0)
    if Y.shape[0] == 1 and X.shape[0] > 1:
        Y = np.repeat(Y, X.shape[0], 0)
    i2, i12, i24 = pow(2, p - 2, p), pow(12, p - 2, p), pow(24, p - 2, p)
    XY = bbr(C, X, Y, p)
    XXY = bbr(C, X, XY, p)
    YXY = bbr(C, Y, XY, p)
    YXXY = bbr(C, Y, XXY, p)
    return (X + Y + i2 * XY + i12 * XXY - i12 * YXY - i24 * YXXY) % p


def check_group(C, p, trials=200):
    n = C.shape[0]
    X, Y, Z = (rng.integers(0, p, (trials, n)) for _ in range(3))
    a = bch(C, bch(C, X, Y, p), Z, p)
    b = bch(C, X, bch(C, Y, Z, p), p)
    assert np.array_equal(a, b), "BCH not associative"
    assert not np.any(bch(C, X, (-X) % p, p)), "inverse"


def enc(V, p):
    V = np.atleast_2d(V)
    w = p ** np.arange(V.shape[1])[::-1]
    return (V % p) @ w


def all_vectors(B, p):
    """All elements of the span of rows of B."""
    k = B.shape[0]
    if k == 0:
        return np.zeros((1, B.shape[1]), dtype=np.int64)
    coeffs = np.array(list(itertools.product(range(p), repeat=k)), dtype=np.int64)
    return (coeffs @ B) % p


def make_oracle(C, h, p):
    """Left-coset labels: f(x) = f(y) iff x^{-1} * y in exp(h)."""
    n = C.shape[0]
    G = all_vectors(np.eye(n, dtype=np.int64), p)
    Hel = all_vectors(h, p)
    lab = -np.ones(p ** n, dtype=np.int64)
    nxt = 0
    for x in G:
        ex = enc(x, p)[0]
        if lab[ex] >= 0:
            continue
        coset = bch(C, x.reshape(1, -1), Hel, p)
        lab[enc(coset, p)] = nxt
        nxt += 1
    assert np.all(lab >= 0)
    # sanity: labels are exactly the left cosets (count)
    assert nxt * len(Hel) == p ** n
    return lambda V: lab[enc(V, p)]


def fibres_are_left_cosets(Cq, fq, hq, p):
    """Every fibre of fq on F_p^q equals q0 * exp(hq) (BCH of the quotient)."""
    q = Cq.shape[0]
    Q = all_vectors(np.eye(q, dtype=np.int64), p)
    labs = fq(Q)
    Hel = all_vectors(hq, p)
    seen = set()
    for idx in range(len(Q)):
        l = labs[idx]
        if l in seen:
            continue
        seen.add(l)
        fib = set(enc(Q[labs == l], p).tolist())
        cos = set(enc(bch(Cq, Q[idx].reshape(1, -1), Hel, p), p).tolist())
        if fib != cos:
            return False
    return True


def fourier_law(F, b, p):
    """Exact-in-float law of one Fourier sample for the abelian oracle F on F_p^b."""
    Z = all_vectors(np.eye(b, dtype=np.int64), p)
    labs = F(Z)
    omega = np.exp(2j * np.pi / p)
    chis = Z
    phase = omega ** ((chis @ Z.T) % p)            # [chi, z]
    probs = np.zeros(len(chis))
    for l in np.unique(labs):
        mask = labs == l
        amp = phase[:, mask].sum(1) / np.sqrt(mask.sum()) / np.sqrt(p ** b)
        probs += (mask.sum() / len(Z)) * np.abs(amp) ** 2
    return chis, probs


def run_instance(C0, h0, k, p, stats, fourier=False):
    m = C0.shape[0]
    f0 = make_oracle(C0, h0, p)
    C, kj = C0, k
    Lam = np.eye(m, dtype=np.int64)              # rows: images of L_j basis in L_0
    f = lambda V, Lam=Lam: f0((np.atleast_2d(V) @ Lam) % p)
    h_lie = h0                                    # Lie-side truth, only for assertions
    levels = []
    while True:
        n = C.shape[0]
        if kj <= 0:
            hJ = np.eye(n, dtype=np.int64)
            break
        if n == 0 or L.is_abelian_space(C, np.eye(n, dtype=np.int64), p):
            Z = all_vectors(np.eye(n, dtype=np.int64), p) if n else np.zeros((1, 0), dtype=np.int64)
            hJ = L.span(Z[f(Z) == f(np.zeros((1, n), dtype=np.int64))[0]], n, p) if n else Z[:0]
            break
        X = L.construct_ideal(C, p, rng)
        b = X.shape[0]
        if b <= kj:
            # terminal: read h_J from the transported oracle (stands in for the solver)
            Z = all_vectors(np.eye(n, dtype=np.int64), p)
            hJ = L.span(Z[f(Z) == f(np.zeros((1, n), dtype=np.int64))[0]], n, p)
            stats['terminal'] += 1
            break
        # restricted oracle on the ideal
        F = lambda Zc, X=X, f=f: f((np.atleast_2d(Zc) @ X) % p)
        Zb = all_vectors(np.eye(b, dtype=np.int64), p)
        lb = F(Zb)
        W = L.span(Zb[lb == lb[0]], b, p)            # z with F(z) = F(0) (Zb[0] = 0)
        assert len(Zb[lb == lb[0]]) == p ** L.dim(W), "kernel not a subspace"
        # every fibre of F is a coset of W
        for l in np.unique(lb):
            fib = Zb[lb == l]
            assert len(fib) == p ** L.dim(W)
            d = (fib - fib[0]) % p
            assert all(L.in_span(v, W, p) for v in d[:: max(1, len(d) // 25)])
        Ilie = L.span(X, n, p)
        Wtrue = L.span([L.solve_coords(X, v, p) for v in L.intersect(h_lie, Ilie, n, p)], b, p) \
            if L.dim(L.intersect(h_lie, Ilie, n, p)) else np.zeros((0, b), dtype=np.int64)
        assert L.equal(W, Wtrue, p), "oracle-read W differs from iota^-1(h cap I)"
        assert L.dim(W) >= b - kj >= 1
        if fourier and b <= 4:
            chis, probs = fourier_law(F, b, p)
            Wp = L.annihilator(W, b, p)
            r = L.dim(Wp)
            for chi, pr in zip(chis, probs):
                inperp = L.in_span(chi, Wp, p) if r else not np.any(chi)
                assert abs(pr - (p ** (-r) if inperp else 0.0)) < 1e-9
            stats['fourier'] += 1
        K = (W @ X) % p
        S = L.normalizer(C, K, p)
        Cq, sec, proj = L.quotient(C, S, K, p, rng)
        hq = L.span([proj(v) for v in h_lie], Cq.shape[0], p)
        check_group(Cq, p, 50)
        # transport through a random section that is neither linear nor a homomorphism
        q = Cq.shape[0]
        Qall = all_vectors(np.eye(q, dtype=np.int64), p)
        Kall = all_vectors(K, p)
        junk = Kall[rng.integers(0, len(Kall), len(Qall))]
        table = {int(e): j for j, e in enumerate(enc(Qall, p))}

        def tau(V, sec=sec, junk=junk, table=table):
            V = np.atleast_2d(V) % p
            idx = np.array([table[int(e)] for e in enc(V, p)])
            return (V @ sec + junk[idx]) % p
        ftau = lambda V, tau=tau, f=f: f(tau(V))
        assert fibres_are_left_cosets(Cq, ftau, hq, p), "nonlinear transport failed"
        stats['sections'] += 1
        stats['parent_queries'] += len(Qall)
        # the algorithm itself continues with the linear section
        levels.append((sec, K, n))
        Lam = (sec @ Lam) % p
        f = lambda V, Lam=Lam: f0((np.atleast_2d(V) @ Lam) % p)
        assert fibres_are_left_cosets(Cq, f, hq, p), "linear transport failed"
        kj = kj - (n - L.dim(S))
        C, h_lie = Cq, hq
    cur = hJ
    for sec, K, n in reversed(levels):
        img = (cur @ sec) % p if L.dim(cur) else np.zeros((0, n), dtype=np.int64)
        cur = L.span(np.vstack([img, K]), n, p)
    assert L.equal(cur, h0, p), "unwinding failed"
    stats['ok'] += 1


def birthday_uniformity(C, h, p):
    """For every left coset gH, x^{-1} * y over x, y in gH hits each h' in H |H| times."""
    n = C.shape[0]
    Hel = all_vectors(h, p)
    G = all_vectors(np.eye(n, dtype=np.int64), p)
    seen = set()
    for g in G[rng.permutation(len(G))[:30]]:
        cos = bch(C, g.reshape(1, -1), Hel, p)
        key = min(enc(cos, p).tolist())
        if key in seen:
            continue
        seen.add(key)
        Xs = np.repeat(cos, len(cos), 0)
        Ys = np.tile(cos, (len(cos), 1))
        D = bch(C, (-Xs) % p, Ys, p)
        cnt = np.bincount(enc(D, p), minlength=p ** n)
        hk = enc(Hel, p)
        assert np.all(cnt[hk] == len(Hel)) and cnt.sum() == len(Hel) ** 2
    return True


def heis(pn, p):
    n = 2 * pn + 1
    return L.from_brackets(n, {(i, pn + i): {n - 1: 1} for i in range(pn)}, p)


def main():
    stats = dict(ok=0, terminal=0, sections=0, parent_queries=0, fourier=0)
    algs = []
    for p in (5, 7):
        algs += [(f'heis3 p={p}', heis(1, p), p), (f'fil4 p={p}', L.filiform(4, p), p)]
    algs += [('fil5 p=5', L.filiform(5, 5), 5),
             ('hand5 p=5', L.from_brackets(5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1},
                                               (1, 2): {4: 1}}, 5), 5),
             ('heis5 p=5', heis(2, 5), 5),
             ('n4 p=5', L.strictly_upper(4, 5)[0], 5)]
    for _ in range(6):
        C = L.random_nilpotent(5, 5, rng, push=0.7)
        if L.nil_class(C, 5) <= 4:
            algs.append(('rand5 p=5', C, 5))
    for _ in range(4):
        C = L.random_nilpotent(4, 7, rng, push=0.7)
        algs.append(('rand4 p=7', C, 7))
    nbirthday = 0
    for name, C, p in algs:
        assert L.nil_class(C, p) <= 4 < p
        check_group(C, p)
        n = C.shape[0]
        hs = []
        while len(hs) < (4 if n >= 6 else 8):
            gens = [rng.integers(0, p, n) * (rng.random(n) < 0.6) for _ in range(rng.integers(1, 3))]
            h = L.subalgebra_generated(C, gens, p)
            if 0 < n - L.dim(h) <= 4:
                hs.append(h)
        for h in hs:
            normal = L.is_ideal(C, h, p)
            for slack in (0, 1):
                run_instance(C, h, n - L.dim(h) + slack, p, stats, fourier=(slack == 0))
            if not normal and p ** n * len(all_vectors(h, p)) <= 2_000_000:
                birthday_uniformity(C, h, p)
                nbirthday += 1
        print(f"  {name}: dim {n}, class {L.nil_class(C, p)}, {len(hs)} hidden subgroups done")
    # Heisenberg remark
    for p in (3, 5, 7):
        C = heis(1, p)
        n = 3
        bad = 0
        for M in itertools.product(range(p), repeat=6):
            B = np.array(M, dtype=np.int64).reshape(2, 3)
            S = L.span(B, n, p)
            if L.dim(S) == 2 and L.is_subalgebra(C, S, p) and not L.in_span([0, 0, 1], S, p):
                bad += 1
        print(f"Heis(F_{p}): two-dimensional subalgebras missing the centre: {bad}")
        assert bad == 0
    print(f"instances recovered: {stats['ok']} (all), nonabelian terminals: {stats['terminal']}, "
          f"nonlinear sections checked: {stats['sections']} ({stats['parent_queries']} parent "
          f"queries), exact Fourier laws checked: {stats['fourier']}, "
          f"birthday uniformity (nonnormal H): {nbirthday}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
