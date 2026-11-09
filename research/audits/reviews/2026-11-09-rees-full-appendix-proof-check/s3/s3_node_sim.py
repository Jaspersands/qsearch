#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): implement the node (N1)-(N5) of appendix-schedule3.tex as
written (fair-bit draws with attempt cap B+ceil(log2 F), Rabin splitting with round cap R,
Bezout exponent alpha, exact check), run it on i.i.d. uniform banks, and test:
  * every non-aborting run returns s != 0 with sum_i s_i^d lambda_i = 0 (N5 always passes);
  * Lemma s3-root: the returned t satisfies t^kappa = y; empirical split rate >= 1/3;
  * abort frequencies against the bounds of Lemma s3-node(c).
A finite randomized check: it can falsify the procedure, it proves nothing."""
import sys, math, random
import numpy as np
from flint import nmod_poly

rng = random.Random(20261109)
nrng = np.random.default_rng(20261109)

def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

class Timeout(Exception): pass

class Draws:
    """fair-bit sampler: ell = ceil(log2 p) bits, accept if < p, cap attempts per draw"""
    def __init__(self, p, cap):
        self.p, self.cap, self.ell = p, cap, (p-1).bit_length()
        self.count = 0; self.attempts = 0
    def draw(self):
        self.count += 1
        for _ in range(self.cap):
            self.attempts += 1
            v = rng.getrandbits(self.ell)
            if v < self.p: return v
        raise Timeout("draw")

def root_extract(y, kap, p, R, draws, stats):
    """Lemma s3-root: returns t with t^kap = y; g = x^kap - y; split by gcd with (x+delta)^((p-1)/2)-1"""
    g = nmod_poly([(-y) % p] + [0]*(kap-1) + [1], p)
    while g.degree() >= 2:
        for rnd in range(R):
            delta = draws.draw()
            stats['rounds'] += 1
            xd = nmod_poly([delta, 1], p)
            pw = pow(xd, (p-1)//2, g)            # reduce modulo g by repeated squaring
            g1 = g.gcd(pw - 1)
            if 0 < g1.degree() < g.degree():
                stats['splits'] += 1
                g2 = g // g1
                g = g1 if g1.degree() <= g2.degree() else g2
                break
        else:
            raise Timeout("root")
    # deg g == 1, monic: x + c0  -> root -c0
    co = g.coeffs()
    lead_inv = pow(int(co[1]), p-2, p)
    return (-int(co[0]) * lead_inv) % p

def kernel_basis(Lam, p):
    """RREF of g x M matrix (list of rows), return rank and kernel basis vectors"""
    A = [list(r) for r in Lam]
    M = len(A[0]); rows = len(A); r = 0; piv = []
    for c in range(M):
        pr = None
        for i in range(r, rows):
            if A[i][c] % p: pr = i; break
        if pr is None: continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p-2, p); A[r] = [x*inv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(x - f*z) % p for x, z in zip(A[i], A[r])]
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(M) if c not in piv]
    basis = []
    for fc in free:
        v = [0]*M; v[fc] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-A[i][fc]) % p
        basis.append(v)
    return r, basis

def node(Lam, p, d, u, B, stats):
    """(N2)-(N5). Lam: list of g_d rows (labels are its columns). Returns ('ok', s) or ('abort', why)"""
    M = len(Lam[0])
    kap = math.gcd(d, p-1); h = (p-1)//kap
    g_, al, alp = egcd(d, p-1)
    # alpha d + alpha'(p-1) = kappa
    assert g_ == kap and al*d + alp*(p-1) == kap
    K = 4 * kap**M * B
    L = max(1, math.ceil(math.log2(kap))) if kap > 1 else 1
    R = 2*(B + math.ceil(math.log2(M*L)))
    F = K*M + M*L*R
    cap = B + math.ceil(math.log2(F))
    draws = Draws(p, cap)
    r, basis = kernel_basis(Lam, p)
    if r > u-1: return ('abort', 'rank')
    Kb = np.array(basis, dtype=np.int64).T if basis else np.zeros((M, 0), dtype=np.int64)  # M x (M-r)
    powh_table = np.array([pow(x, h, p) for x in range(p)], dtype=np.int64)
    y = None
    try:
        # (N3): draws in batches (exactly as sequential fair-bit draws, vectorized)
        j = 0
        batch = 4096
        while j < K:
            nb = min(batch, K - j)
            ell = (p-1).bit_length()
            # each theta entry: fair-bit rejection with cap
            th = np.empty((nb, M - r), dtype=np.int64)
            for col in range(M - r):
                vals = nrng.integers(0, 2**ell, size=(nb, cap))
                ok = vals < p
                if not ok.any(axis=1).all():
                    raise Timeout("draw")
                first = ok.argmax(axis=1)
                th[:, col] = vals[np.arange(nb), first]
            draws.count += nb*(M-r)
            W = (th @ Kb.T) % p                       # nb x M
            nz = W != 0
            okrow = nz.any(axis=1) & np.all(~nz | (powh_table[W] == 1), axis=1)
            if okrow.any():
                idx = int(np.argmax(okrow))
                stats['trials'] += j + idx + 1
                y = [int(v) for v in W[idx]]
                break
            j += nb
        if y is None:
            stats['trials'] += K
            return ('abort', 'trials')
        # (N4)
        s = []
        for yi in y:
            if yi == 0: s.append(0); continue
            if kap == 1: t = yi
            else: t = root_extract(yi, kap, p, R, draws, stats)
            assert pow(t, kap, p) == yi, "root wrong"
            s.append(pow(t, al % (p-1), p) if t else 0)   # t^alpha (alpha may be negative; t != 0)
    except Timeout as e:
        return ('abort', str(e))
    # (N5)
    g = len(Lam)
    ok = any(s) and all(sum(pow(si, d, p) * Lam[row][i] for i, si in enumerate(s)) % p == 0 for row in range(g))
    if not ok:
        stats['n5fail'] += 1
        return ('abort', 'N5')
    return ('ok', s)

def run(p, d, u, gd, ad, nnodes, B):
    M = 4*u
    stats = dict(trials=0, rounds=0, splits=0, n5fail=0)
    outcomes = {}
    for _ in range(nnodes):
        # E: g_d x a_d basis of a random a_d-dim subspace K_d^perp (fixed per experiment would also do)
        while True:
            E = [[rng.randrange(p) for _ in range(ad)] for _ in range(gd)]
            if ad == 0: break
            rk, _ = kernel_basis([list(col) for col in zip(*E)], p) if gd else (0, None)
            if rk == ad: break
        X = [[rng.randrange(p) for _ in range(M)] for _ in range(ad)]
        Lam = [[sum(E[i][k]*X[k][j] for k in range(ad)) % p for j in range(M)] for i in range(gd)]
        res, val = node(Lam, p, d, u, B, stats)
        outcomes[val if res == 'abort' else 'ok'] = outcomes.get(val if res == 'abort' else 'ok', 0) + 1
    kap = math.gcd(d, p-1)
    sr = stats['splits']/stats['rounds'] if stats['rounds'] else float('nan')
    print(f"p={p} d={d} kappa={kap} u={u} M={M} g_d={gd} a_d={ad} B={B}: outcomes={outcomes} "
          f"mean trials={stats['trials']/nnodes:.1f} split-rate={sr:.3f} N5fail={stats['n5fail']}")
    return outcomes, stats

if __name__ == "__main__":
    # root extraction exhaustive for small p: every y in P_kappa\{0}, every kappa | p-1, kappa >= 2
    nroots = 0; rounds = 0; splits = 0
    for p in [7, 11, 13, 31, 37, 41, 61, 67, 73, 97, 151, 181, 241]:
        for kap in range(2, p):
            if (p-1) % kap: continue
            h = (p-1)//kap
            ys = sorted({pow(x, kap, p) for x in range(1, p)})
            for y in ys:
                st = dict(rounds=0, splits=0)
                t = root_extract(y, kap, p, 60, Draws(p, 60), st)
                assert pow(t, kap, p) == y
                nroots += 1; rounds += st['rounds']; splits += st['splits']
    print(f"root extraction: {nroots} roots correct; split rate {splits/rounds:.3f} (lemma: >= 1/3)")
    # nodes on i.i.d. banks (c = 2 tree parameters: B = ceil(log2(64*4u)))
    for (p, d, u, gd, ad, nn) in [(67, 2, 2, 3, 1, 60), (67, 2, 2, 2, 0, 20), (67, 2, 2, 1, 1, 40),
                                  (151, 2, 3, 4, 2, 25), (151, 3, 3, 2, 2, 2), (157, 3, 3, 2, 1, 2),
                                  (151, 3, 3, 1, 0, 3)]:
        B = math.ceil(math.log2(64 * (4*u)))
        run(p, d, u, gd, ad, nn, B)
