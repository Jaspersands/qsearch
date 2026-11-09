"""Exact linear algebra and nilpotent Lie algebras over F_p (helper for the
2026-11-03 Appendix E check). Imports nothing from the repository.

A Lie algebra of dimension n is a numpy int64 array C of shape (n, n, n) with
[e_i, e_j] = sum_l C[i, j, l] e_l (mod p). Vectors are int64 arrays mod p.
Subspaces are stored as reduced row echelon bases (rows).
"""
import itertools
import numpy as np


# ---------------------------------------------------------------- linear algebra
def rref(rows, p):
    """Reduced row echelon form of a list/array of row vectors mod p.
    Returns (R, pivots) with R the nonzero rows."""
    A = np.array(rows, dtype=np.int64).reshape(-1, len(rows[0]) if len(rows) else 0) % p \
        if len(rows) else np.zeros((0, 0), dtype=np.int64)
    if A.size == 0:
        return A.reshape(0, A.shape[1] if A.ndim == 2 else 0), []
    A = A.copy()
    nr, nc = A.shape
    piv = []
    r = 0
    for c in range(nc):
        if r == nr:
            break
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        i = r + nz[0]
        if i != r:
            A[[r, i]] = A[[i, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        for i2 in range(nr):
            if i2 != r and A[i2, c]:
                A[i2] = (A[i2] - A[i2, c] * A[r]) % p
        piv.append(c)
        r += 1
    return A[:r], piv


def span(rows, n, p):
    if len(rows) == 0:
        return np.zeros((0, n), dtype=np.int64)
    R, _ = rref(np.array(rows, dtype=np.int64).reshape(-1, n), p)
    return R


def dim(S):
    return S.shape[0]


def in_span(v, S, p):
    if S.shape[0] == 0:
        return not np.any(np.asarray(v) % p)
    return dim(span(np.vstack([S, np.asarray(v).reshape(1, -1)]), S.shape[1], p)) == dim(S)


def contains(S, T, p):
    """T subset S (both row bases)."""
    return all(in_span(t, S, p) for t in T)


def equal(S, T, p):
    return dim(S) == dim(T) and contains(S, T, p)


def nullspace(A, n, p):
    """Basis (rows) of {y in F_p^n : A y = 0}; A has n columns."""
    A = np.array(A, dtype=np.int64).reshape(-1, n) % p
    if A.shape[0] == 0:
        return np.eye(n, dtype=np.int64)
    R, piv = rref(A, p)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(n, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-R[i, f]) % p
        basis.append(v)
    if not basis:
        return np.zeros((0, n), dtype=np.int64)
    return span(basis, n, p)


def annihilator(S, n, p):
    """Rows theta with theta . s = 0 for all s in S."""
    return nullspace(S, n, p) if dim(S) else np.eye(n, dtype=np.int64)


def intersect(S, T, n, p):
    # x in S cap T iff theta.x = 0 for theta in ann(S) and ann(T)
    A = np.vstack([annihilator(S, n, p), annihilator(T, n, p)])
    return nullspace(A, n, p)


def complement_basis(S, n, p, rng=None):
    """Rows completing S to a basis of F_p^n (randomized if rng given)."""
    out = []
    cur = S.copy()
    cand = list(np.eye(n, dtype=np.int64))
    if rng is not None:
        rng.shuffle(cand)
        cand = [(c + rng.integers(0, p) * (cur[rng.integers(0, dim(cur))] if dim(cur) else 0)) % p
                for c in cand]
    for c in cand:
        if not in_span(c, cur, p):
            out.append(np.asarray(c) % p)
            cur = span(np.vstack([cur, np.asarray(c).reshape(1, -1)]), n, p)
    return np.array(out, dtype=np.int64).reshape(-1, n)


def solve_coords(B, v, p):
    """Coordinates a with a @ B = v, B rows linearly independent (raises if none)."""
    k, n = B.shape
    # solve B^T a = v
    M = np.hstack([B.T % p, np.asarray(v).reshape(-1, 1) % p])
    R, piv = rref(M, p)
    if k in piv:
        raise ValueError("not in span")
    a = np.zeros(k, dtype=np.int64)
    for i, c in enumerate(piv):
        a[c] = R[i, k]
    return a % p


# ---------------------------------------------------------------- Lie algebras
def br(C, x, y, p):
    return np.einsum('i,j,ijl->l', np.asarray(x), np.asarray(y), C) % p


def br_basis(C, i, j):
    return C[i, j]


def check_lie(C, p):
    n = C.shape[0]
    if np.any((C + C.transpose(1, 0, 2)) % p):
        return False
    for i, j, k in itertools.combinations(range(n), 3):
        e = np.eye(n, dtype=np.int64)
        s = (br(C, e[i], br(C, e[j], e[k], p), p) + br(C, e[j], br(C, e[k], e[i], p), p)
             + br(C, e[k], br(C, e[i], e[j], p), p)) % p
        if np.any(s):
            return False
    return True


def bracket_space(C, S, T, p):
    n = C.shape[0]
    rows = [br(C, s, t, p) for s in S for t in T]
    return span(rows, n, p) if rows else np.zeros((0, n), dtype=np.int64)


def lower_central(C, p):
    """[gamma_1, gamma_2, ...] until zero (zero space not included). Returns None
    if the series stabilises at a nonzero space (not nilpotent)."""
    n = C.shape[0]
    g = np.eye(n, dtype=np.int64)
    series = []
    cur = g
    while dim(cur) > 0:
        series.append(cur)
        nxt = bracket_space(C, g, cur, p)
        if dim(nxt) == dim(cur):
            return None
        cur = nxt
    return series


def nil_class(C, p):
    s = lower_central(C, p)
    return None if s is None else len(s)  # class = number of nonzero gamma_i


def is_subalgebra(C, S, p):
    return all(in_span(br(C, a, b, p), S, p) for a in S for b in S) if dim(S) else True


def subalgebra_generated(C, gens, p):
    n = C.shape[0]
    S = span(gens, n, p)
    while True:
        new = bracket_space(C, S, S, p)
        T = span(np.vstack([S, new]), n, p) if dim(new) else S
        if dim(T) == dim(S):
            return S
        S = T


def centralizer(C, S, p):
    n = C.shape[0]
    if dim(S) == 0:
        return np.eye(n, dtype=np.int64)
    # [y, s] = 0: y_i C[i,:,:] s
    rows = []
    for s in S:
        M = np.einsum('ijl,j->li', C, s) % p  # row l: coefficient of y_i in [y,s]_l
        rows.extend(M)
    return nullspace(rows, n, p)


def normalizer(C, K, p):
    """{y : [y, K] subset K}."""
    n = C.shape[0]
    ann = annihilator(K, n, p)
    rows = []
    for v in K:
        M = np.einsum('ijl,j->li', C, v) % p   # [y,v] = M y
        for th in ann:
            rows.append(th @ M % p)
    return nullspace(rows, n, p) if rows else np.eye(n, dtype=np.int64)


def is_ideal(C, S, p):
    n = C.shape[0]
    e = np.eye(n, dtype=np.int64)
    return all(in_span(br(C, e[i], s, p), S, p) for i in range(n) for s in S)


def is_abelian_space(C, S, p):
    return all(not np.any(br(C, a, b, p)) for a in S for b in S)


# ---------------------------------------------------------------- Lemma E.ideal
def construct_ideal(C, p, rng):
    """Lemma lem:app-codim-ideal with random admissible choices.
    Returns the flag basis x_1..x_b (rows) in order."""
    n = C.shape[0]
    xs = []
    I = np.zeros((0, n), dtype=np.int64)
    while True:
        rows = []
        for x in xs:                       # [y, x] = 0
            rows.extend(np.einsum('ijl,j->li', C, x) % p)
        ann = annihilator(I, n, p)         # theta.[u_e, y] = 0
        for e in range(n):
            M = C[e].T % p                 # [u_e, y]_l = sum_j C[e,j,l] y_j
            for th in ann:
                rows.append(th @ M % p)
        V = nullspace(rows, n, p) if rows else np.eye(n, dtype=np.int64)
        if dim(V) == dim(I):
            return np.array(xs, dtype=np.int64).reshape(-1, n)
        while True:
            y = (rng.integers(0, p, dim(V)) @ V) % p
            if not in_span(y, I, p):
                break
        xs.append(y)
        I = span(np.vstack([I, y.reshape(1, -1)]), n, p)


# ---------------------------------------------------------------- quotients
def quotient(C, S, K, p, rng=None):
    """s/k for a subalgebra S with ideal K subset S.
    Returns (Cq, sec, proj) with sec: q-coords -> ambient vector (linear section,
    rows are the complement basis), proj(v) for v in S -> q-coords."""
    n = C.shape[0]
    # basis of S adapted to K: K rows then complement rows inside S
    comp = []
    cur = K.copy()
    cand = list(S)
    if rng is not None:
        idx = rng.permutation(len(cand))
        cand = [cand[i] for i in idx]
        if dim(K):
            cand = [(c + (rng.integers(0, p, dim(K)) @ K)) % p for c in cand]
    for c in cand:
        if not in_span(c, cur, p):
            comp.append(c % p)
            cur = span(np.vstack([cur, c.reshape(1, -1)]), n, p)
    comp = np.array(comp, dtype=np.int64).reshape(-1, n)
    full = np.vstack([comp, K]) if dim(K) else comp
    q = dim(comp)

    def proj(v):
        a = solve_coords(full, v, p)
        return a[:q] % p

    Cq = np.zeros((q, q, q), dtype=np.int64)
    for i in range(q):
        for j in range(q):
            Cq[i, j] = proj(br(C, comp[i], comp[j], p))
    return Cq, comp, proj


# ---------------------------------------------------------------- generators
def central_extension_step(C, p, rng, push_class=True):
    """Random one-dimensional central extension g + F z by a random 2-cocycle.
    If push_class, prefer cocycles nonzero on gamma_c x g (raises the class)."""
    n = C.shape[0]
    pairs = list(itertools.combinations(range(n), 2))
    idx = {pr: t for t, pr in enumerate(pairs)}
    npair = len(pairs)

    def omega_row(u, v):
        # linear functional (in omega variables) of omega(u, v) for vectors u, v
        r = np.zeros(npair, dtype=np.int64)
        for i in range(n):
            if not u[i]:
                continue
            for j in range(n):
                if not v[j] or i == j:
                    continue
                if i < j:
                    r[idx[(i, j)]] += u[i] * v[j]
                else:
                    r[idx[(j, i)]] -= u[i] * v[j]
        return r % p

    e = np.eye(n, dtype=np.int64)
    rows = []
    for i, j, k in itertools.combinations(range(n), 3):
        r = (omega_row(br(C, e[i], e[j], p), e[k]) + omega_row(br(C, e[j], e[k], p), e[i])
             + omega_row(br(C, e[k], e[i], p), e[j])) % p
        if np.any(r):
            rows.append(r)
    Z2 = nullspace(rows, npair, p) if rows else np.eye(npair, dtype=np.int64)
    if dim(Z2) == 0:
        return None
    om = None
    if push_class:
        series = lower_central(C, p)
        top = series[-1]
        # cocycles nonzero on top x g
        for _ in range(20):
            w = (rng.integers(0, p, dim(Z2)) @ Z2) % p
            if any(np.any(omega_row(t, e[j]) @ w % p) for t in top for j in range(n)):
                om = w
                break
    if om is None:
        om = (rng.integers(0, p, dim(Z2)) @ Z2) % p
        if not np.any(om):
            return None
    C2 = np.zeros((n + 1, n + 1, n + 1), dtype=np.int64)
    C2[:n, :n, :n] = C
    for (i, j), t in idx.items():
        C2[i, j, n] = om[t]
        C2[j, i, n] = (-om[t]) % p
    return C2


def random_nilpotent(n, p, rng, push=0.5):
    """Iterated central extensions starting from a random abelian algebra of dim 2 or 3."""
    a0 = int(rng.integers(2, 4))
    C = np.zeros((a0, a0, a0), dtype=np.int64)
    while C.shape[0] < n:
        C2 = central_extension_step(C, p, rng, push_class=rng.random() < push)
        if C2 is None:
            # abelian extension (add a free direction)
            m = C.shape[0]
            C2 = np.zeros((m + 1, m + 1, m + 1), dtype=np.int64)
            C2[:m, :m, :m] = C
        C = C2
    # random change of basis
    P = random_invertible(n, p, rng)
    return change_basis(C, P, p)


def random_invertible(n, p, rng):
    while True:
        P = rng.integers(0, p, (n, n))
        if dim(span(P, n, p)) == n:
            return P.astype(np.int64)


def mat_inv(P, p):
    n = P.shape[0]
    R, _ = rref(np.hstack([P % p, np.eye(n, dtype=np.int64)]), p)
    return R[:, n:] % p


def change_basis(C, P, p):
    """New basis f_i = sum_k P[i,k] e_k."""
    n = C.shape[0]
    Pinv = mat_inv(P, p)
    Cn = np.einsum('ia,jb,abl->ijl', P, P, C) % p      # [f_i,f_j] in e-coords
    Cn = np.einsum('ijl,lm->ijm', Cn, Pinv) % p         # to f-coords
    return Cn


def strictly_upper(N, p):
    """n_N with basis E_{ij}, i<j."""
    idx = [(i, j) for i in range(N) for j in range(i + 1, N)]
    pos = {e: t for t, e in enumerate(idx)}
    n = len(idx)
    C = np.zeros((n, n, n), dtype=np.int64)
    for a, (i, j) in enumerate(idx):
        for b, (k, l) in enumerate(idx):
            if j == k:
                C[a, b, pos[(i, l)]] += 1
            if l == i:
                C[a, b, pos[(k, j)]] -= 1
    return C % p, idx


def sub_of_nN(N, p, rng, ngen):
    """Subalgebra of n_N generated by ngen random elements, as an abstract algebra."""
    C, _ = strictly_upper(N, p)
    n = C.shape[0]
    gens = [rng.integers(0, p, n) * (rng.random(n) < 0.4) for _ in range(ngen)]
    S = subalgebra_generated(C, gens, p)
    Cs, sec, _ = quotient(C, S, np.zeros((0, n), dtype=np.int64), p)
    return Cs


def filiform(m, p):
    """Basis x, e_1..e_{m-1}; [x,e_i] = e_{i+1}."""
    C = np.zeros((m, m, m), dtype=np.int64)
    for i in range(1, m - 1):
        C[0, i, i + 1] = 1
        C[i, 0, i + 1] = p - 1
    return C


def from_brackets(n, table, p):
    """table: {(i,j): {l: coeff}} with 0-based indices, i<j."""
    C = np.zeros((n, n, n), dtype=np.int64)
    for (i, j), d in table.items():
        for l, c in d.items():
            C[i, j, l] = c % p
            C[j, i, l] = (-c) % p
    return C
