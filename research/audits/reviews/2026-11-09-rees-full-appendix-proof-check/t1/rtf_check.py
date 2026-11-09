"""t1 check of thm:ring-to-field, (M1)-(M3), lem:tb-quotient-oracle, lem:tb-section-rank,
prop:tb-recursion and cor:tb-correspondence on small finite Lazard rings over Z/p^e.

For each ring: enumerate ALL Lie subrings h (BFS on HNF lattices); for each, build the real hiding
function f (left cosets of exp h in (L,*), * = truncated BCH), and run Algorithm RtF with
  - (M1) Smith form presentation of S/K, normal-form section sigma (column convention, as in the paper),
  - (M3) socle basis p^{a_i-1}u_i and tensor by exact division,
  - (M2) idealizer, computed by brute force and compared with the group normalizer (cor (b)),
  - the field call replaced by an oracle that reads the hidden subgroup of f o sigma o iota_M
    directly (truth), or, in adversarial mode, returns random subspaces/subalgebras.
Checks: hiding property of f o sigma o iota_M (all pairs, or generators+count), the paper's claim
U = iota^{-1}((h/K) cap M[p]); output = h; calls <= b and <= log_p|H|+1 on the truth branch;
calls <= b on every adversarial branch; K ideal of S on every branch; section rank/class bounds;
without stop rule 1, H = G in Z/p^b costs b+1 calls. Finite checks only.
"""
import sys, itertools, random, json, math
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, ".")
from lazard_words import TA


def egcd(a, b):
    if b == 0:
        return (abs(a), (1 if a >= 0 else -1), 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)


class Ring:
    def __init__(self, name, p, e, brackets):
        self.name, self.p, self.e, self.m = name, p, list(e), len(e)
        m = self.m
        self.mods = np.array([p ** x for x in e], dtype=np.int64)
        self.M = p ** max(e)
        C = np.zeros((m, m, m), dtype=np.int64)
        for (i, j), vec in brackets.items():
            for k, v in enumerate(vec):
                C[i, j, k] = v % self.mods[k]
                C[j, i, k] = (-v) % self.mods[k]
        self.C = C
        self.N = int(np.prod(self.mods))
        self.stride = np.array([int(np.prod(self.mods[i + 1:])) for i in range(m)], dtype=np.int64)
        self.all = np.array(list(itertools.product(*[range(int(x)) for x in self.mods])), dtype=np.int64)
        self.D = [tuple(int(self.mods[i]) if j == i else 0 for j in range(m)) for i in range(m)]
        self._check()
        self.cls = self.lcs_class_full()
        assert self.cls < p, (name, self.cls)
        A = TA(self.cls)
        bch = A.bch({(0,): Fr(1)}, {(1,): Fr(1)})
        self.bterms = []
        for w, v in sorted(bch.items(), key=lambda t: (len(t[0]), t[0])):
            r = v / len(w)
            self.bterms.append((w, (r.numerator * pow(r.denominator, -1, self.M)) % self.M))
        self.R = self.dquot(self.hnf_closure_add(self.brackets_of(self.unit_rows())), self.zero())

    # ---------- basic ops ----------
    def red(self, X):
        return np.mod(X, self.mods)

    def br(self, A, B):
        return self.red(np.einsum('...i,...j,ijk->...k', A, B, self.C))

    def bch(self, A, B):
        A, B = np.broadcast_arrays(A, B)
        vals = {(0,): A, (1,): B}
        res = np.zeros_like(A)
        def get(w):
            if w not in vals:
                vals[w] = self.br(get(w[:-1]), vals[(w[-1],)])
            return vals[w]
        for w, beta in self.bterms:
            res = res + beta * get(w)
        return self.red(res)

    def neg(self, A):
        return self.red(-A)

    def idx(self, X):
        return (X @ self.stride)

    def _check(self):
        m, mods, C = self.m, self.mods, self.C
        for i in range(m):
            for j in range(m):
                for k in range(m):
                    # well-definedness: p^{e_i} [eps_i, eps_j] = 0 in L
                    assert (mods[i] * C[i, j, k]) % mods[k] == 0, ("ill-defined", self.name, i, j, k)
            assert all(C[i, i, k] == 0 for k in range(m))
        E = np.eye(m, dtype=np.int64)
        for i, j, k in itertools.product(range(m), repeat=3):
            a, b, c = E[i], E[j], E[k]
            J = self.br(a, self.br(b, c)) + self.br(b, self.br(c, a)) + self.br(c, self.br(a, b))
            assert not self.red(J).any(), ("Jacobi", self.name, i, j, k)

    # ---------- lattices: row HNF of generators + D ----------
    def zero(self):
        return self.hnf([])

    def unit_rows(self):
        return self.hnf([tuple(int(i == j) for j in range(self.m)) for i in range(self.m)])

    def hnf(self, rows):
        m, mods = self.m, [int(x) for x in self.mods]
        A = [list(r) for r in rows] + [list(r) for r in self.D]
        H = []
        for col in range(m):
            A = A + [list(self.D[k]) for k in range(col, m)]  # D rows lie in the lattice
            piv, rest = None, []
            for r in A:
                if r[col] != 0:
                    if piv is None:
                        piv = r
                    else:
                        a, b = piv[col], r[col]
                        g, s, t = egcd(a, b)
                        newp = [s * x + t * y for x, y in zip(piv, r)]
                        rr = [(b // g) * x - (a // g) * y for x, y in zip(piv, r)]
                        piv = newp
                        rest.append(rr)
                else:
                    rest.append(r)
            if piv[col] < 0:
                piv = [-x for x in piv]
            for k in range(col + 1, m):
                piv[k] %= mods[k]
            for r in rest:
                for k in range(col + 1, m):
                    r[k] %= mods[k]
            H.append(piv)
            A = rest
        for i in range(m):
            for j in range(i):
                q = H[j][i] // H[i][i]
                if q:
                    H[j] = [x - q * y for x, y in zip(H[j], H[i])]
        return tuple(tuple(r) for r in H)

    def member(self, H, v):
        v = list(v)
        for i in range(self.m):
            if v[i] % H[i][i]:
                return False
            q = v[i] // H[i][i]
            if q:
                v = [x - q * y for x, y in zip(v, H[i])]
        return True

    def reduce_all(self, H, X):
        X = X.copy()
        for i in range(self.m):
            q = X[:, i] // H[i][i]
            X -= q[:, None] * np.array(H[i], dtype=np.int64)[None, :]
        return X

    def size(self, H):
        return int(np.prod(self.mods)) // int(np.prod([H[i][i] for i in range(self.m)]))

    def elements(self, H):
        rng_ = [range(int(self.mods[i]) // H[i][i]) for i in range(self.m)]
        T = np.array(list(itertools.product(*rng_)), dtype=np.int64)
        return self.red(T @ np.array(H, dtype=np.int64))

    def brackets_of(self, H):
        rows = np.array(H, dtype=np.int64)
        out = []
        for i in range(self.m):
            for j in range(self.m):
                out.append(tuple(int(x) for x in self.br(rows[i], rows[j])))
        return out

    def hnf_closure_add(self, rows):
        return self.hnf(rows)

    def lie_closure(self, rows):
        H = self.hnf(rows)
        while True:
            new = [v for v in self.brackets_of(H) if not self.member(H, v)]
            if not new:
                return H
            H = self.hnf(list(H) + new)

    def is_subring(self, H):
        return all(self.member(H, v) for v in self.brackets_of(H))

    def contains(self, A, B):  # B subset of A
        return all(self.member(A, r) for r in B)

    def span_br(self, A, B):  # additive span of [a,b]
        ra, rb = np.array(A, dtype=np.int64), np.array(B, dtype=np.int64)
        return self.hnf([tuple(int(x) for x in self.br(ra[i], rb[j])) for i in range(self.m) for j in range(self.m)])

    def add_lat(self, A, B):
        return self.hnf(list(A) + list(B))

    def dquot(self, A, B):
        """d(A/B) for lattices B subset A: number of nontrivial invariant factors"""
        BA = Fmat_inv_mul(A, B, self.m)
        delta, _, _ = snf(BA)
        return sum(1 for d in delta if d != 1)

    def lcs_class_full(self):
        S = self.unit_rows()
        g = S
        for j in range(1, 60):
            g2 = self.span_br(S, g)
            if g2 == self.zero():
                return j
            g = g2
        raise RuntimeError

    def class_section(self, S, K):
        g = S
        for j in range(1, 60):
            if self.contains(K, g):
                return j - 1
            g = self.add_lat(self.span_br(S, g), K)
        raise RuntimeError


# ---------- exact integer matrix helpers (column convention for (M1)) ----------

def mat_inv_frac(B):
    n = len(B)
    A = [[Fr(B[i][j]) for j in range(n)] + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def Fmat_inv_mul(A, B, m):
    """lattices as row-HNF tuples; column bases B_A = A^T; return integer C = B_A^{-1} B_B"""
    BA, BB = transpose(A), transpose(B)
    C = matmul(mat_inv_frac(BA), BB)
    out = []
    for r in C:
        row = []
        for x in r:
            assert x.denominator == 1, "K not inside S"
            row.append(int(x))
        out.append(row)
    return out


def snf(C):
    """Smith normal form with transforms: P C Q = diag(delta), P, Q unimodular. Returns (delta, P, Q)."""
    n = len(C)
    A = [list(r) for r in C]
    P = [[int(i == j) for j in range(n)] for i in range(n)]
    Q = [[int(i == j) for j in range(n)] for i in range(n)]

    def rowop(i, j, f):  # row_i += f * row_j
        A[i] = [x + f * y for x, y in zip(A[i], A[j])]
        P[i] = [x + f * y for x, y in zip(P[i], P[j])]

    def colop(i, j, f):  # col_i += f * col_j
        for r in range(n):
            A[r][i] += f * A[r][j]
            Q[r][i] += f * Q[r][j]

    def swaprow(i, j):
        A[i], A[j] = A[j], A[i]
        P[i], P[j] = P[j], P[i]

    def swapcol(i, j):
        for r in range(n):
            A[r][i], A[r][j] = A[r][j], A[r][i]
            Q[r][i], Q[r][j] = Q[r][j], Q[r][i]

    for t in range(n):
        while True:
            nz = [(abs(A[i][j]), i, j) for i in range(t, n) for j in range(t, n) if A[i][j] != 0]
            if not nz:
                return [A[i][i] for i in range(n)], P, Q
            _, i, j = min(nz)
            swaprow(t, i)
            swapcol(t, j)
            done = True
            for i in range(t + 1, n):
                q = A[i][t] // A[t][t]
                if q:
                    rowop(i, t, -q)
                if A[i][t]:
                    done = False
            for j in range(t + 1, n):
                q = A[t][j] // A[t][t]
                if q:
                    colop(j, t, -q)
                if A[t][j]:
                    done = False
            if not done:
                continue
            bad = [(i, j) for i in range(t + 1, n) for j in range(t + 1, n) if A[i][j] % A[t][t]]
            if bad:
                i, j = bad[0]
                rowop(t, i, 1)
                continue
            if A[t][t] < 0:
                A[t] = [-x for x in A[t]]
                P[t] = [-x for x in P[t]]
            break
    return [A[i][i] for i in range(n)], P, Q


# ---------- the explicit F_p algebra Omega ----------

class FpAlg:
    def __init__(self, p, T):
        self.p = p
        self.k = T.shape[0]
        self.T = T % p
        cls = self.lcs_dims()
        self.cls = cls[0]
        self.derived = cls[1]
        A = TA(max(self.cls, 1))
        bch = A.bch({(0,): Fr(1)}, {(1,): Fr(1)})
        self.bterms = []
        for w, v in sorted(bch.items(), key=lambda t: (len(t[0]), t[0])):
            r = v / len(w)
            self.bterms.append((w, (r.numerator * pow(r.denominator, -1, p)) % p))

    def br(self, A, B):
        return np.mod(np.einsum('...i,...j,ijk->...k', A, B, self.T), self.p)

    def bch(self, A, B):
        A, B = np.broadcast_arrays(A, B)
        vals = {(0,): A, (1,): B}
        res = np.zeros_like(A)
        def get(w):
            if w not in vals:
                vals[w] = self.br(get(w[:-1]), vals[(w[-1],)])
            return vals[w]
        for w, beta in self.bterms:
            res = res + beta * get(w)
        return np.mod(res, self.p)

    def rank(self, rows):
        return len(rref(rows, self.p))

    def lcs_dims(self):
        k, p = self.k, self.p
        E = np.eye(k, dtype=np.int64)
        g = [tuple(r) for r in E]
        dims = [k]
        cls = 0
        while True:
            G = rref(g, p)
            if not G:
                break
            cls += 1
            new = [tuple(self.br(E[i], np.array(v, dtype=np.int64))) for i in range(k) for v in G]
            g = new
            dims.append(len(rref(g, p)))
        derived = dims[1] if len(dims) > 1 else 0
        return cls, derived

    def closed(self, basis):
        if not basis:
            return True
        r0 = len(rref(basis, self.p))
        for a in basis:
            for b in basis:
                v = tuple(self.br(np.array(a), np.array(b)))
                if len(rref(list(basis) + [v], self.p)) > r0:
                    return False
        return True


def rref(rows, p):
    A = [list(int(x) % p for x in r) for r in rows]
    out = []
    if not A:
        return out
    n = len(A[0])
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return [tuple(x) for x in A[:r]]


# ---------- enumeration of Lie subrings ----------

def all_subrings(L, limit=200000):
    start = L.zero()
    seen = {start}
    queue = [start]
    p = L.p
    while queue:
        H = queue.pop()
        # candidates g with p g in H, g not in H, canonical mod H
        X = L.reduce_all(H, L.all)
        pX = L.red(p * L.all)
        mem = np.array([L.member(H, v) for v in pX]) if L.N <= 4000 else None
        reps = set()
        for i in range(L.N):
            if mem is not None and not mem[i]:
                continue
            v = tuple(int(x) for x in X[i])
            if any(v):
                reps.add(v)
        for g in reps:
            H2 = L.lie_closure(list(H) + [g])
            if H2 not in seen:
                seen.add(H2)
                queue.append(H2)
                if len(seen) > limit:
                    raise RuntimeError("too many")
    return sorted(seen, key=lambda H: L.size(H))


# ---------- hiding function ----------

def coset_labels(L, H):
    """labels of left cosets x*H, via union-find under right multiplication by the HNF rows of H
    (additive generators). Checks that the class of 0 equals H as a set (cor (a), 2nd sentence)."""
    parent = np.arange(L.N)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for h in H:
        h = np.mod(np.array(h, dtype=np.int64), L.mods)
        if not h.any():
            continue
        Y = L.bch(L.all, h[None, :])
        iy = L.idx(Y)
        for a, b in zip(range(L.N), iy):
            ra, rb = find(a), find(int(b))
            if ra != rb:
                parent[ra] = rb
    lab = np.array([find(a) for a in range(L.N)])
    # class of 0 must be the set H
    zero_cls = set(np.nonzero(lab == lab[0])[0].tolist())
    Hset = set(L.idx(L.elements(H)).tolist())
    assert zero_cls == Hset, "group generated by additive generators != H"
    sizes = np.unique(lab, return_counts=True)[1]
    assert (sizes == L.size(H)).all()
    return lab


# ---------- RtF ----------

class Stats:
    def __init__(self):
        self.d = dict(runs=0, hiding_checked=0, U_claim_ok=0, max_calls_minus_b=-99, rounds=0,
                      normalizer_checked=0, section_checks=0, idealizer_eq_normalizer=0)

    def bump(self, k, v=1):
        self.d[k] = self.d.get(k, 0) + v


def present_section(L, S, K):
    """(M1) in the paper's column convention. Returns (delta list, u list (vectors), coord function, sigma)."""
    C = Fmat_inv_mul(S, K, L.m)          # B_S^{-1} B_K
    delta, P, Q = snf(C)
    BS = transpose(S)
    Pinv = [[int(x) for x in r] for r in mat_inv_frac(P)]
    W = matmul(BS, Pinv)                  # columns w_i
    keep = [i for i, d in enumerate(delta) if d != 1]
    for d in delta:
        assert d > 0 and (d & (d - 1) == 0 or True)
        x = d
        while x % L.p == 0:
            x //= L.p
        assert x == 1, "delta not a power of p"
    us = [np.mod(np.array([W[r][i] for r in range(L.m)], dtype=np.int64), L.mods) for i in keep]
    PBSinv = matmul(P, mat_inv_frac(BS))  # Fractions
    dk = [delta[i] for i in keep]

    def coord(y):  # y integer vector in Lambda_S
        t = [sum(PBSinv[i][j] * int(y[j]) for j in range(L.m)) for i in range(L.m)]
        out = []
        for i, d in zip(keep, dk):
            assert t[i].denominator == 1, "y not in Lambda_S"
            out.append(int(t[i]) % d)
        return out

    def sigma(T):  # T array (n, len(keep))
        X = np.zeros((T.shape[0], L.m), dtype=np.int64)
        for i, u in enumerate(us):
            X = X + T[:, i:i + 1] * u[None, :]
        return L.red(X)
    return dk, us, coord, sigma


def socle(L, dk, us, coord):
    """(M3): basis p^{a_i-1} u_i and the F_p tensor by exact division."""
    p = L.p
    a = [int(round(math.log(d, p))) for d in dk]
    k = len(dk)
    sb = [L.red(u * (p ** (ai - 1))) for u, ai in zip(us, a)]
    T = np.zeros((k, k, k), dtype=np.int64)
    for i in range(k):
        for j in range(k):
            v = L.br(sb[i], sb[j])
            t = coord(v)
            for kk in range(k):
                q = p ** (a[kk] - 1)
                assert t[kk] % q == 0, "socle coefficient not divisible"
                T[i, j, kk] = (t[kk] // q) % p
    return a, T


def idealizer(L, S, K):
    """I_S(K) by brute force over the elements of S."""
    X = L.elements(S)
    ok = np.ones(len(X), dtype=bool)
    for kr in K:
        kv = np.mod(np.array(kr, dtype=np.int64), L.mods)
        Y = L.br(X, kv[None, :])
        mem = np.array([L.member(K, y) for y in Y])
        ok &= mem
    Ix = X[ok]
    # lattice from elements (greedy)
    I = L.zero()
    for v in Ix:
        v = tuple(int(x) for x in v)
        if not L.member(I, v):
            I = L.hnf(list(I) + [v])
    return I, X, ok


def normalizer_check(L, S, K, X, ok):
    """cor (b): exp x normalizes K (conjugation x*k*(-x) for generators k) iff x in I_S(K)."""
    okn = np.ones(len(X), dtype=bool)
    for kr in K:
        kv = np.mod(np.array(kr, dtype=np.int64), L.mods)
        Y = L.bch(L.bch(X, kv[None, :]), L.neg(X))
        okn &= np.array([L.member(K, y) for y in Y])
    return bool((okn == ok).all())


def rtf(L, Hh, lab, mode, rng, st, stop1=True, check_hiding=True, check_norm=True, q_adv=0.3):
    p = L.p
    b = sum(L.e)
    K, S = L.zero(), L.unit_rows()
    calls = 0
    valid = True  # invariant K subset h subset S along the branch
    while True:
        st.bump("rounds")
        assert L.contains(S, K) and L.is_subring(S) and L.is_subring(K)
        # K ideal of S
        assert L.contains(K, L.span_br(S, K)), "K not an ideal of S"
        if stop1 and S == K:
            return K, calls, valid
        dk, us, coord, sigma = present_section(L, S, K)
        # check (M1): t -> sigma(t)+K bijection onto S/K, coordinates consistent
        if L.size(S) // L.size(K) <= 3125:
            Tall = np.array(list(itertools.product(*[range(d) for d in dk])), dtype=np.int64) if dk else np.zeros((1, 0), dtype=np.int64)
            Xs = sigma(Tall)
            for t, x in zip(Tall[:50], Xs[:50]):
                assert coord(x) == [int(v) for v in t], "coord(sigma(t)) != t"
                assert L.member(S, x)
            reps = {tuple(int(v) for v in r) for r in L.reduce_all(K, Xs)}
            assert len(reps) == len(Tall) == L.size(S) // L.size(K), "sigma not a transversal"
        a, T = socle(L, dk, us, coord)
        k = len(dk)
        # Lemma section-rank checks
        cM = L.class_section(S, K)
        dMM = L.dquot(L.add_lat(L.span_br(S, S), K), K)
        st.bump("section_checks")
        Om = FpAlg(p, T) if k else None
        if k:
            assert cM <= L.cls and dMM <= L.R and k <= L.m
            assert Om.derived <= L.R and Om.cls <= min(L.cls, L.R + 1)
        if not stop1 and S == K:
            # a call on the trivial section: count it, oracle returns nothing
            calls += 1
            return K, calls, valid
        # the call
        calls += 1
        Fall = np.array(list(itertools.product(range(p), repeat=k)), dtype=np.int64)
        Tm = Fall * np.array([p ** (ai - 1) for ai in a], dtype=np.int64)[None, :]
        fO = lab[L.idx(sigma(Tm))]
        U0 = [tuple(int(x) for x in Fall[i]) for i in range(len(Fall)) if fO[i] == fO[0]]
        U0set = set(U0)
        U0basis = rref(U0, p)
        hides = None
        if check_hiding and valid:
            # f o sigma o iota hides U0 in (Omega,*): full pair check if small
            assert len(rref(U0, p)) == round(math.log(len(U0), p)) if len(U0) > 1 else True
            if len(Fall) <= 125:
                idxF = {tuple(int(x) for x in r): i for i, r in enumerate(Fall)}
                good = True
                for i in range(len(Fall)):
                    Z = Om.bch(np.mod(-Fall[i], p)[None, :], Fall)
                    inU = np.array([tuple(int(x) for x in z) in U0set for z in Z])
                    same = (fO == fO[i])
                    if not (inU == same).all():
                        good = False
                        break
                hides = good
            else:
                nlab = len(set(fO.tolist()))
                hides = (nlab * len(U0) == len(Fall))
                for ub in U0basis:
                    Z = Om.bch(Fall, np.array(ub)[None, :])
                    iz = [int(sum(int(v) * p ** (k - 1 - j) for j, v in enumerate(z))) for z in Z]
                    hides &= bool((fO[iz] == fO).all())
            assert hides, "f o sigma o iota does not hide U0"
            st.bump("hiding_checked")
            # the paper's claim: U0 = iota^{-1}((h/K) cap M[p])
            claim = []
            for i in range(len(Fall)):
                x = sigma(Tm[i:i + 1])[0]
                if L.member(Hh, tuple(int(v) for v in x)):
                    claim.append(tuple(int(v) for v in Fall[i]))
            assert set(claim) == U0set, "U != iota^{-1}((h/K) cap M[p])"
            st.bump("U_claim_ok")
        # oracle answer
        ans = U0basis
        if mode == "adv" and rng.random() < q_adv and k:
            if rng.random() < 0.5:
                dim = rng.randrange(0, k + 1)
                ans = rref([tuple(rng.randrange(p) for _ in range(k)) for _ in range(dim)], p)
            else:  # random subalgebra (closure of random vectors)
                gens = [tuple(rng.randrange(p) for _ in range(k)) for _ in range(rng.randrange(1, 3))]
                B = rref(gens, p)
                while True:
                    new = [tuple(Om.br(np.array(x), np.array(y))) for x in B for y in B]
                    B2 = rref(list(B) + new, p)
                    if len(B2) == len(B):
                        break
                    B = B2
                ans = B
            if set(map(tuple, ans)) != set(map(tuple, U0basis)) or len(ans) != len(U0basis):
                if rref(list(ans), p) != rref(list(U0basis), p):
                    valid = False
        # stop rule 2
        if not ans or not Om.closed(ans):
            return K, calls, valid
        # step 4: K' = q^{-1}(U), S' = I_S(K')
        lifts = []
        for v in ans:
            t = np.array([v], dtype=np.int64) * np.array([p ** (ai - 1) for ai in a], dtype=np.int64)[None, :]
            lifts.append(tuple(int(x) for x in sigma(t)[0]))
        K2 = L.hnf(list(K) + lifts)
        assert L.size(K2) > L.size(K) and L.contains(S, K2) and L.is_subring(K2)
        S2, X, ok = idealizer(L, S, K2)
        if check_norm and len(X) * len(K2) <= 400000:
            assert normalizer_check(L, S, K2, X, ok), "normalizer != idealizer"
            st.bump("normalizer_checked")
        assert L.contains(S2, K2)
        if valid:
            assert L.contains(K2, []) and L.contains(Hh, K2) and L.contains(S2, Hh), "invariant broken on truth branch"
        K, S = K2, S2


def rings():
    R = []
    R.append(Ring("Z3xZ9", 3, [1, 2], {}))
    R.append(Ring("Z/3^4 cyclic", 3, [4], {}))
    R.append(Ring("(Z9)^2 [x,y]=3y", 3, [2, 2], {(0, 1): [0, 3]}))
    R.append(Ring("Z27xZ3 [x,y]=9x", 3, [3, 1], {(0, 1): [9, 0]}))
    R.append(Ring("Heis Z9,Z9,Z3", 3, [2, 2, 1], {(0, 1): [0, 0, 1]}))
    R.append(Ring("Heis(F3) x Z9", 3, [1, 1, 1, 2], {(0, 1): [0, 0, 1, 0]}))
    R.append(Ring("Heis3(Z9)", 3, [2, 2, 2], {(0, 1): [0, 0, 1]}))
    R.append(Ring("(Z25)^2 [x,y]=5y", 5, [2, 2], {(0, 1): [0, 5]}))
    R.append(Ring("x,y ord5, z ord25, [x,y]=5z", 5, [1, 1, 2], {(0, 1): [0, 0, 5]}))
    R.append(Ring("Z25,Z25,Z5 [x,y]=5y+z", 5, [2, 2, 1], {(0, 1): [0, 5, 1]}))
    R.append(Ring("filiform x25,e1..e3 ord5", 5, [2, 1, 1, 1], {(0, 1): [0, 0, 1, 0], (0, 2): [0, 0, 0, 1]}))
    return R


def main():
    rng = random.Random(1109)
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = []
    for L in rings():
        if which != "all" and which not in L.name:
            continue
        b = sum(L.e)
        subs = all_subrings(L)
        st = Stats()
        worst_truth = 0
        for Hh in subs:
            lab = coset_labels(L, Hh)
            Kout, calls, valid = rtf(L, Hh, lab, "truth", rng, st)
            assert valid and Kout == Hh, ("wrong output", L.name, Hh)
            logH = round(math.log(L.size(Hh), L.p))
            assert calls <= b and calls <= logH + 1, (L.name, calls, b, logH)
            worst_truth = max(worst_truth, calls)
            st.bump("runs")
        # adversarial branches
        adv_max = 0
        nadv = 0
        for Hh in subs[:: max(1, len(subs) // 60)]:
            lab = coset_labels(L, Hh)
            for rep in range(6):
                Kout, calls, valid = rtf(L, Hh, lab, "adv", rng, st, check_hiding=True, check_norm=False, q_adv=0.5)
                assert calls <= b, ("adversarial branch exceeds b", L.name, calls, b)
                adv_max = max(adv_max, calls)
                nadv += 1
        # without stop rule 1, H = G
        G = L.unit_rows()
        lab = coset_labels(L, G)
        _, calls_nostop, _ = rtf(L, G, lab, "truth", rng, st, stop1=False, check_norm=False)
        res = dict(ring=L.name, p=L.p, e=L.e, cls=L.cls, R=L.R, b=b, n_subrings=len(subs),
                   max_calls_truth=worst_truth, adversarial_runs=nadv, max_calls_adv=adv_max,
                   calls_HeqG_without_stop1=calls_nostop, **st.d)
        print(json.dumps(res))
        sys.stdout.flush()
        out.append(res)


if __name__ == "__main__":
    main()
