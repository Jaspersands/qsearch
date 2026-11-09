"""Referee B: SIMPLE5, an independent solver for F_5^n {0,+-1}-zero-sums that uses ONLY Fact F5
(every spanning label set in F_5^2 \\ 0 is 2-feasible with weak nondegeneracy) and Lemmas 1, 2(A).

Stage at codimension q >= 2: take the first q + 2 unused columns, ANY two independent dependencies
delta, delta' of their images mod U (rank <= q, so dim D >= 2), labels l_i = (delta_i, delta'_i);
columns with l_i = 0 go back to the pool; a gadget (Phi, gamma) for the label set gives realizers
y_alpha(i) = <alpha, Phi(l_i)> + <gamma_alpha, l_i> in S of alpha.h, h_j = sum Phi_j(l_i) v_i.
Gain <h1, h2> (cost <= q + 2) or a witness.  q = 1: two columns (always realize the line or give a
witness).  Then one closing column.  No peeling, no Lemma D, no Lemma J.
Worst-case column count: guarantee_simple(n) = n^2/4 + 3n/2 + O(1) (exact recursion below).
The gadget is found by the referee's own CNF (f5_feas.decide encoding) and re-checked.
"""
import itertools, numpy as np, pycosat
p = 5
S = {0, 1, 4}
F2 = list(itertools.product(range(p), repeat=2))
alphas = [a for a in F2 if any(a)]

def dirkey(a):
    lead = a[0] if a[0] else a[1]
    inv = pow(lead, -1, p)
    return ((a[0] * inv) % p, (a[1] * inv) % p)

def nullspace(A):
    """A: r x c over F_p; returns basis (rows) of {x : A x = 0}."""
    A = np.array(A, dtype=np.int64) % p
    r, c = A.shape
    A = A.copy(); piv = []; row = 0
    for col in range(c):
        pr = next((i for i in range(row, r) if A[i, col]), None)
        if pr is None:
            continue
        A[[row, pr]] = A[[pr, row]]
        A[row] = (A[row] * pow(int(A[row, col]), -1, p)) % p
        for i in range(r):
            if i != row and A[i, col]:
                A[i] = (A[i] - A[i, col] * A[row]) % p
        piv.append(col); row += 1
        if row == r:
            break
    free = [j for j in range(c) if j not in piv]
    B = []
    for f in free:
        x = np.zeros(c, dtype=np.int64); x[f] = 1
        for i, pc in enumerate(piv):
            x[pc] = (-A[i, f]) % p
        B.append(x)
    return np.array(B, dtype=np.int64).reshape(len(B), c)

class Quot:
    """subspace U of F_p^n in reduced echelon form; reduce(v) = canonical rep of v mod U."""
    def __init__(self, n):
        self.n = n; self.rows = []   # (pivot, row)
    def reduce(self, v):
        v = np.array(v, dtype=np.int64) % p
        for pc, r in self.rows:
            if v[pc]:
                v = (v - v[pc] * r) % p
        return v
    def add(self, v):
        v = self.reduce(v)
        if not v.any():
            return False
        pc = int(np.nonzero(v)[0][0])
        v = (v * pow(int(v[pc]), -1, p)) % p
        self.rows = [(q, (r - r[pc] * v) % p) for q, r in self.rows] + [(pc, v)]
        return True
    def contains(self, v):
        return not self.reduce(v).any()
    def dim(self):
        return len(self.rows)
    def copy(self):
        Q = Quot(self.n); Q.rows = [(a, b.copy()) for a, b in self.rows]; return Q

def check_gadget(L, Phi, gam):
    for k in set(dirkey(a) for a in alphas):
        nz = False
        for a in alphas:
            if dirkey(a) != k:
                continue
            for l in L:
                y = (a[0] * Phi[l][0] + a[1] * Phi[l][1] + gam[a][0] * l[0] + gam[a][1] * l[1]) % p
                if y not in S:
                    return False
                nz |= y != 0
        if not nz:
            return False
    return True

CACHE = {}
def gadget(L):
    key = frozenset(L)
    if key in CACHE:
        return CACHE[key]
    L = sorted(key)
    nv = [0]; cl = []
    def var():
        nv[0] += 1; return nv[0]
    def onehot(m):
        vs = [var() for _ in range(m)]
        cl.append(vs[:]); cl.extend([-vs[i], -vs[j]] for i in range(m) for j in range(i + 1, m))
        return vs
    PH = {l: onehot(25) for l in L}; GA = {a: onehot(25) for a in alphas}
    dz = {}
    for a in alphas:
        for l in L:
            z = var(); dz.setdefault(dirkey(a), []).append(z)
            for fi, f in enumerate(F2):
                af = a[0] * f[0] + a[1] * f[1]
                for gi, g in enumerate(F2):
                    y = (af + g[0] * l[0] + g[1] * l[1]) % p
                    if y not in S:
                        cl.append([-PH[l][fi], -GA[a][gi]])
                    elif y == 0:
                        cl.append([-z, -PH[l][fi], -GA[a][gi]])
    cl.extend(dz.values())
    sol = pycosat.solve(cl)
    if sol == 'UNSAT':
        CACHE[key] = None; return None
    pos = set(v for v in sol if v > 0)
    Phi = {l: F2[[i for i, v in enumerate(PH[l]) if v in pos][0]] for l in L}
    gam = {a: F2[[i for i, v in enumerate(GA[a]) if v in pos][0]] for a in alphas}
    assert check_gadget(L, Phi, gam)
    CACHE[key] = (Phi, gam)
    return CACHE[key]

class Infeasible(Exception):
    pass

def two_dim_piece(lam, U, idxs):
    """idxs: column indices whose images mod U have >= 2 independent dependencies.
    Returns ('witness', x) or ('piece', X, realizer(alpha)->dict, h) and the unused indices."""
    M = lam.shape[1]
    V = np.array([U.reduce(lam[:, i]) for i in idxs], dtype=np.int64).T
    D = nullspace(V)
    assert D.shape[0] >= 2
    d1, d2 = D[0], D[1]
    lab = [(int(a), int(b)) for a, b in zip(d1, d2)]
    X = [i for i, l in zip(idxs, lab) if any(l)]
    labX = [l for l in lab if any(l)]
    unused = [i for i, l in zip(idxs, lab) if not any(l)]
    g = gadget(set(labX))
    if g is None:
        raise Infeasible(sorted(set(labX)))
    Phi, gam = g
    h = [sum(Phi[l][j] * lam[:, i] for i, l in zip(X, labX)) % p for j in range(2)]
    def real(a):
        return {i: (a[0] * Phi[l][0] + a[1] * Phi[l][1] + gam[a][0] * l[0] + gam[a][1] * l[1]) % p for i, l in zip(X, labX)}
    for a in alphas:
        y = real(a)
        s = sum(y[i] * lam[:, i] for i in X) % p
        assert all(v in S for v in y.values())
        assert U.contains((s - a[0] * h[0] - a[1] * h[1]) % p), 'realizer does not realize alpha.h mod U'
    for a in alphas:
        if U.contains((a[0] * h[0] + a[1] * h[1]) % p):
            # dependent: some multiple of a has a realizer nonzero on X (weak nondegeneracy)
            for lmb in range(1, p):
                b = ((lmb * a[0]) % p, (lmb * a[1]) % p)
                y = real(b)
                if any(y.values()):
                    x = np.zeros(M, dtype=np.int64)
                    for i, v in y.items():
                        x[i] = v
                    return ('witness', x), unused
            raise AssertionError('weak nondegeneracy violated')
    return ('piece', X, real, h), unused

def solve(lam, log=None):
    n, M = lam.shape
    U = Quot(n); pieces = []; pool = list(range(M)); used = 0
    def fin(x):
        return unwind(lam, pieces, x)
    while n - U.dim() >= 2:
        q = n - U.dim()
        if len(pool) < q + 2:
            return None
        F, pool = pool[:q + 2], pool[q + 2:]
        for i in F:
            if U.contains(lam[:, i]):
                x = np.zeros(M, dtype=np.int64); x[i] = 1
                return fin(x)
        res, unused = two_dim_piece(lam, U, F)
        pool = unused + pool
        if res[0] == 'witness':
            return fin(res[1])
        _, X, real, h = res
        used += len(X)
        if log is not None:
            log.append((q, len(X)))
        pieces.append((U.copy(), X, real, h))
        U.add(h[0]); U.add(h[1])
        assert n - U.dim() == q - 2
    if n - U.dim() == 1:
        if len(pool) < 2:
            return None
        (i1, i2), pool = pool[:2], pool[2:]
        u, v = U.reduce(lam[:, i1]), U.reduce(lam[:, i2])
        for i, w in ((i1, u), (i2, v)):
            if not w.any():
                x = np.zeros(M, dtype=np.int64); x[i] = 1
                return fin(x)
        c = next(c for c in range(1, p) if not ((v - c * u) % p).any())
        # nontrivial (a, b) in S^2 with a + b c = 0 -> witness
        for a, b in itertools.product(sorted(S), repeat=2):
            if (a or b) and (a + b * c) % p == 0:
                x = np.zeros(M, dtype=np.int64); x[i1] = a; x[i2] = b
                return fin(x)
        tab = {}
        for a, b in itertools.product(sorted(S), repeat=2):
            tab.setdefault((a + b * c) % p, (a, b))
        assert len(tab) == p
        def real1(al, tab=tab, i1=i1, i2=i2):
            a, b = tab[(al[0]) % p]
            return {i1: a, i2: b}
        pieces.append((U.copy(), [i1, i2], real1, [u % p, np.zeros(n, dtype=np.int64)]))
        U.add(u)
        if log is not None:
            log.append((1, 2))
    if not pool:
        return None
    x = np.zeros(M, dtype=np.int64); x[pool[0]] = 1
    return fin(x)

def unwind(lam, pieces, x):
    n = lam.shape[0]
    tau = (-(lam @ x)) % p
    for Uj, X, real, h in reversed(pieces):
        al = next(a for a in F2 if Uj.contains((tau - a[0] * h[0] - a[1] * h[1]) % p))
        if any(al):
            y = real(al)
            for i, v in y.items():
                assert x[i] == 0
                x[i] = v
                tau = (tau - v * lam[:, i]) % p
        assert Uj.contains(tau)
    assert not tau.any()
    assert x.any() and all(int(v) in S for v in x) and not ((lam @ x) % p).any()
    return x

def guarantee_simple(n):
    total = worst = 0; q = n
    while q >= 2:
        worst = max(worst, total + q + 2); total += q + 2; q -= 2
    if q == 1:
        worst = max(worst, total + 2); total += 2
    return max(worst, total + 1)

if __name__ == '__main__':
    for n in (3, 4, 10, 11, 100, 101, 1000, 1001):
        g = guarantee_simple(n)
        print(n, g, g - n * n / 4, 'n^2/4 + 3n/2 + 2 =', n * n / 4 + 1.5 * n + 2)
