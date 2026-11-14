"""Finite-field class utilities (independent recompute, 2026-11-13). Written from the
definitions in core/main-core.tex sec:halving and fragment.tex only."""
import numpy as np
from functools import lru_cache
from math import gcd

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0].tolist()

def factor(n):
    f, d = [], 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: f.append(n)
    return f

def least_primitive_root(p):
    if p == 2: return 1
    fs = factor(p - 1)
    g = 2
    while True:
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs): return g
        g += 1

class Field:
    """F_p with xi = least primitive root; cl_D(x) = log_xi(x) mod D."""
    def __init__(self, p):
        self.p = p
        self.g = least_primitive_root(p)
        # powers g^i, i = 0..p-2, vectorised in blocks
        n = p - 1
        B = int(np.ceil(np.sqrt(n))) + 1
        small = np.empty(B, dtype=np.int64); small[0] = 1
        for i in range(1, B): small[i] = small[i - 1] * self.g % p
        gB = pow(self.g, B, p)
        big = np.empty(B, dtype=np.int64); big[0] = 1
        for i in range(1, B): big[i] = big[i - 1] * gB % p
        pw = (big[:, None] * small[None, :] % p).reshape(-1)[:n]
        self.pw = pw                       # pw[i] = g^i
        lg = np.full(p, -1, dtype=np.int64)
        lg[pw] = np.arange(n, dtype=np.int64)
        assert (lg[1:] >= 0).all()
        self.lg = lg                       # lg[x] = log_g x, lg[0] = -1
        self._S0 = {}

    def cl(self, x, D):
        x %= self.p
        assert x != 0
        return int(self.lg[x]) % D

    def S0(self, D):
        """S0[k] = (frozenset of D-classes of 1+y, y in Q_k, 1+y != 0; zero flag)."""
        if D in self._S0: return self._S0[D]
        p = self.p
        y = np.arange(1, p, dtype=np.int64)
        cy = self.lg[y] % D
        z = (1 + y) % p
        nz = z != 0
        cz = self.lg[z[nz]] % D
        pairs = np.unique(cy[nz] * D + cz)
        res = [[set(), False] for _ in range(D)]
        for v in pairs.tolist(): res[v // D][0].add(v % D)
        cm1 = int(self.lg[p - 1]) % D       # -1 = 1 + y with y = -2? no: 1+y = 0 iff y = -1
        res[cm1][1] = True
        out = tuple((frozenset(a), b) for a, b in res)
        self._S0[D] = out
        return out

class CSet:
    """A P_D-stable subset of F_p: set of D-classes plus zero flag."""
    __slots__ = ("cls", "zero")
    def __init__(self, cls, zero=False):
        self.cls = frozenset(cls); self.zero = bool(zero)
    def key(self): return (self.cls, self.zero)
    def __eq__(self, o): return self.key() == o.key()
    def __hash__(self): return hash(self.key())
    def __repr__(self): return f"CSet({sorted(self.cls)},{self.zero})"

def cs_union(*xs):
    c, z = set(), False
    for x in xs: c |= x.cls; z |= x.zero
    return CSet(c, z)

def cs_shift(A, e, D):
    return CSet({(a + e) % D for a in A.cls}, A.zero)

def cs_add(A, B, S0, D):
    """{a + b : a in A, b in B} as a class set."""
    c, z = set(), False
    for a in A.cls:
        for b in B.cls:
            s, zf = S0[(b - a) % D]
            c |= {(a + x) % D for x in s}; z |= zf
    if A.zero: c |= B.cls; z |= B.zero
    if B.zero: c |= A.cls
    return CSet(c, z)

def t_pk(F, k):
    """least t with a nonzero zero sum of t k-th powers (exact, by class sumsets)."""
    S0 = F.S0(k)
    Pset = CSet({0})
    Sig = Pset; t = 1
    while not Sig.zero:
        Sig = cs_add(Sig, Pset, S0, k); t += 1
        assert t <= k + 1
    return t

def T_sets(F, kappa, m, smax):
    """T_0..T_smax for the type recursion with eps = -xi^{-m}."""
    p = F.p; D = kappa
    S0 = F.S0(D)
    e = ((p - 1) // 2 - m) % D           # cl(eps) = cl(-1) - m
    T = [CSet({0})]
    for j in range(1, smax + 1):
        A = T[-1]; eA = cs_shift(A, e, D)
        T.append(cs_union(A, eA, cs_add(A, eA, S0, D)))
    return T
