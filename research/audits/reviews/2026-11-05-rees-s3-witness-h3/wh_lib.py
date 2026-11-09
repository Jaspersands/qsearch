"""Witness sampler at free-coordinate grades with digit set D_0 = mu_h u {0} (h = (p-1)/kappa).

Companion of research/audits/reviews/2026-11-05-rees-s3-witness-h3.md.

Problem W(h; n, M, p): given i.i.d. uniform columns v_1, v_2, ... of F_p^n, find y != 0 with
y_i in D_0 = mu_h u {0} and sum_i y_i v_i = 0.  (At an FCS grade, D_0 = P_kappa u {0}.)

Digit chain.  D_0 = mu_h u {0};  D_{j+1} = D_j - D_j (subsets of F_p).  J(h,p) = least J with
D_J = F_p.  Level J is linear algebra (any kernel vector).  A level-j solve (j < J) in
dimension d uses switches: a level-(j+1) homogeneous solve on the first d-1 coordinates gives
alpha (entries in D_{j+1}); a fixed table splits alpha_i = x_i - x'_i with x_i, x'_i in D_j.
The two choices on the block differ by beta * e_d, beta = <alpha, coordinate d> (uniform).
Switches are drawn until the subset sums of their betas cover F_p.  Then recurse on d-1.

Variant `scaled` (J = 1, any size of p): every level-1 relation may be scaled by any c in F_p^*,
so the k-th switch is scaled to beta = 2^k; ceil(log2 p) switches per coordinate, binary
expansion for the backward choice; entries are split into D_0 - D_0 by a randomized search
(valid when D_0 - D_0 = F_p, guaranteed for sqrt(p) > (kappa-1)(kappa-2)+3).

Everything is exact integer arithmetic; every output is checked exactly by the callers.
"""

from fractions import Fraction
from functools import lru_cache
import math
import random
import numpy as np


class Exhausted(Exception):
    pass


# ------------------------------------------------------------------ digit chains

def mu(h, p):
    """The h-th roots of unity in F_p (requires h | p-1)."""
    assert (p - 1) % h == 0
    return sorted({x for x in range(1, p) if pow(x, h, p) == 1})


def chain_sets(h, p, maxlev=64):
    """List [D_0, D_1, ..., D_J] of Python sets, D_J = F_p.  Small p only (O(p^2) per level)."""
    D = [set(mu(h, p)) | {0}]
    while len(D[-1]) < p:
        A = D[-1]
        D.append({(x - y) % p for x in A for y in A})
        assert len(D) <= maxlev
    return D


def depth_fft(h, p):
    """J(h,p) and the sizes |D_j|, via cyclic boolean autocorrelation (numpy FFT)."""
    ind = np.zeros(p)
    ind[0] = 1
    x = 1
    g = None
    # mu_h = {y^kappa}: generate by powering an element of order h
    kappa = (p - 1) // h
    for c in range(2, p):
        z = pow(c, kappa, p)
        if h == 1 or all(pow(z, h // q, p) != 1 for q in prime_factors(h)):
            g = z
            break
    if h == 1:
        g = 1
    for _ in range(h):
        ind[x] = 1
        x = x * g % p
    sizes = [int(ind.sum())]
    J = 0
    while sizes[-1] < p:
        F = np.fft.rfft(ind)
        # (D - D)(z) = sum_x 1_D(x) 1_D(x - z): correlation
        corr = np.fft.irfft(F * np.conj(F), n=p)
        ind = (corr > 0.5).astype(float)
        J += 1
        sizes.append(int(ind.sum()))
    return J, sizes


def prime_factors(n):
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def split_tables(D, p):
    """For j < J: SX[j][a], SXP[j][a] with SX - SXP = a, both in D_j, for a in D_{j+1}; else -1.
    Deterministic choice: least x in D_j (as an integer in [0,p))."""
    SX, SXP = [], []
    for j in range(len(D) - 1):
        sx = np.full(p, -1, dtype=np.int64)
        sxp = np.full(p, -1, dtype=np.int64)
        Dj = sorted(D[j])
        Djs = D[j]
        for a in D[j + 1]:
            for x in Dj:
                xp = (x - a) % p
                if xp in Djs:
                    sx[a], sxp[a] = x, xp
                    break
            assert sx[a] >= 0
        SX.append(sx)
        SXP.append(sxp)
    return SX, SXP


# ------------------------------------------------------------------ streams and algebra

class Stream:
    """Fresh i.i.d. columns in F_p^n (uniform unless `gen` is given), counted; optional cap."""

    def __init__(self, p, n, rng, cap=None, gen=None):
        self.p, self.n, self.rng, self.cap, self.gen = p, n, rng, cap, gen
        self.buf = np.empty((1 << 10, max(n, 1)), dtype=np.int64)
        self.count = 0

    def draw(self, k):
        if self.cap is not None and self.count + k > self.cap:
            raise Exhausted
        while self.count + k > len(self.buf):
            nb = np.empty((2 * len(self.buf), self.buf.shape[1]), dtype=np.int64)
            nb[: len(self.buf)] = self.buf
            self.buf = nb
        if self.gen is None:
            self.buf[self.count:self.count + k] = self.rng.integers(0, self.p, (k, self.buf.shape[1]))
        else:
            self.buf[self.count:self.count + k] = self.gen(k)
        idx = np.arange(self.count, self.count + k)
        self.count += k
        return idx


def kernel_vec(A, p):
    """Nonzero x with A x = 0 mod p for a d x k matrix with k > d (Python ints; any p)."""
    A = [[int(v) % p for v in row] for row in A]
    d = len(A)
    k = len(A[0]) if d else None
    if d == 0:
        return None
    piv, r = [], 0
    for c in range(k):
        if r == d:
            break
        i = next((i for i in range(r, d) if A[i][c]), None)
        if i is None:
            continue
        A[r], A[i] = A[i], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [v * inv % p for v in A[r]]
        for i2 in range(d):
            if i2 != r and A[i2][c]:
                f = A[i2][c]
                A[i2] = [(v - f * w) % p for v, w in zip(A[i2], A[r])]
        piv.append(c)
        r += 1
    free = next(c for c in range(k) if c not in set(piv))
    x = [0] * k
    x[free] = 1
    for row, pc in enumerate(piv):
        x[pc] = (-A[row][free]) % p
    return x


# ------------------------------------------------------------------ table solver (small p)

class Chain:
    def __init__(self, h, p):
        self.h, self.p = h, p
        self.D = chain_sets(h, p)
        self.J = len(self.D) - 1
        self.SX, self.SXP = split_tables(self.D, p)
        self.member = [np.array([x in Dj for x in range(p)]) for Dj in self.D]


def solve(ch, level, d, target, st, stats=None):
    """Level-`level` solve in dimension d with the given target (length d).  Returns
    (idx, w): fresh indices, weights in D_level (nonzero mod p), sum w_i v_i[:d] = target."""
    p, J = ch.p, ch.J
    if level == J:
        assert not any(int(t) % p for t in target)
        idx = st.draw(d + 1)
        if d == 0:
            return idx[:1], np.array([1], dtype=np.int64)
        x = np.array(kernel_vec(st.buf[idx, :d].T.tolist(), p), dtype=np.int64)
        keep = x != 0
        return idx[keep], x[keep]
    t = np.asarray(target, dtype=np.int64) % p
    stages = []
    for dd in range(d, 0, -1):
        switches = []
        reach = {0: ()}
        while len(reach) < p:
            aidx, aw = solve(ch, level + 1, dd - 1, np.zeros(dd - 1, dtype=np.int64), st, stats)
            beta = int((aw @ st.buf[aidx, dd - 1]) % p)
            x = ch.SX[level][aw]
            xp = ch.SXP[level][aw]
            k = len(switches)
            switches.append((aidx, x, xp))
            if stats is not None:
                stats["switches"] = stats.get("switches", 0) + 1
            new = {}
            for r, T in reach.items():
                v = (r + beta) % p
                if v not in reach and v not in new:
                    new[v] = T + (k,)
            reach.update(new)
        c = np.zeros(dd, dtype=np.int64)
        for (aidx, x, xp) in switches:
            c = (c + xp @ st.buf[aidx, :dd]) % p
        stages.append((dd, t.copy(), c, switches, reach))
        t = (t - c)[: dd - 1] % p
    z = st.draw(1)
    widx, ww = [z], [np.array([1], dtype=np.int64)]
    for (dd, tdd, c, switches, reach) in reversed(stages):
        I = np.concatenate(widx)
        W = np.concatenate(ww)
        s = (W @ st.buf[I, :dd]) % p
        resid = (tdd - c - s) % p
        assert not np.any(resid[: dd - 1])
        T = set(reach[int(resid[dd - 1])])
        for k, (aidx, x, xp) in enumerate(switches):
            src = x if k in T else xp
            keep = src != 0
            widx.append(aidx[keep])
            ww.append(src[keep])
    return np.concatenate(widx), np.concatenate(ww)


def check(ch, st, I, W, d, target, level):
    """Exact check: nonempty, distinct indices, weights nonzero and in D_level, correct sum."""
    p = ch.p
    if len(I) == 0 or len(set(I.tolist())) != len(I):
        return False
    if np.any(W % p == 0) or not np.all(ch.member[level][W % p]):
        return False
    s = (W @ st.buf[I, :d]) % p if d else np.zeros(0, dtype=np.int64)
    return bool(np.all(s == np.asarray(target, dtype=np.int64) % p))


# ------------------------------------------------------------------ expectations

@lru_cache(maxsize=None)
def covering_time_exact(p):
    """Exact E[#uniform draws until subset sums cover F_p] (2^p-state memo; p <= 17)."""
    full = (1 << p) - 1

    @lru_cache(maxsize=None)
    def E(mask):
        if mask == full:
            return Fraction(0)
        tot = Fraction(1)
        for b in range(1, p):
            sh = ((mask << b) | (mask >> (p - b))) & full
            tot += Fraction(1, p) * E(mask | sh)
        return tot / (1 - Fraction(1, p))

    return E(1)


def covering_time_mc(p, draws, seed):
    rng = random.Random(seed)
    full = (1 << p) - 1
    tot = 0
    tot2 = 0
    for _ in range(draws):
        mask, k = 1, 0
        while mask != full:
            b = rng.randrange(p)
            mask |= ((mask << b) | (mask >> (p - b))) & full
            k += 1
        tot += k
        tot2 += k * k
    m = tot / draws
    return m, math.sqrt((tot2 / draws - m * m) / draws)


def sigma_public(p):
    return min(p, math.ceil(2 * math.log2(p - 1)) + 4)


def expected_reads(J, n, s):
    """N_0(n) for depth J: N_J(d) = d+1, N_j(d) = 1 + s * sum_{e<d} N_{j+1}(e)."""
    N = [Fraction(d + 1) if isinstance(s, Fraction) else float(d + 1) for d in range(n + 1)]
    for _ in range(J):
        pref = [0]
        for d in range(n + 1):
            pref.append(pref[-1] + N[d])
        N = [1 + s * pref[d] for d in range(n + 1)]
    return N[n]


# ------------------------------------------------------------------ scaled J = 1 solver (any p)

class BigStream:
    """Fresh uniform columns of F_p^n as Python ints (any size of p)."""

    def __init__(self, p, n, seed, cap=None):
        self.p, self.n, self.cap = p, n, cap
        self.rng = random.Random(seed)
        self.cols = []

    def draw(self, k):
        if self.cap is not None and len(self.cols) + k > self.cap:
            raise Exhausted
        start = len(self.cols)
        for _ in range(k):
            self.cols.append([self.rng.randrange(self.p) for _ in range(self.n)])
        return list(range(start, start + k))

    @property
    def count(self):
        return len(self.cols)


def split_random(a, h, kappa, p, rng, cap, stats):
    """x, x' in mu_h u {0} with x - x' = a, by random search; returns (x, x', b) where b is a
    known kappa-th root of x (or None if x = 0)."""
    if a == 0:
        return 0, 0
    if pow(a, h, p) == 1:
        return a, 0
    if pow(-a % p, h, p) == 1:
        return 0, (-a) % p
    stats["split_searches"] = stats.get("split_searches", 0) + 1
    for _ in range(cap):
        stats["split_trials"] = stats.get("split_trials", 0) + 1
        b = rng.randrange(1, p)
        u = pow(b, kappa, p)
        w = (u - a) % p
        if w and pow(w, h, p) == 1:
            return u, w
    raise Exhausted


def solve_scaled(d, target, st, h, kappa, rng, split_cap, stats):
    """Level-0 solve, J = 1 (requires D_0 - D_0 = F_p).  Weights in mu_h u {0}."""
    p = st.p
    K = max(1, (p - 1).bit_length())          # 2^K > p - 1
    t = [x % p for x in target]
    stages = []
    for dd in range(d, 0, -1):
        switches = []
        for k in range(K):
            while True:
                idx = st.draw(dd)
                if dd == 1:
                    alpha = [1]
                else:
                    alpha = kernel_vec([[st.cols[i][r] for i in idx] for r in range(dd - 1)], p)
                beta = sum(a * st.cols[i][dd - 1] for a, i in zip(alpha, idx)) % p
                if beta:
                    break
                stats["zero_beta"] = stats.get("zero_beta", 0) + 1
            sc = pow(2, k, p) * pow(beta, p - 2, p) % p
            alpha = [a * sc % p for a in alpha]
            xs, xps = [], []
            for a in alpha:
                x, xp = split_random(a, h, kappa, p, rng, split_cap, stats)
                xs.append(x)
                xps.append(xp)
            switches.append((idx, xs, xps))
        c = [0] * dd
        for (idx, xs, xps) in switches:
            for i, xp in zip(idx, xps):
                if xp:
                    for r in range(dd):
                        c[r] = (c[r] + xp * st.cols[i][r]) % p
        stages.append((dd, list(t), c, switches))
        t = [(t[r] - c[r]) % p for r in range(dd - 1)]
    z = st.draw(1)
    W = {z[0]: 1}
    for (dd, tdd, c, switches) in reversed(stages):
        s = [0] * dd
        for i, w in W.items():
            for r in range(dd):
                s[r] = (s[r] + w * st.cols[i][r]) % p
        resid = [(tdd[r] - c[r] - s[r]) % p for r in range(dd)]
        assert not any(resid[: dd - 1])
        a = resid[dd - 1]
        for k, (idx, xs, xps) in enumerate(switches):
            src = xs if (a >> k) & 1 else xps
            for i, w in zip(idx, src):
                if w:
                    W[i] = w
    return W


def check_big(W, st, d, target, h, p):
    if not W:
        return False
    for w in W.values():
        if w % p == 0 or pow(w, h, p) != 1:
            return False
    for r in range(d):
        if sum(w * st.cols[i][r] for i, w in W.items()) % p != target[r] % p:
            return False
    return True


# ------------------------------------------------------------------ Weil threshold

def weil_pairs_lower(kappa, p):
    """Lower bound on #{(u,v) in mu_h^2 : u - v = y} for y != 0 (Jacobi sums)."""
    A = (kappa - 1) * (kappa - 2)
    return (p - A * math.sqrt(p) - (kappa - 1) - 2 * kappa) / kappa ** 2


def weil_ok(kappa, p):
    return math.sqrt(p) > (kappa - 1) * (kappa - 2) + 3


# ------------------------------------------------------------------ cyclotomic constants

def cyclotomic_poly(h):
    """Integer coefficients (low to high) of Phi_h."""
    from sympy import cyclotomic_poly as cp, Poly, symbols
    X = symbols("X")
    return [int(c) for c in reversed(Poly(cp(h, X), X).all_coeffs())]


def power_basis_coeffs(h):
    """coef[t] = coordinates of zeta^t (t < h) in the basis 1, zeta, ..., zeta^{phi-1}."""
    phi_c = cyclotomic_poly(h)
    phi = len(phi_c) - 1
    coef = []
    cur = [1] + [0] * (phi - 1)
    for t in range(h):
        coef.append(list(cur))
        # multiply by zeta
        nxt = [0] + cur[:-1]
        top = cur[-1]
        if top:
            nxt = [nxt[i] - top * phi_c[i] for i in range(phi)]
        cur = nxt
    return phi, coef


def l1_ball_count(phi, K):
    """#{m in Z^phi : ||m||_1 <= K}."""
    K = int(math.floor(K))
    return sum(2 ** i * math.comb(phi, i) * math.comb(K, i) for i in range(min(phi, K) + 1))
