"""Small exact Lie-algebra / Lazard-group toolkit over F_p (referee scratch)."""
import itertools, numpy as np

def tensor(m, br, p):
    C = np.zeros((m, m, m), dtype=np.int64)
    for (i, j), d in br.items():
        for k, c in d.items():
            C[i, j, k] = (C[i, j, k] + c) % p; C[j, i, k] = (C[j, i, k] - c) % p
    return C

def br(x, y, C, p):
    return np.einsum('i,j,ijk->k', x, y, C) % p

def jacobi_ok(C, p):
    m = C.shape[0]; E = np.eye(m, dtype=np.int64)
    for i, j, k in itertools.combinations(range(m), 3):
        a, b, c = E[i], E[j], E[k]
        s = (br(a, br(b, c, C, p), C, p) + br(b, br(c, a, C, p), C, p) + br(c, br(a, b, C, p), C, p)) % p
        if s.any(): return False
    return True

def rref(M, p):
    M = [list(map(int, r)) for r in M]; r = 0; piv = []
    rows = len(M); cols = len(M[0]) if rows else 0
    for c in range(cols):
        q = next((i for i in range(r, rows) if M[i][c] % p), None)
        if q is None: continue
        M[r], M[q] = M[q], M[r]; iv = pow(M[r][c], -1, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    return [row for row in M[:r]], piv

def rank(M, p):
    if len(M) == 0: return 0
    return len(rref(M, p)[0])

def span_contains(B, v, p):
    return rank(list(B) + [list(v)], p) == rank(B, p) if len(B) else not np.any(np.array(v) % p)

def subspaces(m, k, p):
    """all k-dim subspaces of F_p^m as RREF bases"""
    for pivs in itertools.combinations(range(m), k):
        free = [(r, c) for r in range(k) for c in range(m) if c > pivs[r] and c not in pivs]
        for vals in itertools.product(range(p), repeat=len(free)):
            B = np.zeros((k, m), dtype=np.int64)
            for r in range(k): B[r, pivs[r]] = 1
            for (r, c), v in zip(free, vals): B[r, c] = v
            yield B

def derived(C, p):
    m = C.shape[0]; E = np.eye(m, dtype=np.int64)
    vs = [br(E[i], E[j], C, p) for i in range(m) for j in range(m)]
    R, _ = rref(vs, p); return np.array(R, dtype=np.int64).reshape(-1, m)

def lcs(C, p):
    m = C.shape[0]; E = np.eye(m, dtype=np.int64); cur = E; out = [E]
    while True:
        vs = [br(x, E[j], C, p) for x in cur for j in range(m)]
        R, _ = rref(vs, p); R = np.array(R, dtype=np.int64).reshape(-1, m)
        out.append(R); 
        if len(R) == 0: return out
        cur = R

def center(C, p):
    m = C.shape[0]
    # z with [z, e_j] = 0 all j : linear system sum_i z_i C[i,j,k] = 0
    A = C.reshape(m, m * m).T % p   # rows (j,k), cols i
    return nullspace(A, p)

def nullspace(A, p):
    A = np.array(A, dtype=np.int64) % p
    rows, cols = A.shape
    R, piv = rref(A, p)
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = [0] * cols; v[f] = 1
        for r, c in enumerate(piv): v[c] = (-R[r][f]) % p
        basis.append(v)
    return np.array(basis, dtype=np.int64).reshape(-1, cols)

def is_ideal(B, C, p):
    m = C.shape[0]; E = np.eye(m, dtype=np.int64)
    return all(span_contains(B, br(b, E[j], C, p), p) for b in B for j in range(m))

def is_abelian_sub(B, C, p):
    return all(not br(a, b, C, p).any() for a in B for b in B)

def is_central(B, C, p):
    m = C.shape[0]; E = np.eye(m, dtype=np.int64)
    return all(not br(b, E[j], C, p).any() for b in B for j in range(m))

def bch(X, Y, C, p, cls):
    inv2 = pow(2, -1, p); inv12 = pow(12, -1, p); inv24 = pow(24, -1, p)
    XY = br(X, Y, C, p)
    Z = (X + Y + inv2 * XY) % p
    if cls >= 3:
        Z = (Z + inv12 * (br(X, XY, C, p) - br(Y, XY, C, p))) % p
    if cls >= 4:
        Z = (Z - inv24 * br(Y, br(X, XY, C, p), C, p)) % p
    assert cls <= 4
    return Z

def lines(m, p):
    out = []
    for v in itertools.product(range(p), repeat=m):
        v = np.array(v, dtype=np.int64); nz = np.nonzero(v)[0]
        if len(nz) and v[nz[0]] == 1: out.append(v)
    return np.array(out)

ALGS = {
  'heis3':   (3, {(0, 1): {2: 1}}),
  'fil4':    (4, {(0, 1): {2: 1}, (0, 2): {3: 1}}),
  'free23':  (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}),
  'fil5':    (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (1, 2): {4: 1}}),   # class 4, [x2,x3]=x5
  'fil4+1':  (5, {(0, 1): {2: 1}, (0, 2): {3: 1}}),                                    # fil4 (+) F_p e5 central
  # non-graded-basis variant of fil4 (same algebra, perturbed basis) -- tests basis independence
}
