"""Small exact Lie-algebra / Rees-cover utilities over F_p (class <= 3).

Elements of the truncated Rees cover A^{(d)} are dicts {grade k: int array of
shape (N, m)} (vectorised over a leading axis N); grade k lives in gamma_k(L)
written in an adapted basis of L.  Group law: truncated BCH (class <= 3).
"""
import numpy as np

def algebra(name):
    """Return (m, C, gamma_idx) with C[i,j,:] = [e_i, e_j]."""
    if name == "heis":          # x, y, z ; [x,y] = z
        m = 3; C = np.zeros((m, m, m), dtype=np.int64)
        C[0, 1, 2] = 1; C[1, 0, 2] = -1
        gam = {1: [0, 1, 2], 2: [2]}
    elif name == "free3":       # x,y,z,u,w ; [x,y]=z,[x,z]=u,[y,z]=w
        m = 5; C = np.zeros((m, m, m), dtype=np.int64)
        for (i, j, k) in [(0, 1, 2), (0, 2, 3), (1, 2, 4)]:
            C[i, j, k] = 1; C[j, i, k] = -1
        gam = {1: [0, 1, 2, 3, 4], 2: [2, 3, 4], 3: [3, 4]}
    elif name == "fili4":       # e1..e4 ; [e1,e2]=e3, [e1,e3]=e4 (class 3)
        m = 4; C = np.zeros((m, m, m), dtype=np.int64)
        for (i, j, k) in [(0, 1, 2), (0, 2, 3)]:
            C[i, j, k] = 1; C[j, i, k] = -1
        gam = {1: [0, 1, 2, 3], 2: [2, 3], 3: [3]}
    else:
        raise ValueError(name)
    return m, C, gam

class Cover:
    """Truncated Rees cover A^{(d)} = sum_{k<=d} t^k gamma_k(L) over F_p."""
    def __init__(self, name, p, d):
        self.m, self.C, self.gam = algebra(name)
        self.p, self.d = p, d
        self.inv2 = pow(2, -1, p)
        self.inv12 = pow(12, -1, p) if p > 3 else None

    def br(self, X, Y):
        p, d = self.p, self.d
        out = {}
        for i, a in X.items():
            for j, b in Y.items():
                k = i + j
                if k > d:
                    continue
                v = np.einsum('ni,nj,ijk->nk', a, b, self.C) % p
                out[k] = (out.get(k, 0) + v) % p
        return out

    def add(self, *Xs, coef=None):
        p = self.p; out = {}
        coef = coef or [1] * len(Xs)
        for c, X in zip(coef, Xs):
            for k, v in X.items():
                out[k] = (out.get(k, 0) + c * v) % p
        return out

    def mul(self, X, Y):
        """BCH truncated at class d (d <= 3)."""
        XY = self.br(X, Y)
        terms = [X, Y, XY]; coef = [1, 1, self.inv2]
        if self.d >= 3:
            assert self.inv12 is not None
            terms += [self.br(X, XY), self.br(Y, XY)]
            coef += [self.inv12, (-self.inv12) % self.p]
        return self.add(*terms, coef=coef)

    def inv(self, X):
        return {k: (-v) % self.p for k, v in X.items()}

    def dil(self, s, X):
        """delta_s; s may be an int or an int array of shape (N,)."""
        s = np.asarray(s, dtype=np.int64)
        out = {}
        for k, v in X.items():
            f = np.asarray(pow_vec(s, k, self.p))
            out[k] = (v * (f[..., None] if f.ndim else f)) % self.p
        return out

def pow_vec(s, k, p):
    s = np.asarray(s, dtype=np.int64)
    r = np.ones_like(s)
    for _ in range(k):
        r = (r * s) % p
    return r

def in_span(vecs, basis, p):
    """vecs (N,m); basis (b,m) rows; True where vec in rowspan(basis) mod p."""
    if len(basis) == 0:
        return np.all(vecs % p == 0, axis=1)
    B = np.array(basis, dtype=np.int64) % p
    r0 = rank_mod(B, p)
    out = np.empty(len(vecs), dtype=bool)
    for n, v in enumerate(vecs):
        out[n] = rank_mod(np.vstack([B, v[None]]), p) == r0
    return out

def rank_mod(M, p):
    M = np.array(M, dtype=np.int64) % p
    r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c] % p:
                piv = i; break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
        if r == rows:
            break
    return r
