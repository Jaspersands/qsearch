"""Weight-doubling recursion for average-case binary SIS mod p (zero-sum node at Gamma_0).

Companion of research/audits/reviews/2026-11-05-rees-s3-arity.md, section P.

Problem BinSIS(n, M, p): given i.i.d. uniform v_1, v_2, ... in F_p^n, find a nonempty T with
sum_{i in T} v_i = 0.  The solver below is Las Vegas in the number of columns: it reads fresh
columns from a stream until it succeeds, it never fails, and it is deterministic given the
columns.  Its expected consumption is given EXACTLY by the recursion `expected_consumption`
(Wald's identity; see the report).  Every output is checked exactly.

Levels.  Level 0 has weights {0,1}.  Level j >= 1 has weights D_{2^(j-1)} = {-2^(j-1),...,2^(j-1)}
(as integers, read mod p).  Level jstar = ceil(log2(p-1)) is plain linear algebra, because
D_{2^(jstar-1)} contains a representative of every residue.  A level-j solve in dimension d
(any target) uses, for each coordinate dd = d,...,1, "switches": a homogeneous level-(j+1)
solve on the first dd-1 coordinates of fresh columns gives alpha with entries in D_{2^j};
split alpha = x - x' with x = ceil(alpha/2), x' = -floor(alpha/2), both in the level-j set.
The two choices differ by beta * e_dd, where beta = <alpha, coordinate dd> is uniform.
Switches are drawn until the subset sums of their betas cover F_p.  Then the residual target
moves one coordinate down.  The base (dimension 0) is one fresh column with weight 1.

Pure integers in every decision (numpy int64 arithmetic mod p).
"""

from fractions import Fraction
from functools import lru_cache
import math
import numpy as np


class Exhausted(Exception):
    """Raised when a budgeted stream runs out (used by the fixed-arity node)."""


class Stream:
    """Fresh i.i.d. uniform columns in F_p^n, drawn on demand; counts consumption."""

    def __init__(self, p, n, rng, cap=None, source=None):
        self.p, self.n, self.rng, self.cap = p, n, rng, cap
        self.source = source            # optional pre-drawn array (rows = columns)
        if source is not None:
            self.buf = source
        else:
            self.buf = np.empty((1 << 12, max(n, 1)), dtype=np.int16)
        self.count = 0

    def draw(self, k):
        if self.cap is not None and self.count + k > self.cap:
            raise Exhausted
        if self.source is not None:
            if self.count + k > len(self.source):
                raise Exhausted
        else:
            while self.count + k > len(self.buf):
                nb = np.empty((2 * len(self.buf), self.buf.shape[1]), dtype=np.int16)
                nb[: len(self.buf)] = self.buf
                self.buf = nb
            self.buf[self.count:self.count + k] = self.rng.integers(0, self.p, (k, self.buf.shape[1]))
        idx = np.arange(self.count, self.count + k)
        self.count += k
        return idx


def kernel_vec(M, p):
    """Nonzero x with M x = 0 mod p, for a d x k matrix with k > d (always exists)."""
    M = (M.astype(np.int64)) % p
    d, k = M.shape
    if d == 0:
        x = np.zeros(k, dtype=np.int64)
        x[0] = 1
        return x
    piv = []
    r = 0
    for c in range(k):
        if r == d:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        i = r + int(nz[0])
        if i != r:
            M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        col = M[:, c].copy()
        col[r] = 0
        M = (M - np.outer(col, M[r])) % p
        piv.append(c)
        r += 1
    pivset = set(piv)
    free = next(c for c in range(k) if c not in pivset)
    x = np.zeros(k, dtype=np.int64)
    x[free] = 1
    for row, pc in enumerate(piv):
        x[pc] = (-M[row, free]) % p
    return x


def jstar_of(p):
    """Least j with 2^j >= p-1, i.e. ceil(log2(p-1)); level jstar is linear algebra."""
    j = 0
    while (1 << j) < p - 1:
        j += 1
    return j


def bound_of_level(j):
    """Largest |weight| at level j >= 1 (level 0 is {0,1})."""
    return 1 << (j - 1)


def solve(level, d, target, st, p, jstar, stats=None):
    """Return (idx, w): fresh column indices and integer weights (nonzero), with
    sum w_i v_i[:d] = target mod p, w in the level's weight set, and w not all zero."""
    if level == jstar:
        assert not np.any(np.asarray(target) % p)
        idx = st.draw(d + 1)
        if d == 0:
            return idx[:1], np.array([1], dtype=np.int64)
        A = st.buf[idx, :d].astype(np.int64)
        x = kernel_vec(A.T, p)
        x = np.where(x > p // 2, x - p, x)
        keep = x != 0
        return idx[keep], x[keep]
    t = np.asarray(target, dtype=np.int64) % p
    stages = []
    for dd in range(d, 0, -1):
        switches = []
        reach = {0: ()}
        while len(reach) < p:
            aidx, aw = solve(level + 1, dd - 1, np.zeros(dd - 1, dtype=np.int64), st, p, jstar, stats)
            beta = int((aw @ st.buf[aidx, dd - 1].astype(np.int64)) % p)
            x = (aw + 1) // 2
            xp = -(aw // 2)
            k = len(switches)
            switches.append((aidx, x, xp))
            if stats is not None:
                stats["switches"] += 1
            new = {}
            for r, T in reach.items():
                v = (r + beta) % p
                if v not in reach and v not in new:
                    new[v] = T + (k,)
            reach.update(new)
        c = np.zeros(dd, dtype=np.int64)
        for (aidx, x, xp) in switches:
            c += xp @ st.buf[aidx, :dd].astype(np.int64)
        c %= p
        stages.append((dd, t.copy(), c, switches, reach))
        t = (t - c)[: dd - 1] % p
    z = st.draw(1)
    widx = [z]
    ww = [np.array([1], dtype=np.int64)]
    for (dd, tdd, c, switches, reach) in reversed(stages):
        I = np.concatenate(widx)
        W = np.concatenate(ww)
        s = (W @ st.buf[I, :dd].astype(np.int64)) % p
        resid = (tdd - c - s) % p
        assert not np.any(resid[: dd - 1]), "residual check failed"
        T = set(reach[int(resid[dd - 1])])
        for k, (aidx, x, xp) in enumerate(switches):
            src = x if k in T else xp
            keep = src != 0
            widx.append(aidx[keep])
            ww.append(src[keep])
    I = np.concatenate(widx)
    W = np.concatenate(ww)
    return I, W


def check_solution(st, I, W, d, target, p, level):
    """Exact check: distinct indices, weights in the level set, nonzero, correct sum."""
    if len(I) == 0 or len(set(I.tolist())) != len(I):
        return False
    if level == 0:
        if not np.all(W == 1):
            return False
    else:
        b = bound_of_level(level)
        if np.any(np.abs(W) > b) or np.any(W == 0):
            return False
    s = (W @ st.buf[I, :d].astype(np.int64)) % p
    return bool(np.all(s == (np.asarray(target) % p)))


def binsis(p, n, rng, cap=None, source=None, stats=None):
    """Las Vegas zero-sum finder; returns (T, consumed) or raises Exhausted."""
    js = jstar_of(p)
    st = Stream(p, n, rng, cap=cap, source=source)
    I, W = solve(0, n, np.zeros(n, dtype=np.int64), st, p, js, stats)
    assert check_solution(st, I, W, n, np.zeros(n, dtype=np.int64), p, 0)
    return I, st.count, st


# ------------------------------------------------------------------ exact expectations

def covering_time(p):
    """Exact E[S], S = number of i.i.d. uniform beta in F_p until the subset sums cover F_p."""
    full = (1 << p) - 1

    @lru_cache(maxsize=None)
    def E(mask):
        if mask == full:
            return Fraction(0)
        tot = Fraction(1)
        for b in range(1, p):
            sh = ((mask << b) | (mask >> (p - b))) & full   # R + b
            tot += Fraction(1, p) * E(mask | sh)
        return tot / (1 - Fraction(1, p))

    return E(1)


def expected_consumption(p, n, sp=None):
    """Exact expected number of columns read by binsis(p, n): N_0(n), where
    N_jstar(d) = d+1 and N_j(d) = 1 + s_p * sum_{dd=1}^{d} N_{j+1}(dd-1)."""
    js = jstar_of(p)
    if sp is None:
        sp = covering_time(p)
    N = [Fraction(d + 1) for d in range(n + 1)]
    for _ in range(js):
        pref = [Fraction(0)]
        for d in range(n + 1):
            pref.append(pref[-1] + N[d])
        N = [1 + sp * pref[d] for d in range(n + 1)]   # pref[d] = sum_{e=0}^{d-1} N_{j+1}(e)
    return N[n]


def closed_form_bound(p, n, sp):
    """(s_p+1)^jstar * C(n+jstar+1, jstar+1), the bound proved in the report."""
    js = jstar_of(p)
    return (sp + 1) ** js * math.comb(n + js + 1, js + 1)
