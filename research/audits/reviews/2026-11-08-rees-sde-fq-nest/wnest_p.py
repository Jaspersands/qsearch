"""WNEST over F_p: worst-case two-dimensions-per-piece solver for the diagonal SDE with
coefficient set S = P u {0} (P = kappa-th powers), built from the F_3 WNEST of
2026-11-08-rees-sde-p3-nest.md and the label-set gadgets of this folder.  Written for p = 5,
kappa = 2 (where the k = 2 gadget exists for every label set with >= 4 labels, enum_labels_p5.out);
the code is generic and records every label set for which no gadget exists.

Stage at codimension q (V = F_p^a / U, U the realized subgroup):
  pool  = first N(q) unused columns, N(q) = min{N : N - (p/(p-1)) q >= 3p/(p-1) + sqrt(N)}.
  peel  : delete coloops; delete proportionality classes of size >= p (Lemma P keeps
          Delta = |F| - (p/(p-1)) rank non-decreasing).  Classes of size <= p-1 remain.
  select: delta in D(F*) by conditional expectations (Lemma D over F_p): |wt - (1-1/p)N*| <= sigma,
          sigma^2 = (1-1/p)(1/p) sum a_j^2 <= (1-1/p)^2 N*.  X = supp delta; dim D(X) >= |X| - r* >= 3.
  labels: delta' in D(X) with >= 4 joint labels (delta_i, delta'_i) (exists: Lemma J), L' = label set.
  gadget: CNF for L' (gadget_cnf4.solve4, cached); either gain 2 (h_1, h_2 independent mod U) or a
          nonzero S-weighted zero-sum mod U.
Unwinding by Lemma 1 over the chain of pieces.  Every output is re-summed over the original columns.
"""
import sys, math, itertools, time
import numpy as np
from verify_gadget import nullspace_mod, rank_mod
from gadget_cnf4 import solve4
from sparse_tri import Field, Quotient

rng = np.random.default_rng(5)
GADGET_CACHE = {}
INFEASIBLE = []


def pool_size(p, q):
    N = q
    while N - p / (p - 1) * q < 3 * p / (p - 1) + math.sqrt(N):
        N += 1
    return N


def dep_basis(cols, p):
    """cols: list of vectors (in the quotient coordinates); returns basis matrix of D (k x N)."""
    A = np.array(cols, dtype=np.int64).T
    return nullspace_mod(A, p)


def peel(cols, p):
    """returns indices kept (F*), after deleting coloops and proportionality classes of size >= p."""
    idx = list(range(len(cols)))
    while True:
        D = dep_basis([cols[i] for i in idx], p)
        if D.shape[0] == 0:
            return idx, D
        colvecs = [tuple(int(x) for x in D[:, j]) for j in range(len(idx))]
        coloops = [j for j, v in enumerate(colvecs) if not any(v)]
        if coloops:
            idx = [idx[j] for j in range(len(idx)) if j not in set(coloops)]
            continue
        # proportionality classes: normalise each functional by its first nonzero entry
        def canon(v):
            lead = next(x for x in v if x)
            inv = pow(lead, -1, p)
            return tuple((x * inv) % p for x in v)
        classes = {}
        for j, v in enumerate(colvecs):
            classes.setdefault(canon(v), []).append(j)
        big = max(classes.values(), key=len)
        if len(big) >= p:
            idx = [idx[j] for j in range(len(idx)) if j not in set(big)]
            continue
        return idx, D


def pick_codeword(D, p):
    """Lemma D over F_p: codeword delta = x D with (wt - (1-1/p)N)^2 <= Var, by conditional expectations."""
    k, N = D.shape
    mu = 1 - 1 / p

    def Phi(prefix):
        """E[(wt - mu N)^2 | x_1..x_j = prefix] computed exactly."""
        j = len(prefix)
        # f_i(x) = c_i + g_i(x_rest), c_i = sum_{t<j} prefix_t D[t,i], g_i = D[j:, i]
        c = (np.array(prefix, dtype=np.int64) @ D[:j]) % p if j else np.zeros(N, dtype=np.int64)
        G = D[j:]
        const_part = 0.0
        groups = {}
        for i in range(N):
            g = tuple(int(x) for x in G[:, i])
            if not any(g):
                const_part += (1.0 if c[i] else 0.0) - mu
            else:
                lead = next(x for x in g if x)
                inv = pow(lead, -1, p)
                key = tuple((x * inv) % p for x in g)
                groups.setdefault(key, []).append((int(c[i]), lead))
        total = const_part ** 2
        for key, members in groups.items():
            # within the class f_i = c_i + s_i t, t uniform in F_p (s_i = lead)
            acc = 0.0
            for t in range(p):
                sm = sum((1.0 if (ci + si * t) % p else 0.0) - mu for ci, si in members)
                acc += sm * sm
            total += acc / p
        return total

    prefix = []
    for j in range(k):
        best = min(range(p), key=lambda v: Phi(prefix + [v]))
        prefix.append(best)
    delta = (np.array(prefix, dtype=np.int64) @ D) % p
    var0 = Phi([])
    wt = int(np.count_nonzero(delta))
    assert (wt - mu * N) ** 2 <= var0 + 1e-9, (wt, mu * N, var0)
    return delta, var0


def choose_second(delta, DX, p, need=4):
    """delta' in D(X) with >= need distinct joint labels; tries basis vectors, pair sums, random combos."""
    k, n = DX.shape
    cands = [DX[j] for j in range(k)]
    cands += [(DX[i] + DX[j]) % p for i in range(k) for j in range(i + 1, k)]
    for _ in range(200):
        cands.append((rng.integers(0, p, size=k) @ DX) % p)
    best = None
    for d2 in cands:
        labels = {(int(a), int(b)) for a, b in zip(delta, d2)}
        # independence of delta' from delta
        M = np.vstack([delta, d2])
        if rank_mod(M, p) < 2:
            continue
        if best is None or len(labels) > best[0]:
            best = (len(labels), d2, labels)
        if len(labels) >= need:
            return d2, labels
    return (best[1], best[2]) if best else (None, None)


def gadget_for(p, S, labels):
    key = tuple(sorted(labels))
    if key not in GADGET_CACHE:
        r, sol, dt = solve4(p, S, 2, 2, list(key), weak=True)
        GADGET_CACHE[key] = sol if r == 'sat' else None
    return GADGET_CACHE[key]


class Piece:
    def __init__(self, X, labels_per_col, Phi, gamma, h):
        self.X, self.lab, self.Phi, self.gamma, self.h = X, labels_per_col, Phi, gamma, h

    def realizer(self, alpha, p):
        """S-weights on X realizing alpha . h (mod the earlier subgroup)."""
        y = []
        for l in self.lab:
            y.append((alpha[0] * self.Phi[l][0] + alpha[1] * self.Phi[l][1] + self.gamma[alpha][0] * l[0] + self.gamma[alpha][1] * l[1]) % p)
        return y


def solve(F, lam, log=None):
    p, a = F.p, lam.shape[0]
    S = sorted(F.S)
    M = lam.shape[1]
    U = Quotient(a, p)
    pieces = []     # (Piece, dim gained) in order
    pool = list(range(M))
    consumed = 0
    while U.dim() < a:
        q = a - U.dim()
        if q <= 2:
            # one-dimensional contraction rounds (as in sparse_tri) for the last codimensions
            res = finish_1d(F, lam, U, pieces, pool, log)
            return res
        N = pool_size(p, q)
        if len(pool) < N:
            return None
        Fidx, pool = pool[:N], pool[N:]
        cols = [U.reduce(lam[:, i]) for i in Fidx]
        zero = [i for i, c in zip(Fidx, cols) if not c.any()]
        if zero:
            # a column lying in U: closes
            x = np.zeros(M, dtype=np.int64); x[zero[0]] = 1
            return unwind(F, lam, U, pieces, x, lam[:, zero[0]].copy())
        kept, D = peel(cols, p)
        Fstar = [Fidx[j] for j in kept]
        Nstar = len(Fstar)
        rstar = rank_mod(np.array([cols[j] for j in kept], dtype=np.int64), p)
        assert D.shape[0] == Nstar - rstar
        delta, var0 = pick_codeword(D, p)
        wt = int(np.count_nonzero(delta))
        assert wt >= rstar + 3, (wt, rstar, Nstar, var0)
        X = [Fstar[j] for j in range(Nstar) if delta[j]]
        dX = delta[delta != 0]
        pool = [Fidx[j] for j in range(N) if Fidx[j] not in set(X)] + pool
        colsX = [U.reduce(lam[:, i]) for i in X]
        DX = dep_basis(colsX, p)
        assert DX.shape[0] >= 3
        # genuine D(X)-classes
        classes = {}
        for j in range(len(X)):
            classes.setdefault(tuple(int(x) for x in DX[:, j]), []).append(j)
        if len(classes) <= DX.shape[0]:
            # c <= k: every class sum is 0 mod U -> a class is a zero-sum
            cl = next(iter(classes.values()))
            x = np.zeros(M, dtype=np.int64)
            for j in cl:
                x[X[j]] = 1
            rho = (lam @ x) % p
            assert U.contains(rho)
            return unwind(F, lam, U, pieces, x, rho)
        if len(set(int(v) for v in dX)) == 1:
            x = np.zeros(M, dtype=np.int64)
            for i in X:
                x[i] = 1
            rho = (lam @ x) % p
            assert U.contains(rho)
            return unwind(F, lam, U, pieces, x, rho)
        d2, labels = choose_second(dX, DX, p)
        assert d2 is not None and len(labels) >= 4, (len(labels) if labels else None)
        sol = gadget_for(p, S, labels)
        if sol is None:
            INFEASIBLE.append(sorted(labels))
            raise RuntimeError(f'no gadget for label set {sorted(labels)}')
        Phi, gamma = sol
        labcol = [(int(a_), int(b_)) for a_, b_ in zip(dX, d2)]
        h = []
        for j in range(2):
            hj = np.zeros(a, dtype=np.int64)
            for i, l in zip(X, labcol):
                hj = (hj + Phi[l][j] * lam[:, i]) % p
            h.append(hj)
        piece = Piece(X, labcol, Phi, gamma, h)
        # independence mod U?
        Utest = Quotient(a, p)
        for row in U.B:
            Utest.add(row)
        indep = True
        for alpha in itertools.product(range(p), repeat=2):
            if not any(alpha):
                continue
            val = (alpha[0] * h[0] + alpha[1] * h[1]) % p
            if U.contains(val):
                indep = False
                y = piece.realizer(alpha, p)
                assert any(y)
                x = np.zeros(M, dtype=np.int64)
                for i, yi in zip(X, y):
                    x[i] = yi
                rho = (lam @ x) % p
                assert U.contains(rho)
                return unwind(F, lam, U, pieces, x, rho)
        consumed += len(X)
        if log is not None:
            log.append((q, N, Nstar, rstar, wt, len(labels)))
        pieces.append(piece)
        U.add(h[0]); U.add(h[1])
    if not pool:
        return None
    x = np.zeros(M, dtype=np.int64); x[pool[0]] = 1
    return unwind(F, lam, U, pieces, x, lam[:, pool[0]].copy())


def finish_1d(F, lam, U, pieces, pool, log):
    """last codimensions (q <= 2) with one contraction round each (pool q + 1, full dependency)."""
    p, a = F.p, lam.shape[0]
    M = lam.shape[1]
    while U.dim() < a:
        q = a - U.dim()
        if len(pool) < q + 1:
            return None
        Fidx, pool = pool[:q + 1], pool[q + 1:]
        cols = np.array([U.reduce(lam[:, i]) for i in Fidx], dtype=np.int64).T
        D = nullspace_mod(cols, p)
        delta = D[0]
        X = [Fidx[j] for j in range(q + 1) if delta[j]]
        dX = delta[delta != 0]
        pool = [Fidx[j] for j in range(q + 1) if not delta[j]] + pool
        v = np.zeros(a, dtype=np.int64)
        for i, d in zip(X, dX):
            v = (v + F.beta[F.cos[int(d)]] * d * lam[:, i]) % p
        if log is not None:
            log.append((q, q + 1, q + 1, q, len(X), 0))
        if U.contains(v):
            x = np.zeros(M, dtype=np.int64)
            for i, wi in zip(X, F.weights(dX, 1)):
                x[i] = wi
            rho = (lam @ x) % p
            return unwind(F, lam, U, pieces, x, rho)
        pieces.append(('1d', X, dX, v.copy()))
        U.add(v)
    if not pool:
        return None
    x = np.zeros(M, dtype=np.int64); x[pool[0]] = 1
    return unwind(F, lam, U, pieces, x, lam[:, pool[0]].copy())


def unwind(F, lam, U, pieces, x, rho):
    p, a = F.p, lam.shape[0]
    tau = (-rho) % p
    for j in range(len(pieces) - 1, -1, -1):
        Uj = Quotient(a, p)
        for pc in pieces[:j]:
            if isinstance(pc, tuple):
                Uj.add(pc[3])
            else:
                Uj.add(pc.h[0]); Uj.add(pc.h[1])
        pc = pieces[j]
        if isinstance(pc, tuple):
            _, X, dX, v = pc
            zeta = next(z for z in range(p) if Uj.contains((tau - z * v) % p))
            if zeta:
                w = F.weights(dX, zeta)
                for i, wi in zip(X, w):
                    assert x[i] == 0
                    x[i] = wi
                    tau = (tau - wi * lam[:, i]) % p
        else:
            alpha = next(al for al in itertools.product(range(p), repeat=2)
                         if Uj.contains((tau - al[0] * pc.h[0] - al[1] * pc.h[1]) % p))
            if any(alpha):
                y = pc.realizer(alpha, p)
                for i, yi in zip(pc.X, y):
                    assert x[i] == 0
                    x[i] = yi
                    tau = (tau - yi * lam[:, i]) % p
        assert Uj.contains(tau)
    assert not tau.any()
    return x


def guarantee(p, n):
    """columns needed by the recursion: stages q = n, n-2, ... >= 3 each costing <= (1-1/p)N + sigma, then 1-d rounds."""
    total = 0
    worst = 0
    q = n
    stages = []
    while q >= 3:
        N = pool_size(p, q)
        cost = math.floor((1 - 1 / p) * N + (1 - 1 / p) * math.sqrt(N))
        worst = max(worst, total + N)
        total += cost
        stages.append((q, N, cost))
        q -= 2
    while q >= 1:
        worst = max(worst, total + q + 1)
        total += q + 1
        q -= 1
    worst = max(worst, total + 1)
    return worst, stages


def main():
    p, kappa = 5, 2
    F = Field(p, kappa)
    print(f'p={p} kappa={kappa} S={sorted(F.S)}')
    for n in (10, 20, 30, 40, 60):
        g, stages = guarantee(p, n)
        print(f'n={n}: guarantee {g} ({g/n**2:.3f} n^2); KOW F_5 (+-1) recursion ~ 0.4 n^2 + O(n log n); triangular {(n+1)*(n+2)//2}; n^2/4 = {n*n/4:.0f}', flush=True)
        trials = 12 if n <= 30 else 4
        used = []
        for t in range(trials):
            kind = t % 4
            M = g
            if kind == 0:
                lam = rng.integers(0, p, size=(n, M))
            elif kind == 1:
                B = rng.integers(0, p, size=(n, max(2, n // 2)))
                lam = (B @ rng.integers(0, p, size=(B.shape[1], M))) % p
            elif kind == 2:
                poolc = rng.integers(0, p, size=(n, n + 3))
                lam = poolc[:, rng.integers(0, n + 3, size=M)]
            else:
                lam = (rng.integers(0, p, size=(n, M)) * (rng.random((n, M)) < 0.2)) % p
            lam = lam.astype(np.int64)
            log = []
            x = solve(F, lam, log=log)
            assert x is not None, 'ran out of columns within the guarantee'
            assert x.any() and all(int(v) in F.S for v in x) and not ((lam @ x) % p).any()
            cons = sum(e[4] for e in log)
            used.append(cons)
            if t == 0:
                print('   stages (q, N, N*, r*, |X|, #labels):', log[:4], '...')
        print(f'   {trials} instances (random/low-rank/few-distinct/sparse): all witnesses verified; columns consumed {min(used)}..{max(used)}; gadget cache {len(GADGET_CACHE)} label sets, infeasible {len(INFEASIBLE)}', flush=True)


if __name__ == '__main__':
    main()
