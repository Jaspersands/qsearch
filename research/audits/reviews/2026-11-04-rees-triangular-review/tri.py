#!/usr/bin/env python
"""Referee check of Proposition prop:triangular-sde (main.tex, "Triangular
two-level solver"), 2026-11-04.

The solver is implemented exactly as the written proof describes it:

  * cos(y) = nu  iff  y in g^nu P, computed from y^((p-1)/kappa);
  * round k: take the next a - dim U_k + 1 unused columns, find delta != 0
    with e_{k+1} = sum delta_i lambda_i in U_k, scale so that the FIRST
    nonzero entry is 1, form v_{k+1} = sum beta_{cos delta_i} delta_i lambda_i;
    stop if v_{k+1} in U_k (R = realisation with zeta = 1), else
    U_{k+1} = U_k + F_p v_{k+1};
  * back substitution: tau = -R; for l = k..1, zeta_l = v_l-coordinate of
    tau in U_{l-1} + F_p v_l; if zeta_l != 0 add the weights
    x_i = zeta_l delta_i (alpha_n + beta_{cos delta_i}), n = cos(zeta_l), and
    tau -= zeta_l (alpha_n e_l + v_l);
  * finally take kappa-th roots and a Bezout exponent t (t d' = 1 mod q').

The contraction (alpha, beta) is found here by our own search (exhaustive
for small p, randomized otherwise), in the normal form alpha_0 = 1,
beta_0 = 0, with the conditions alpha_j + beta_i in g^{-(i+j)} P u {0}.
The script does not use the files of the 2026-11-02 linear-arity pass.

Usage: nice -n 10 /opt/anaconda3/bin/python tri.py [--quick] [--jobs 2]
Writes tri_results.json next to this file.
"""
import argparse
import itertools
import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------- arithmetic
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for q in range(3, r + 1, 2):
        if n % q == 0:
            return False
    return True


def factor(n):
    out, q = [], 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p):
    fs = factor(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g
    return 1  # p = 2


class Field:
    """F_p with the coset labelling of a coset generator g."""

    def __init__(self, p, kappa, g):
        self.p, self.kappa, self.g = p, kappa, g
        self.h = (p - 1) // kappa
        zeta = pow(g, self.h, p)
        self.roots = {}
        z = 1
        for nu in range(kappa):
            assert z not in self.roots, "g is not a coset generator"
            self.roots[z] = nu
            z = z * zeta % p
        self.pow_evals = 0

    def cos(self, y):
        """Coset index of y != 0 (one evaluation of y -> y^h)."""
        y %= self.p
        assert y != 0
        self.pow_evals += 1
        return self.roots[pow(y, self.h, self.p)]

    def in_P0(self, y):
        """y in P u {0}?  (not counted: verification only)"""
        y %= self.p
        return y == 0 or pow(y, self.h, self.p) == 1


# ------------------------------------------------------- contraction search
def coset_tables(p, kappa, g):
    """lab[x] = coset index of x (x != 0), -1 at 0.  inQ0[m][x] = x in Q_m u {0}."""
    h = (p - 1) // kappa
    zeta = pow(g, h, p)
    zpow = {}
    z = 1
    for nu in range(kappa):
        zpow[z] = nu
        z = z * zeta % p
    lab = np.full(p, -1, dtype=np.int64)
    for x in range(1, p):
        lab[x] = zpow[pow(x, h, p)]
    inQ0 = np.zeros((kappa, p), dtype=bool)
    for m in range(kappa):
        inQ0[m] = (lab == m)
        inQ0[m][0] = True
    return lab, inQ0


def check_contraction(p, kappa, g, alpha, beta):
    F = Field(p, kappa, g)
    for i in range(kappa):
        for j in range(kappa):
            y = (alpha[j] + beta[i]) % p
            if y == 0:
                continue
            if (F.cos(y) + i + j) % kappa != 0:
                return False
    return (alpha[0] + beta[0]) % p != 0


def alpha_candidates(p, kappa, inQ0, beta):
    """For fixed beta (beta_0 = 0), the admissible alpha_j, j = 1..kappa-1."""
    xs = np.arange(p)
    cands = []
    for j in range(1, kappa):
        ok = inQ0[(-j) % kappa].copy()  # i = 0: alpha_j + 0
        for i in range(1, kappa):
            ok &= inQ0[(-(i + j)) % kappa][(xs + beta[i]) % p]
        cands.append(np.nonzero(ok)[0])
    return cands


def find_contraction(p, kappa, g, rng, exhaustive_below=200, tries=200000):
    """Return (alpha, beta) with alpha_0 = 1, beta_0 = 0, or None if none exists
    (only claimed when the exhaustive search ran)."""
    lab, inQ0 = coset_tables(p, kappa, g)
    xs = np.arange(p)
    # beta_i must satisfy 1 + beta_i in Q_{-i} u {0}
    bset = [None] + [np.nonzero(inQ0[(-i) % kappa][(xs + 1) % p])[0] for i in range(1, kappa)]

    def finish(beta):
        cands = alpha_candidates(p, kappa, inQ0, beta)
        if all(len(c) for c in cands):
            alpha = [1] + [int(c[0]) for c in cands]
            assert check_contraction(p, kappa, g, alpha, beta)
            return alpha, list(beta)
        return None

    if p < exhaustive_below:
        for bs in itertools.product(*bset[1:]):
            r = finish([0] + [int(b) for b in bs])
            if r:
                return r
        return None
    for _ in range(tries):
        beta = [0] + [int(rng.choice(bset[i])) for i in range(1, kappa)]
        r = finish(beta)
        if r:
            return r
    # fall back to exhaustive (slow, but only reached near E_2)
    for bs in itertools.product(*bset[1:]):
        r = finish([0] + [int(b) for b in bs])
        if r:
            return r
    return None


# --------------------------------------------------------- linear algebra
class Counter:
    def __init__(self):
        self.elims = 0


def rref(A, p):
    """Row-reduce a list of rows mod p in place; return pivot columns."""
    rows, cols = len(A), (len(A[0]) if A else 0)
    piv, r = [], 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return piv


def dependency_mod_U(block, Ubasis, a, p, C):
    """delta != 0 (length len(block)) with sum delta_i lambda_i in span(Ubasis).
    One Gaussian elimination on the a x (|block| + dim U) matrix."""
    C.elims += 1
    vecs = list(block) + list(Ubasis)
    n = len(vecs)
    if a == 0:
        null = [1] + [0] * (n - 1)
    else:
        A = [[vecs[j][r] % p for j in range(n)] for r in range(a)]
        piv = rref(A, p)
        free = [c for c in range(n) if c not in piv]
        assert free, "no dependency: column count wrong"
        f = free[0]
        null = [0] * n
        null[f] = 1
        for r, c in enumerate(piv):
            null[c] = (-A[r][f]) % p
    delta = null[: len(block)]
    assert any(delta), "dependency has zero block part (U basis dependent?)"
    return delta


def coords(tau, basis, a, p, C):
    """Coordinates of tau in the independent list basis (tau must lie in its span)."""
    C.elims += 1
    n = len(basis)
    if n == 0:
        assert not any(t % p for t in tau)
        return []
    A = [[basis[j][r] % p for j in range(n)] + [tau[r] % p] for r in range(a)]
    piv = rref(A, p)
    assert n not in piv, "tau not in span"
    assert piv == list(range(n)), "basis dependent"
    return [A[r][n] for r in range(n)]


def in_span(v, basis, a, p, C):
    C.elims += 1
    if a == 0:
        return True
    n = len(basis)
    A = [[basis[j][r] % p for j in range(n)] + [v[r] % p] for r in range(a)]
    piv = rref(A, p)
    return n not in piv


def lin(p, terms, a):
    out = [0] * a
    for c, vec in terms:
        if c % p:
            for r in range(a):
                out[r] = (out[r] + c * vec[r]) % p
    return out


# ------------------------------------------------------------- the solver
def triangular(cols, a, F, alpha, beta, normalise="first"):
    """Proposition prop:triangular-sde, as written.  Returns (x, info)."""
    p = F.p
    C = Counter()
    F.pow_evals = 0
    M = len(cols)
    x = [0] * M
    U = []          # basis v_1..v_k of U_k (U_k = span(v_1..v_k))
    rounds = []     # per round l: (indices, delta, e_l, v_l)
    nxt = 0
    k = 0
    while True:
        need = a - len(U) + 1
        assert nxt + need <= M, "ran out of columns"
        idx = list(range(nxt, nxt + need))
        nxt += need
        block = [cols[i] for i in idx]
        delta = dependency_mod_U(block, U, a, p, C)
        nz = [t for t, dl in enumerate(delta) if dl % p]
        pos = nz[0] if normalise == "first" else nz[-1]
        inv = pow(delta[pos], p - 2, p)
        delta = [dl * inv % p for dl in delta]
        e = lin(p, [(delta[t], block[t]) for t in range(need)], a)
        cs = [F.cos(dl) if dl % p else None for dl in delta]
        v = lin(p, [(beta[cs[t]] * delta[t], block[t]) for t in range(need) if delta[t] % p], a)
        if in_span(v, U, a, p, C):
            # R: realisation with zeta = 1 (n = cos(1) = 0)
            for t in range(need):
                if delta[t] % p:
                    x[idx[t]] = delta[t] * (alpha[0] + beta[cs[t]]) % p
            Rval = lin(p, [(x[i], cols[i]) for i in idx], a)
            assert x[idx[pos]] == (alpha[0] + beta[0]) % p == 1
            break
        rounds.append((idx, delta, cs, e, v))
        U.append(v)
        k += 1
    tau = [(-r) % p for r in Rval]
    for l in range(k, 0, -1):
        idx, delta, cs, e, v = rounds[l - 1]
        co = coords(tau, U[:l], a, p, C)
        z = co[l - 1]
        if z % p:
            n = F.cos(z)
            for t in range(len(idx)):
                if delta[t] % p:
                    x[idx[t]] = z * delta[t] * (alpha[n] + beta[cs[t]]) % p
            tau = [(tt - z * (alpha[n] * ee + vv)) % p for tt, ee, vv in zip(tau, e, v)]
        # invariant: tau in U_{l-1}
    assert not any(tau), "tau != 0 at the end"
    info = dict(used=nxt, rounds=k + 1, elims=C.elims, pow_evals=F.pow_evals)
    return x, info


def kth_root_table(p, kappa):
    t = {0: 0}
    for y in range(1, p):
        t.setdefault(pow(y, kappa, p), y)
    return t


def verify(cols, a, F, x, roots, rng):
    p, kappa = F.p, F.kappa
    assert len(x) == len(cols)
    assert any(xi % p for xi in x), "x = 0"
    assert all(F.in_P0(xi) for xi in x), "x not in P u {0}"
    s = lin(p, [(xi, c) for xi, c in zip(x, cols)], a)
    assert not any(s), "sum x_i lambda_i != 0"
    # passage to eq:sde-target: d = kappa d' with gcd(d', q') = 1
    q = (p - 1) // kappa
    while True:
        dp = rng.randrange(1, 4 * q + 5)
        if math.gcd(dp, q) == 1:
            break
    d = kappa * dp
    assert math.gcd(d, p - 1) == kappa
    t = pow(dp, -1, q) if q > 1 else 1
    if t == 0:
        t = q
    u = [roots[xi % p] for xi in x]
    ss = [pow(ui, t, p) for ui in u]
    assert any(ss)
    tot = lin(p, [(pow(si, d, p), c) for si, c in zip(ss, cols)], a)
    assert not any(tot), "sde-target fails"
    return d


# ---------------------------------------------------------- column families
def families(a, p, kappa, M, F, rng):
    rv = lambda: [rng.randrange(p) for _ in range(a)]
    unit = lambda i, c=1: [c % p if r == i else 0 for r in range(a)]
    fam = {}
    fam["random"] = [rv() for _ in range(M)]
    fam["zero"] = [[0] * a for _ in range(M)]
    w = rv()
    fam["all_equal"] = [list(w) for _ in range(M)]
    # scalar multiples of one vector with coset-varied scalars
    gpows = [pow(F.g, nu, p) for nu in range(kappa)]
    fam["coset_multiples"] = [[gpows[t % kappa] * c % p for c in w] for t in range(M)]
    if a >= 1:
        fam["units_cycled"] = [unit(t % a, gpows[(t // a) % kappa]) for t in range(M)]
        fam["units_blocks"] = [unit(min(t * a // M, a - 1)) for t in range(M)]
        # low rank: span of one or two random vectors
        b1, b2 = rv(), rv()
        fam["rank2"] = [lin(p, [(rng.randrange(p), b1), (rng.randrange(p), b2)], a) for _ in range(M)]
        fam["sparse"] = [unit(rng.randrange(a), rng.randrange(1, p)) if rng.random() < .8 else [0] * a
                         for _ in range(M)]
        # non-residue-heavy entries
        nr = [y for y in range(1, min(p, 400)) if F.in_P0(y) is False]
        fam["nonresidue_entries"] = [[rng.choice(nr) if nr else 1 for _ in range(a)] for _ in range(M)]
        # small entries
        fam["small_entries"] = [[rng.randrange(3) for _ in range(a)] for _ in range(M)]
    return fam


def greedy_adversary(a, p, kappa, M, F, alpha, beta, rng, trials=12):
    """Try to build column sets that keep the solver running as long as
    possible: random columns, keep the set using the most columns."""
    best, bestu = None, -1
    for _ in range(trials):
        cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
        _, info = triangular(cols, a, F, alpha, beta)
        if info["used"] > bestu:
            best, bestu = cols, info["used"]
    return best


# ---------------------------------------------- existence (tightness probe)
def has_solution(cols, a, p, Pset):
    """Is there a nonzero x in (P u {0})^N with sum x_i lambda_i = 0?  DP over F_p^a."""
    if a == 0:
        return len(cols) > 0
    n = p ** a
    base = np.array([p ** r for r in range(a)], dtype=np.int64)
    digits = (np.arange(n)[:, None] // base[None, :]) % p
    S = np.zeros(n, dtype=bool)  # sums of choices with nonempty support
    for lam in cols:
        S0 = S.copy()
        S0[0] = True               # empty choice allowed before adding w*lam
        new = S.copy()
        for w in Pset:
            mv = np.array([w * c % p for c in lam], dtype=np.int64)
            perm = ((digits + mv[None, :]) % p) @ base
            new[perm[S0]] = True
        S = new
        if S[0]:
            return True
    return bool(S[0])


# ----------------------------------------------------------------- driver
def primes_for(kappa, E2, quick):
    small = [p for p in range(3, 400) if is_prime(p) and (p - 1) % kappa == 0 and p not in E2]
    mid = [p for p in range(400, 2000) if is_prime(p) and (p - 1) % kappa == 0 and p not in E2]
    big = [p for p in range(2000, 10001) if is_prime(p) and (p - 1) % kappa == 0 and p not in E2]
    rng = random.Random(1000 + kappa)
    nsmall = 10 if quick else 30
    out = small[:nsmall] + rng.sample(mid, min(len(mid), 4 if quick else 10)) \
        + rng.sample(big, min(len(big), 4 if quick else 12)) + [big[-1]]
    return sorted(set(out))


E2_KNOWN = {2: set(), 3: set(), 4: {5, 13, 17, 29, 37, 53}}


def job(args):
    kappa, p, quick, seed = args
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    pr = primitive_root(p)
    # coset generator: a random one (not necessarily a primitive root)
    while True:
        g = rng.randrange(2, p) if p > 3 else 2
        if len(set(pow(g, nu * (p - 1) // kappa, p) for nu in range(kappa))) == kappa:
            break
    con = find_contraction(p, kappa, g, nrng)
    res = dict(kappa=kappa, p=p, g=g, contraction=None, runs=0, fails=[], by_a={},
               max_elims={}, max_pow={}, used_all=0, gP_runs=0)
    if con is None:
        res["no_contraction"] = True
        return res
    alpha, beta = con
    res["contraction"] = dict(alpha=alpha, beta=beta)
    F = Field(p, kappa, g)
    roots = kth_root_table(p, kappa)
    # a second representative g' = g*q, q in P: same cosets, same (alpha, beta)
    q = pow(rng.randrange(1, p), kappa, p)
    F2 = Field(p, kappa, g * q % p)
    reps = 3 if quick else 8
    for a in range(0, 7):
        M = (a + 1) * (a + 2) // 2
        stats = dict(runs=0, used_all=0, max_used=0, max_elims=0, max_pow=0)
        for rep in range(reps):
            fam = families(a, p, kappa, M, F, rng)
            if a >= 1:
                fam["greedy"] = greedy_adversary(a, p, kappa, M, F, alpha, beta, rng,
                                                 trials=4 if quick else 10)
            for name, cols in fam.items():
                for FF, tag in ((F, "g"), (F2, "gq")):
                    try:
                        x, info = triangular(cols, a, FF, alpha, beta)
                        verify(cols, a, FF, x, roots, rng)
                        assert info["used"] <= M
                        # cost claims: rounds <= a+1; elims <= 3(a+1); pow evals <= M + a
                        assert info["rounds"] <= a + 1
                        assert info["elims"] <= 3 * (a + 1)
                        assert info["pow_evals"] <= M + a
                    except AssertionError as ex:
                        res["fails"].append(dict(a=a, family=name, g=tag, err=str(ex), cols=cols))
                        continue
                    stats["runs"] += 1
                    stats["used_all"] += info["used"] == M
                    stats["max_used"] = max(stats["max_used"], info["used"])
                    stats["max_elims"] = max(stats["max_elims"], info["elims"])
                    stats["max_pow"] = max(stats["max_pow"], info["pow_evals"])
                    if tag == "gq":
                        res["gP_runs"] += 1
                    # same columns, last-entry normalisation (coherent lemmas)
                    if tag == "g":
                        x2, _ = triangular(cols, a, FF, alpha, beta, normalise="last")
                        verify(cols, a, FF, x2, roots, rng)
        res["by_a"][a] = stats
        res["runs"] += stats["runs"]
        res["used_all"] += stats["used_all"]
    return res


def exhaustive_job(args):
    """Every column tuple for tiny (p, kappa, a)."""
    p, kappa, a = args
    rng = random.Random(p * 100 + a)
    g = primitive_root(p)
    con = find_contraction(p, kappa, g, np.random.default_rng(0))
    alpha, beta = con
    F = Field(p, kappa, g)
    roots = kth_root_table(p, kappa)
    M = (a + 1) * (a + 2) // 2
    vecs = [list(v) for v in itertools.product(range(p), repeat=a)]
    n = fails = used_all = 0
    for tup in itertools.product(range(len(vecs)), repeat=M):
        cols = [vecs[i] for i in tup]
        try:
            x, info = triangular(cols, a, F, alpha, beta)
            verify(cols, a, F, x, roots, rng)
            used_all += info["used"] == M
        except AssertionError:
            fails += 1
        n += 1
    return dict(p=p, kappa=kappa, a=a, M=M, tuples=n, fails=fails, used_all=used_all,
                alpha=alpha, beta=beta)


def tightness_job(args):
    """Search for M-1 columns with NO nonzero x in (P u {0})^{M-1}."""
    p, kappa, a, budget, seed = args
    rng = random.Random(seed)
    M = (a + 1) * (a + 2) // 2
    N = M - 1
    Pset = sorted({pow(y, kappa, p) for y in range(1, p)})
    gens = []
    found = None
    tried = 0
    t0 = time.time()
    # structured candidates first: units times coset representatives
    pr = primitive_root(p)
    reps = [pow(pr, nu, p) for nu in range(kappa)]
    pool = [[(c if r == i else 0) for r in range(a)] for i in range(a) for c in range(1, p)]
    while tried < budget and time.time() - t0 < 120:
        mode = rng.random()
        if mode < 0.4:
            cols = [rng.choice(pool) for _ in range(N)]
        elif mode < 0.7:
            cols = [[rng.choice([0] + reps + [rng.randrange(p)]) for _ in range(a)] for _ in range(N)]
        else:
            cols = [[rng.randrange(p) for _ in range(a)] for _ in range(N)]
        tried += 1
        if not has_solution(cols, a, p, Pset):
            found = cols
            break
    solver_on_cex = None
    if found is not None:
        # independent re-check by brute force over (P u {0})^N, and the solver
        # (which must run out of columns, since no solution exists)
        W = [0] + Pset
        assert len(W) ** N > 2 * 10 ** 6 or not any(any(x) and not any(sum(xi * c[r] for xi, c in zip(x, found)) % p
                                          for r in range(a))
                       for x in itertools.product(W, repeat=N))
        g = primitive_root(p)
        con = find_contraction(p, kappa, g, np.random.default_rng(0))
        try:
            triangular(found, a, Field(p, kappa, g), con[0], con[1])
            solver_on_cex = "returned (impossible)"
        except AssertionError as ex:
            solver_on_cex = str(ex)
    return dict(p=p, kappa=kappa, a=a, M=M, N=N, tried=tried, counterexample=found,
                solver_on_counterexample=solver_on_cex,
                chevalley_warning_forces=N > kappa * a)


def e2_check():
    """Recompute E_2(kappa) below small bounds with our exhaustive search."""
    out = {}
    for kappa, bound in ((2, 200), (3, 120), (4, 120)):
        ex = []
        for p in range(3, bound):
            if is_prime(p) and (p - 1) % kappa == 0:
                g = primitive_root(p)
                if find_contraction(p, kappa, g, np.random.default_rng(0), exhaustive_below=10 ** 9) is None:
                    ex.append(p)
        out[kappa] = dict(bound=bound, exceptional=ex)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--jobs", type=int, default=2)
    args = ap.parse_args()
    t0 = time.time()
    out = {}
    out["e2_check"] = e2_check()
    print("E_2 check:", out["e2_check"], flush=True)
    for kappa in (2, 3, 4):
        assert set(out["e2_check"][kappa]["exceptional"]) == {p for p in E2_KNOWN[kappa]
                                                             if p < out["e2_check"][kappa]["bound"]}
    tasks = []
    for kappa in (2, 3, 4):
        for p in primes_for(kappa, E2_KNOWN[kappa], args.quick):
            tasks.append((kappa, p, args.quick, 7919 * p + kappa))
    with Pool(args.jobs) as pool:
        res = pool.map(job, tasks, chunksize=1)
    out["random_and_adversarial"] = []
    tot = fails = used_all = gP = 0
    for r in res:
        out["random_and_adversarial"].append({k: v for k, v in r.items()})
        tot += r["runs"]
        fails += len(r["fails"])
        used_all += r["used_all"]
        gP += r["gP_runs"]
    out["summary"] = dict(runs=tot, fails=fails, used_all_M=used_all, runs_with_g_times_P=gP,
                          primes={k: sorted(r["p"] for r in res if r["kappa"] == k) for k in (2, 3, 4)},
                          no_contraction=[(r["kappa"], r["p"]) for r in res if r.get("no_contraction")])
    print("summary:", out["summary"], flush=True)
    ex_tasks = [(3, 2, 1), (5, 2, 1), (7, 2, 1), (7, 3, 1), (13, 3, 1), (41, 4, 1), (3, 2, 2)]
    if args.quick:
        ex_tasks = ex_tasks[:-1]
    with Pool(args.jobs) as pool:
        out["exhaustive"] = pool.map(exhaustive_job, ex_tasks, chunksize=1)
    print("exhaustive:", [(e["p"], e["kappa"], e["a"], e["tuples"], e["fails"], e["used_all"])
                          for e in out["exhaustive"]], flush=True)
    t_tasks = []
    for (p, kappa) in ((3, 2), (5, 2), (7, 2), (7, 3), (13, 3), (19, 3), (41, 4), (61, 4)):
        for a in range(1, 7):
            M = (a + 1) * (a + 2) // 2
            if p ** a > 3 * 10 ** 5 or M - 1 > kappa * a:
                continue  # too big, or Chevalley-Warning already forces a solution
            t_tasks.append((p, kappa, a, 3000 if args.quick else 20000, 31 * p + a))
    with Pool(args.jobs) as pool:
        out["tightness"] = pool.map(tightness_job, t_tasks, chunksize=1)
    for t in out["tightness"]:
        print("tight", t["p"], t["kappa"], t["a"], "N=M-1=", t["N"], "tried", t["tried"],
              "counterexample" if t["counterexample"] else "-", t["counterexample"],
              t["solver_on_counterexample"], flush=True)
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "tri_results.json" if not args.quick else "tri_results_quick.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=int)
    print("done in %.0fs" % out["seconds"])
    return 0 if fails == 0 and all(e["fails"] == 0 for e in out["exhaustive"]) else 1


if __name__ == "__main__":
    sys.exit(main())
