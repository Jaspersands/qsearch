"""SPARSE-TRI: the triangular one-dimension-per-round SDE solver (paper prop:triangular-sde) with
KOW's sparse-dependency selection in each round.  Worst case, deterministic given the contraction.

Problem: lambda_1..lambda_M in F_p^a, find nonzero x in (P u {0})^M with sum x_i lambda_i = 0,
P = kappa-th powers.  Round at codimension l (quotient by the realized subgroup U): take the next
l + r unused columns (r = ceil(log_p(l+1))), compute an r-dimensional space of dependencies of
their images mod U, take the sparsest nonzero codeword delta (all p^r - 1 combinations), X = supp
delta.  The contraction weights x_i = zeta delta_i (alpha_{cos zeta} + beta_{cos delta_i}) realize
zeta v (mod U) for every zeta, v = sum beta_{cos delta_i} delta_i lambda_i.  Either v in U (stop:
the zeta = 1 weights are a nonzero S-weighted set with sum in U) or U <- U + F_p v.  Unwinding as
in the paper.  Every output is re-checked: nonzero, weights in P u {0}, sum = 0.

Cost bound used in the recursion: |X| <= floor((l + r)(1 - 1/p) / (1 - p^{-r})) (mean weight of a
uniform nonzero codeword of an r-dimensional code with <= l + r non-identically-zero coordinates).
"""
import sys, itertools, math
import numpy as np

rng = np.random.default_rng(1108)


def primitive_root(p):
    for g in range(2, p):
        if len({pow(g, e, p) for e in range(p - 1)}) == p - 1:
            return g
    return 1


class Field:
    def __init__(self, p, kappa):
        assert (p - 1) % kappa == 0
        self.p, self.kappa = p, kappa
        g = primitive_root(p)
        self.ind = {pow(g, e, p): e for e in range(p - 1)}
        self.cos = {a: self.ind[a] % kappa for a in range(1, p)}
        self.P = sorted({pow(x, kappa, p) for x in range(1, p)})
        self.S = set(self.P) | {0}
        self.g = g
        self.alpha, self.beta = self.find_contraction()

    def find_contraction(self):
        """alpha, beta in F_p^kappa with alpha_0 = 1, beta_0 = 0 and
        alpha_j + beta_i in g^{-(i+j)} P u {0}; brute force (small p)."""
        p, k, g = self.p, self.kappa, self.g
        def ok(aj, bi, i, j):
            s = (aj + bi) % p
            return s == 0 or self.cos[s] == (-(i + j)) % k
        for alpha in itertools.product(range(p), repeat=k - 1):
            alpha = (1,) + alpha
            for beta in itertools.product(range(p), repeat=k - 1):
                beta = (0,) + beta
                if all(ok(alpha[j], beta[i], i, j) for i in range(k) for j in range(k)):
                    return alpha, beta
        raise ValueError('no contraction (p in E_2(kappa))')

    def weights(self, delta, zeta):
        """x_i = zeta delta_i (alpha_{cos zeta} + beta_{cos delta_i}); all in S."""
        p = self.p
        n = self.cos[zeta % p]
        x = np.zeros_like(delta)
        for i, d in enumerate(delta):
            if d:
                x[i] = (zeta * d * (self.alpha[n] + self.beta[self.cos[int(d)]])) % p
                assert int(x[i]) in self.S
        return x


def rref_basis(V, p):
    """Row-reduce V (rows = vectors); return independent rows (basis) and pivot columns."""
    M = V.copy() % p
    rows, cols = M.shape
    r = 0
    piv = []
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i, c]), None)
        if pr is None:
            continue
        M[[r, pr]] = M[[pr, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        piv.append(c)
        r += 1
        if r == rows:
            break
    return M[:r], piv


class Quotient:
    """Realized subgroup U <= F_p^a with reduction of vectors modulo U."""
    def __init__(self, a, p):
        self.a, self.p = a, p
        self.B = np.zeros((0, a), dtype=np.int64)
        self.piv = []

    def reduce(self, v):
        v = v.copy() % self.p
        for row, c in zip(self.B, self.piv):
            if v[c]:
                v = (v - v[c] * row) % self.p
        return v

    def contains(self, v):
        return not self.reduce(v).any()

    def add(self, v):
        self.B, self.piv = rref_basis(np.vstack([self.B, v.reshape(1, -1)]), self.p)

    def dim(self):
        return self.B.shape[0]


def nullspace(A, p):
    from verify_gadget import nullspace_mod
    return nullspace_mod(A, p)


def sparsest(Dbasis, p):
    """sparsest nonzero codeword among all p^r - 1 combinations of the basis rows."""
    r, N = Dbasis.shape
    best = None
    for coef in itertools.product(range(p), repeat=r):
        if not any(coef):
            continue
        c = (np.array(coef) @ Dbasis) % p
        w = int(np.count_nonzero(c))
        if best is None or w < best[0]:
            best = (w, c)
    return best[1]


def solve(F, lam, r_rule=None, log=None):
    """lam: a x M matrix of columns.  Returns weights x (length M) or None if columns ran out.
    pool = unused column indices in order; a round takes the first l + r, consumes X = supp delta
    and returns the rest to the front of the pool."""
    p, a = F.p, lam.shape[0]
    M = lam.shape[1]
    U = Quotient(a, p)
    rounds = []
    pool = list(range(M))
    while U.dim() < a:
        l = a - U.dim()
        r = 1
        while p ** r < l + 1:
            r += 1
        if len(pool) < l + r:
            return None
        F_idx, pool = pool[:l + r], pool[l + r:]
        img = np.array([U.reduce(lam[:, i]) for i in F_idx], dtype=np.int64).T
        D = nullspace(img, p)
        assert D.shape[0] >= r
        delta_full = sparsest(D[:r], p)
        X = [F_idx[i] for i in range(len(F_idx)) if delta_full[i]]
        delta = delta_full[delta_full != 0]
        pool = [F_idx[i] for i in range(len(F_idx)) if not delta_full[i]] + pool
        v = np.zeros(a, dtype=np.int64)
        e = np.zeros(a, dtype=np.int64)
        for i, d in zip(X, delta):
            v = (v + F.beta[F.cos[int(d)]] * d * lam[:, i]) % p
            e = (e + d * lam[:, i]) % p
        assert U.contains(e)
        if log is not None:
            log.append((l, len(F_idx), len(X)))
        if U.contains(v):
            x = np.zeros(M, dtype=np.int64)
            for i, wi in zip(X, F.weights(delta, 1)):
                x[i] = wi
            rho = (lam @ x) % p
            assert U.contains(rho) and x.any()
            return unwind(F, lam, U, rounds, x, rho)
        rounds.append((X, delta, v.copy()))
        U.add(v)
    if not pool:
        return None
    x = np.zeros(M, dtype=np.int64)
    x[pool[0]] = 1
    if log is not None:
        log.append((0, 1, 1))
    return unwind(F, lam, U, rounds, x, lam[:, pool[0]].copy())


def unwind(F, lam, U, rounds, x, rho):
    """Given weights x with value rho in U = span(v_1..v_k), add round weights so that the total is 0."""
    p = F.p
    tau = (-rho) % p
    # coordinates of tau in the (ordered, independent) v_1..v_k: solve by processing from the last round
    k = len(rounds)
    for l in range(k - 1, -1, -1):
        X, delta, v = rounds[l]
        # tau in U_l = span(v_1..v_{l+1}); find zeta with tau - zeta v_{l+1} in U_{l-1} = span(v_1..v_l)
        Ul = Quotient(lam.shape[0], p)
        for j in range(l):
            Ul.add(rounds[j][2])
        zeta = None
        for z in range(p):
            if Ul.contains((tau - z * v) % p):
                zeta = z
                break
        assert zeta is not None
        if zeta:
            w = F.weights(delta, zeta)
            for i, wi in zip(X, w):
                assert x[i] == 0
                x[i] = wi
            val = np.zeros(lam.shape[0], dtype=np.int64)
            for i, wi in zip(X, w):
                val = (val + wi * lam[:, i]) % p
            tau = (tau - val) % p
    assert not tau.any()
    return x


def check(F, lam, x):
    assert x.any()
    assert all(int(v) in F.S for v in x)
    assert not ((lam @ x) % F.p).any()


def recursion(p, a):
    """m_l = max(l + r, m_{l-1} + floor((l+r)(1-1/p)/(1-p^-r))) with r = ceil(log_p(l+1))."""
    from fractions import Fraction
    m = 1   # one closing column at dimension 0
    for l in range(1, a + 1):
        r = 1
        while p ** r < l + 1:
            r += 1
        w = math.floor((l + r) * Fraction(p - 1, p) / (1 - Fraction(1, p ** r)))
        m = max(l + r, m + w)
    return m


def main():
    cases = [(5, 2), (7, 2), (11, 2), (13, 2), (7, 3), (13, 3)]
    for p, kappa in cases:
        F = Field(p, kappa)
        print(f'p={p} kappa={kappa}: P={F.P} contraction alpha={F.alpha} beta={F.beta}')
        for a in (6, 10, 20, 40):
            tri = (a + 1) * (a + 2) // 2
            rec = recursion(p, a)
            fails = 0
            maxused = 0
            trials = 20 if a <= 20 else 6
            for t in range(trials):
                M = rec
                kind = t % 4
                if kind == 0:
                    lam = rng.integers(0, p, size=(a, M))
                elif kind == 1:   # low rank
                    B = rng.integers(0, p, size=(a, max(1, a // 2)))
                    lam = (B @ rng.integers(0, p, size=(B.shape[1], M))) % p
                elif kind == 2:   # few distinct columns
                    pool = rng.integers(0, p, size=(a, 2 * a))
                    lam = pool[:, rng.integers(0, 2 * a, size=M)]
                else:             # sparse columns
                    lam = (rng.integers(0, p, size=(a, M)) * (rng.random((a, M)) < 0.15)) % p
                lam = lam.astype(np.int64)
                log = []
                res = solve(F, lam.copy(), log=log)
                if res is None:
                    fails += 1
                    continue
                check(F, lam, res)
                maxused = max(maxused, sum(c for (_, _, c) in log))
            print(f'  a={a}: triangular {tri}, recursion budget {rec} ({rec/a**2:.3f} a^2, (1-1/p)/2 = {(1-1/p)/2:.3f}); '
                  f'{trials} instances at budget: {fails} failures, max columns consumed {maxused}')


if __name__ == '__main__':
    main()
