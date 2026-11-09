"""Referee's own minimal implementation of WNEST exactly as proved in the note (section 2).

Stages: codimension q >= 4 -> pool = first N(q) unconsumed columns (input order), peel coloops and
proportionality classes of size >= 3, Lemma D codeword by conditional expectations, Lemma G gadget;
q <= 3 -> KOW round with pool q+1.  The realized subgroup is kept as a chain W_0 < W_1 < ...; each
stage stores an explicit table quotient-element -> 0/1 subset, and the final witness is built by back
substitution and re-summed over the ORIGINAL vectors.  Every per-piece claim of the proof is asserted.
"""
import math
import numpy as np
from f3 import rref, rank, nullspace, solve, normalize

CL = [(a, b) for a in (1, 2) for b in range(3)]
UNION = {(0, 1): {(1, 1), (1, 2), (2, 2)}, (0, 2): {(1, 2), (2, 1), (2, 2)},
         (1, 0): {(1, 0), (1, 1), (2, 0)}, (1, 1): {(1, 0), (2, 0), (2, 1)},
         (1, 2): set(CL), (2, 0): {(1, 1), (2, 0), (2, 2)}, (2, 1): {(2, 0), (2, 1), (2, 2)},
         (2, 2): {(1, 0), (1, 2), (2, 1)}}


def Nq(q):
    N = 1
    while N - 1.5 * q < 3 + math.sqrt(N):
        N += 1
    return N


def theorem_bound(n):
    return n * n / 4 + (8 / 9) * (n + 2) ** 1.5 + 4 * n + 2 * math.sqrt(n) + 15


class Fail(Exception):
    pass


class Quot:
    """F_3^n modulo a subspace W (RREF basis); coordinates = non-pivot entries after reduction."""
    def __init__(self, n, Wrows):
        self.n = n
        if len(Wrows):
            self.R, self.piv = rref(np.array(Wrows))
        else:
            self.R, self.piv = np.zeros((0, n), dtype=np.int64), []
        self.free = [c for c in range(n) if c not in set(self.piv)]

    def red(self, v):
        v = np.array(v, dtype=np.int64) % 3
        for i, p in enumerate(self.piv):
            if v[p]:
                v = (v - v[p] * self.R[i]) % 3
        return v[self.free]


class WNEST:
    def __init__(self, vecs):
        self.v = [np.array(x, dtype=np.int64) % 3 for x in vecs]
        self.n = len(self.v[0])
        self.unused = list(range(len(self.v)))   # input order
        self.pulled = 0                          # max index+1 ever placed in a pool (columns needed)
        self.Wrows = []                          # original-space generators of the realized subgroup
        self.stages = []                         # (Quot of W_{j-1}, {quotient elt tuple: subset})
        self.log = []

    def qdim(self):
        return self.n - (rank(np.array(self.Wrows)) if self.Wrows else 0)

    def pool(self, k):
        if len(self.unused) < k:
            raise Fail(f"need pool {k}, only {len(self.unused)} unused")
        P = self.unused[:k]
        self.pulled = max(self.pulled, max(P) + 1)
        return P

    def osum(self, S):
        return sum((self.v[i] for i in S), np.zeros(self.n, dtype=np.int64)) % 3

    # ---- witness by back substitution (Lemma 1 iterated)
    def finish(self, T):
        T = list(T)
        assert len(T) > 0
        t = self.osum(T)
        S = set(T)
        for Q, table in reversed(self.stages):
            key = tuple(int(x) for x in (-Q.red(t)) % 3)
            assert key in table, "target not in realized subgroup"
            U = table[key]
            assert not (S & set(U))
            S |= set(U)
            t = (t + self.osum(U)) % 3
        assert not np.any(t)
        S = sorted(S)
        assert len(S) > 0 and not np.any(self.osum(S)), "witness does not sum to zero"
        return S

    def consume(self, X):
        Xs = set(X)
        self.unused = [i for i in self.unused if i not in Xs]

    # ---- one WNEST stage at codimension q >= 4
    def stage(self, q):
        Q = Quot(self.n, self.Wrows)
        N = Nq(q)
        P = self.pool(N)
        cols = {i: Q.red(self.v[i]) for i in P}
        for i in P:
            if not np.any(cols[i]):
                self.end = 'step0'; return self.finish([i])   # step 0
        F = list(P)
        def Mat(S):
            return np.array([cols[i] for i in S]).T
        delta0 = len(F) - 1.5 * rank(Mat(F))
        assert delta0 >= N - 1.5 * q and N - 1.5 * q >= 3 + math.sqrt(N)
        maxcls = 1
        while True:                                            # step 1 peel
            M = Mat(F); r = rank(M); B = nullspace(M)
            assert len(B) > 0, "dependency code vanished"
            colo = [F[j] for j in range(len(F)) if not np.any(B[:, j])]
            if colo:
                F2 = [i for i in F if i not in set(colo)]
            else:
                cls = {}
                for j in range(len(F)):
                    cls.setdefault(normalize(B[:, j]), []).append(F[j])
                A = max(cls.values(), key=len)
                if len(A) < 3:
                    break
                maxcls = max(maxcls, len(A))
                F2 = [i for i in F if i not in set(A)]
                r2 = rank(Mat(F2)) if F2 else 0
                assert r - r2 >= len(A) - 1, "Lemma P violated"
            r2 = rank(Mat(F2)) if F2 else 0
            assert (len(F2) - 1.5 * r2) >= (len(F) - 1.5 * r) - 1e-9, "Delta decreased"
            F = F2
            assert F, "peeled to empty"
        Ns, rs = len(F), r
        assert Ns - 1.5 * rs >= 3 + math.sqrt(Ns) - 1e-9
        # Lemma M quantities
        sizes = [len(c) for c in cls.values()]
        var9 = 2 * sum(a * a for a in sizes)                    # 9 Var
        assert max(sizes) <= 2 and var9 <= 4 * Ns
        # step 2 select: conditional expectations, exact integer 27*Phi
        k = B.shape[0]; pre = []
        for j in range(k):
            best = None
            for val in range(3):
                ph = self.phi27(B, pre + [val])
                if best is None or ph < best[0]:
                    best = (ph, val)
            pre.append(best[1])
        d = (np.array(pre) @ B) % 3
        wt = int(np.count_nonzero(d))
        assert (3 * wt - 2 * Ns) ** 2 <= var9, "Lemma D window violated"
        assert wt >= rs + 2, "weight below r*+2"
        assert wt <= 2 * N / 3 + 2 * math.sqrt(N) / 3 + 1e-9
        assert wt <= q + (8 / 3) * math.sqrt(q) + 4 + 1e-9
        X = [F[j] for j in range(len(F)) if d[j]]
        dl = {F[j]: int(d[j]) for j in range(len(F)) if d[j]}
        assert not np.any(Mat(X) @ np.array([dl[i] for i in X]) % 3)
        # step 3 gadget
        BX = nullspace(Mat(X))
        assert BX.shape[0] >= 2, "dim D(X) < 2"
        dvec = np.array([dl[i] for i in X])
        dp = next(b for b in BX if rank(np.vstack([dvec, b])) == 2)
        cls6 = {c: [] for c in CL}
        for i, a, b in zip(X, dvec, dp):
            cls6[(int(a), int(b))].append(i)
        U = {al: sorted(sum((cls6[c] for c in UNION[al]), [])) for al in UNION}
        h1 = Q.red(self.osum(U[(1, 0)])); h2 = Q.red(self.osum(U[(0, 1)]))
        for al, S in U.items():
            assert np.array_equal(Q.red(self.osum(S)), (al[0] * h1 + al[1] * h2) % 3), "gadget identity"
        if rank(np.vstack([h1, h2])) == 2:
            table = {tuple([0] * len(h1)): []}
            for al, S in U.items():
                table[tuple(int(x) for x in (al[0] * h1 + al[1] * h2) % 3)] = S
            assert len(table) == 9
            self.stages.append((Q, table))
            self.Wrows += [self.osum(U[(1, 0)]), self.osum(U[(0, 1)])]
            self.consume(X)
            self.log.append(dict(q=q, N=N, Ns=Ns, rs=rs, wt=wt, maxcls=maxcls, gain=2, c2=sum(1 for a in sizes if a == 2), var9=var9))
            return None
        for al in UNION:                                       # degenerate: zero-sum union
            if not np.any((al[0] * h1 + al[1] * h2) % 3) and U[al]:
                self.log.append(dict(q=q, degenerate=al)); self.end = 'gadget-degenerate'
                return self.finish(U[al])
        raise AssertionError("degenerate gadget without nonempty zero-sum union")

    @staticmethod
    def phi27(B, prefix):
        k, N = B.shape; j = len(prefix)
        c = (np.array(prefix, dtype=np.int64) @ B[:j]) % 3
        G = B[j:]
        const = 0; groups = {}
        for i in range(N):
            g = G[:, i]
            if not np.any(g):
                const += 3 * (c[i] != 0) - 2
            else:
                s = int(g[np.nonzero(g)[0][0]])
                groups.setdefault(normalize(g), []).append((int(c[i]), s))
        tot = 3 * const * const
        for lst in groups.values():
            for t in range(3):
                ss = sum(3 * ((ci + si * t) % 3 != 0) - 2 for ci, si in lst)
                tot += ss * ss
        return tot

    # ---- KOW round at codimension q <= 3
    def kow(self, q):
        Q = Quot(self.n, self.Wrows)
        P = self.pool(q + 1)
        cols = [Q.red(self.v[i]) for i in P]
        for i, c in zip(P, cols):
            if not np.any(c):
                self.end = 'kow-step0'; return self.finish([i])
        B = nullspace(np.array(cols).T)
        d = B[0]
        A = [P[j] for j in range(len(P)) if d[j] == 1]; Bs = [P[j] for j in range(len(P)) if d[j] == 2]
        u = Q.red(self.osum(A))
        assert np.array_equal(u, Q.red(self.osum(Bs)))
        if not np.any(u):
            self.end = 'kow-u0'; return self.finish(A if A else Bs)
        table = {tuple([0] * len(u)): [], tuple(int(x) for x in u): A,
                 tuple(int(x) for x in (2 * u) % 3): sorted(A + Bs)}
        self.stages.append((Q, table))
        self.Wrows.append(self.osum(A))
        self.consume(A + Bs)
        self.log.append(dict(q=q, kow=len(A + Bs), gain=1))
        return None

    def run(self):
        while True:
            q = self.qdim()
            if q == 0:
                P = self.pool(1); self.end = 'final-column'
                return self.finish(P[:1])
            res = self.stage(q) if q >= 4 else self.kow(q)
            if res is not None:
                return res
            assert self.qdim() == q - (2 if q >= 4 else 1)


def guarantee(n):
    """Exact per-piece recursion (my own): pool N(q), piece cost <= floor(2N/3 + (2/3)sqrt N)."""
    consumed, best, q = 0, 0, n
    while q > 0:
        if q >= 4:
            N = Nq(q); best = max(best, consumed + N)
            consumed += math.floor(2 * N / 3 + 2 * math.sqrt(N) / 3); q -= 2
        else:
            best = max(best, consumed + q + 1); consumed += q + 1; q -= 1
    return max(best, consumed + 1)
