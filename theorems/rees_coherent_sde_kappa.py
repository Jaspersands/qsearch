"""Coherent (reversible) SDE solve at any fixed kappa_d >= 2 (p not in E_2(kappa)).

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-04-rees-coherent-sde-k3.md (written for
kappa_d = 3, e.g. grade 3 of n4(F_7); the module is general in kappa).

At a recursion grade d with kappa = kappa_d = gcd(d, p-1) >= 2 the merge needs
a nonzero s with sum_i s_i^d lambda_i = 0 (main.tex, eq:sde-target),
lambda_i in F_p^a. This module builds a permutation circuit (X, CX, CCX, SWAP
only) mapping

    |lambda_1..lambda_M>|0>_S|0>_work  ->  |lambda>|s(lambda)>_S|0>_work

on every canonical input, M = (a+1)(a+2)/2, where s is the CANONICAL
triangular witness of the report (Section 1): the solver of
prop:triangular-sde with
  * g = the least integer whose image generates F_p^x / P, P = (F_p^x)^kappa,
    cos(y) = nu iff y in g^nu P, read from y^h = omega^nu, h = (p-1)/kappa,
    omega = g^h;
  * the CANONICAL contraction: the lexicographically least
    (beta_1..beta_{k-1}, alpha_1..alpha_{k-1}) in [0, p)^(2 kappa - 2) with
    alpha_0 = 1, beta_0 = 0 and alpha_j + beta_i in g^-(i+j) P u {0} for all
    i, j (exists iff p not in E_2(kappa)); a classical precomputation;
  * first dependencies (rees_coherent_sde witness with e = 1) for delta in
    every round. The stop test v_{k+1} in U_k is, by report Lemma 4' (every
    kappa; generalises Lemma 4 of the kappa = 2 report), equivalent to "every
    nonzero delta_i is a kappa-th power" and to v_{k+1} = 0: the default
    circuit (stop="power") uses that; stop="general" runs the paper-faithful
    test (a second first dependency per round) and is checked as well;
  * rho(x) = the LEAST kappa-th root of x in {0..p-1}, and the Bezout
    exponent u with u (d/kappa) = 1 mod (p-1)/kappa: s_i = rho(x_i)^u.

Construction (Bennett): F runs every round k = 0..a obliviously (first
dependency of (v_1..v_k, block_k), coset flags, v_{k+1}, the stop bit (an AND
of power flags, or in general mode a first dependency of (v_1..v_{k+1})),
one-hot stop flags), then the coordinates tau, the back substitution with alpha loaded
under the coset flags of zeta, and the weights x. The copy stage computes a
kappa-th root of each x_i by one oblivious generalised Tonelli-Shanks
(Adleman-Manders-Miller digit extraction with the fixed generator g^Q of the
q-Sylow subgroup, S_q - 1 rounds padded) per prime factor q of kappa, then
the least of the kappa roots r * omega^t by comparators and Fredkin swaps,
raises it to u, adds it into S_i and uncomputes. Then F^-1.

Arithmetic: add_product / add_scaled / add_ext / sub_ext of
theorems/rees_circuit_arith.py; helpers of theorems/rees_coherent_sde.py and
theorems/rees_coherent_sde_k2.py (all imported, none edited).

Domain: canonical words (every coordinate < p). Padding words are not
claimed. Does NOT: wire into the generated receiver, the descent (controlled
delta_s), QFT_p, oracle, noise; flip any claim gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import time

import numpy as np

from theorems.rees_circuit_arith import Anc, add_ext, anc_size, formula_counts, sub_ext
from theorems.rees_coherent_sde import BitSim, Prog, chain_length, is_prime, nbits
from theorems.rees_coherent_sde_k2 import (CoherentSDEK2, _and_ccx, _fd_batch, all_inputs,
                                           block_offsets, columns, fd_nonmacro_ccx, fd_products,
                                           first_dependency, input_range, structured_inputs)

STATUS = {"status": "coherent_kappa_sde_solve_finite_checks",
          "scope": "grades with kappa_d = gcd(d, p-1) >= 2 and p not in E_2(kappa_d) (canonical "
                   "contraction found by the stated search), triangular solver of "
                   "prop:triangular-sde at (a+1)(a+2)/2 columns; checked mainly at kappa = 3",
          "coherent_receiver_implemented": False, "general_sde_implemented": False,
          "coherent_kappa3_sde_implemented": True,
          "coherent_fixed_kappa_sde_implemented": True,
          "wired_into_generated_receiver": False,
          "independent_review": False, "speedup_claim_allowed": False}


# ====================================================================== constants

def prime_factors(n):
    """Prime factors of n with multiplicity, ascending."""
    out, q = [], 2
    while q*q <= n:
        while n % q == 0:
            out.append(q)
            n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


def q_adic(p, q):
    """p-1 = q^S Q with q not dividing Q."""
    S, Q = 0, p-1
    while Q % q == 0:
        S, Q = S+1, Q//q
    return S, Q


def kappa_of(p, d):
    return math.gcd(d, p-1)


def coset_generator(p, kappa):
    """Least g >= 2 whose image generates F_p^x / (F_p^x)^kappa."""
    qs = sorted(set(prime_factors(kappa)))
    return next(g for g in range(2, p) if all(pow(g, (p-1)//q, p) != 1 for q in qs))


def bezout_exponent_kappa(p, d):
    """Least u >= 1 with u (d/kappa) = 1 mod (p-1)/kappa, kappa = gcd(d, p-1)."""
    kappa = kappa_of(p, d)
    h = (p-1)//kappa
    if h == 1:
        return 1
    return pow((d//kappa) % h, -1, h)


class Cos:
    """Coset index cos(y) = nu iff y in g^nu P (None for y = 0), via y^h = omega^nu."""

    def __init__(self, p, kappa, g):
        self.p, self.kappa, self.g = p, kappa, g
        self.h = (p-1)//kappa
        self.omega = pow(g, self.h, p)
        self.log = {pow(self.omega, nu, p): nu for nu in range(kappa)}
        assert len(self.log) == kappa

    def __call__(self, y):
        y %= self.p
        return None if y == 0 else self.log[pow(y, self.h, self.p)]

    def ok(self, val, target):
        """val in g^target P u {0}."""
        c = self(val)
        return c is None or c == target % self.kappa


def contraction_valid(p, kappa, g, alpha, beta):
    """All kappa^2 conditions alpha_j + beta_i in g^-(i+j) P u {0}, alpha_0 = 1, beta_0 = 0."""
    cs = Cos(p, kappa, g)
    if alpha[0] % p != 1 or beta[0] % p != 0:
        return False
    return all(cs.ok(alpha[j]+beta[i], -(i+j)) for i in range(kappa) for j in range(kappa))


def canonical_contraction(p, kappa, g=None, scan_cap=None):
    """The canonical contraction (see _canonical_contraction_lazy for the definition).
    For p <= 2*10^6 an exact DFS in the same lexicographic order with pruning: a beta_i
    is kept only if every alpha_j still has a candidate (cross-correlation counts by FFT);
    pruning removes only branches without a completion, so the answer is the same."""
    if p > 2*10**6:
        return _canonical_contraction_lazy(p, kappa, g, scan_cap)
    g = coset_generator(p, kappa) if g is None else g
    h = (p-1)//kappa
    omega = pow(g, h, p)
    logw = {pow(omega, nu, p): nu for nu in range(kappa)}
    pw = np.ones(p, dtype=np.int64)                      # y^h for all y (vectorised)
    base = np.arange(p, dtype=np.int64)
    e = h
    while e:
        if e & 1:
            pw = pw*base % p
        base = base*base % p
        e >>= 1
    cos = np.full(p, -1, dtype=np.int64)
    for val, nu in logw.items():
        cos[pw == val] = nu
    cos[0] = -1
    OK = [(cos == c) | (cos == -1) for c in range(kappa)]   # OK[c][y]: y in g^c P u {0}
    OKf = [np.fft.rfft(np.concatenate([o, o]).astype(float)) for o in OK]

    def counts(cand, c):
        """cnt[t] = #{s : cand[s] and OK[c][s+t mod p]} for all t (circular correlation)."""
        A = np.fft.rfft(np.concatenate([cand[::-1].astype(float), np.zeros(p)]))
        full = np.fft.irfft(A*OKf[c], n=2*p)
        return np.rint(full[p-1:2*p-1]).astype(np.int64)

    beta = [0]*kappa
    cand0 = [None]+[OK[(-j) % kappa].copy() for j in range(1, kappa)]   # i = 0 (beta_0 = 0)

    def dfs(i, cand):
        if i == kappa:
            return [1]+[int(np.argmax(cand[j])) for j in range(1, kappa)]
        okt = OK[(-i) % kappa][(1+np.arange(p)) % p]          # 1 + beta_i in g^-i P u {0}
        for j in range(1, kappa):
            okt &= counts(cand[j], (-(i+j)) % kappa) > 0
        for t in np.nonzero(okt)[0]:
            t = int(t)
            new = [None]+[cand[j] & np.roll(OK[(-(i+j)) % kappa], -t) for j in range(1, kappa)]
            beta[i] = t
            r = dfs(i+1, new)
            if r is not None:
                return r
        return None
    al = dfs(1, cand0)
    if al is None:
        return None
    return tuple(al), tuple(beta)


def _canonical_contraction_lazy(p, kappa, g=None, scan_cap=None):
    """Lexicographically least (beta_1..beta_{k-1}, alpha_1..alpha_{k-1}) in [0,p)^(2k-2)
    with alpha_0 = 1, beta_0 = 0 and alpha_j + beta_i in g^-(i+j) P u {0}; None if none
    exists (p in E_2(kappa)). Exact lexicographic search (DFS over beta in increasing
    order, then the least alpha_j for each j, which are independent given beta).
    scan_cap bounds the alpha scan for huge p; if it is hit the search raises rather
    than return a possibly non-least answer."""
    g = coset_generator(p, kappa) if g is None else g
    cs = Cos(p, kappa, g)
    beta = [0]*kappa

    def least_alpha(j):
        lim = p if scan_cap is None else min(p, scan_cap)
        for t in range(lim):
            if all(cs.ok(t+beta[i], -(i+j)) for i in range(kappa)):
                return t
        if lim < p:
            raise RuntimeError("alpha scan cap hit")
        return None

    def dfs(i):
        if i == kappa:
            al = [1]
            for j in range(1, kappa):
                t = least_alpha(j)
                if t is None:
                    return None
                al.append(t)
            return al
        for t in range(p):
            if cs.ok(1+t, -i):                    # condition (i, j = 0): 1 + beta_i
                beta[i] = t
                r = dfs(i+1)
                if r is not None:
                    return r
        return None
    al = dfs(1)
    if al is None:
        return None
    return tuple(al), tuple(beta)


def contraction_bruteforce(p, kappa, g=None):
    """Independent check (small p only): enumerate all of [0,p)^(2k-2) in lex order."""
    import itertools
    g = coset_generator(p, kappa) if g is None else g
    for tup in itertools.product(range(p), repeat=2*(kappa-1)):
        beta = (0,)+tup[:kappa-1]
        alpha = (1,)+tup[kappa-1:]
        if contraction_valid(p, kappa, g, alpha, beta):
            return alpha, beta
    return None


def root_params(p, q, g):
    """Oblivious q-th root parameters: p-1 = q^S Q, e1 in [1, Q] with q e1 = 1 mod Q
    (e1 = 1 if Q = 1), z = g^Q (generates the q-Sylow subgroup), wq = z^(q^(S-1))."""
    S, Q = q_adic(p, q)
    e1 = 1 if Q == 1 else pow(q, -1, Q)
    if e1 == 0:
        e1 = Q
    z = pow(g, Q, p)
    wq = pow(z, q**(S-1), p)
    return {"q": q, "S": S, "Q": Q, "e1": e1, "z": z, "wq": wq}


_CONST_CACHE = {}


def kappa_constants(p, d, contraction=None, need_contraction=True):
    """Constants of report Section 1 (cached; callers must not mutate the result)."""
    key = (p, d, None if contraction is None else (tuple(contraction[0]), tuple(contraction[1])),
           need_contraction)
    if key not in _CONST_CACHE:
        _CONST_CACHE[key] = _kappa_constants(p, d, contraction, need_contraction)
    return _CONST_CACHE[key]


def _kappa_constants(p, d, contraction=None, need_contraction=True):
    kappa = kappa_of(p, d)
    if kappa < 2:
        raise ValueError("kappa_d = gcd(d, p-1) must be >= 2 (kappa = 1: rees_coherent_sde)")
    g = coset_generator(p, kappa)
    cs = Cos(p, kappa, g)
    if contraction is None and not need_contraction:
        return {"kappa": kappa, "g": g, "h": cs.h, "omega": cs.omega, "alpha": None,
                "beta": None, "u": bezout_exponent_kappa(p, d),
                "roots": [root_params(p, q, g) for q in prime_factors(kappa)]}
    if contraction is None:
        contraction = canonical_contraction(p, kappa, g, scan_cap=None if p < 10**6 else 10**5)
        if contraction is None:
            raise ValueError(f"p = {p} lies in E_2({kappa}): no two-level contraction")
    alpha, beta = contraction
    assert contraction_valid(p, kappa, g, alpha, beta)
    return {"kappa": kappa, "g": g, "h": cs.h, "omega": cs.omega, "alpha": tuple(alpha),
            "beta": tuple(beta), "u": bezout_exponent_kappa(p, d),
            "roots": [root_params(p, q, g) for q in prime_factors(kappa)]}


# ====================================================================== references

def least_root_table(p, kappa):
    """rho(x) = least r in [0, p) with r^kappa = x, for every kappa-th power x (incl. 0)."""
    tab = {}
    for r in range(p):
        tab.setdefault(pow(r, kappa, p), r)
    return tab


def canonical_witness_kappa(p, cols, d, contraction=None):
    """Reference from the DEFINITION (report Section 1), paper-faithful. cols: M tuples
    in F_p^a. Returns dict with s, x, K, istar (x[istar] = 1, report Theorem 2)."""
    C = kappa_constants(p, d, contraction)
    kappa, alpha, beta, u = C["kappa"], C["alpha"], C["beta"], C["u"]
    cs = Cos(p, kappa, C["g"])
    a = len(cols[0])
    M = columns(a)
    assert len(cols) == M
    offs = block_offsets(a)
    V, Y, D, J = [], [], [], []
    K = yprime = None
    for k in range(a+1):
        blk = [list(cols[offs[k]+i]) for i in range(a+1-k)]
        j, y = first_dependency(p, V+blk)
        assert j >= k
        delta = y[k:]
        vnew = [sum(beta[cs(dl)]*dl*bl[r] for dl, bl in zip(delta, blk) if dl % p) % p
                for r in range(a)]
        Y.append(y)
        D.append(delta)
        J.append(j)
        fd = first_dependency(p, V+[vnew])
        if fd is not None:
            assert fd[0] == k
            K, yprime = k, fd[1]
            break
        V.append(vnew)
    x = [0]*M
    for i, dl in enumerate(D[K]):
        if dl:
            x[offs[K]+i] = dl*(1+beta[cs(dl)]) % p
    tau = [(Y[K][l]+yprime[l]) % p for l in range(K)]     # tau[l-1] <-> v_l
    for l in range(K, 0, -1):
        zeta = tau[l-1]
        if zeta == 0:
            continue
        n = cs(zeta)
        for i, dl in enumerate(D[l-1]):
            if dl:
                x[offs[l-1]+i] = zeta*dl*(alpha[n]+beta[cs(dl)]) % p
        for j in range(1, l):
            tau[j-1] = (tau[j-1]+zeta*alpha[n]*Y[l-1][j-1]) % p
    tab = least_root_table(p, kappa)
    s = [pow(tab[xi], u, p) for xi in x]
    return {"s": s, "x": x, "K": K, "istar": offs[K]+J[K]-K, "y_prime_nonzero": any(yprime[:K])}


def check_witness(p, cols, d, s):
    a = len(cols[0])
    if not any(s) or any(not 0 <= v < p for v in s):
        return False
    s = [int(v) for v in s]
    return all(sum(pow(si, d, p)*int(c[r]) for si, c in zip(s, cols)) % p == 0 for r in range(a))


def canonical_witness_kappa_batch(p, A, d, contraction=None):
    """Vectorised reference: A (N, a, M). Returns (s (N, M), x (N, M), K (N,))."""
    C = kappa_constants(p, d, contraction)
    kappa, alpha, beta, u = C["kappa"], np.array(C["alpha"]), np.array(C["beta"]), C["u"]
    A = np.array(A, dtype=np.int64) % p
    N, a, M = A.shape
    assert M == columns(a)
    inv = np.array([0]+[pow(t, -1, p) for t in range(1, p)], dtype=np.int64)
    cs = Cos(p, kappa, C["g"])
    cos = np.array([0]+[cs(t) for t in range(1, p)], dtype=np.int64)   # cos(0) := 0, masked
    Bt = beta[cos] * (np.arange(p) != 0)                                # beta_{cos(y)}, 0 at y = 0
    At = alpha[cos]
    offs = block_offsets(a)
    V = np.zeros((N, a, 0), dtype=np.int64)
    Y, D, YP = [], [], []
    K = np.full(N, -1, dtype=np.int64)
    for k in range(a+1):
        blk = A[:, :, offs[k]:offs[k]+a+1-k]
        _, y = _fd_batch(p, np.concatenate([V, blk], axis=2), inv)
        delta = y[:, k:]
        bd = delta*Bt[delta] % p
        vnew = np.einsum("nri,ni->nr", blk, bd) % p
        js2, y2 = _fd_batch(p, np.concatenate([V, vnew[:, :, None]], axis=2), inv)
        stop = (K < 0) & (js2 == k)
        K[stop] = k
        Y.append(y)
        D.append(delta)
        YP.append(y2)
        V = np.concatenate([V, vnew[:, :, None]], axis=2)
    assert np.all(K >= 0)
    x = np.zeros((N, M), dtype=np.int64)
    tau = np.zeros((N, a), dtype=np.int64)
    for k in range(a+1):
        sel = K == k
        dk = D[k][sel]
        x[sel, offs[k]:offs[k]+a+1-k] = dk*(1+Bt[dk]) % p
        for l in range(k):
            tau[sel, l] = (Y[k][sel, l]+YP[k][sel, l]) % p
    for l in range(a, 0, -1):
        zeta = tau[:, l-1].copy()
        za = zeta*At[zeta] % p                       # zeta alpha_{cos zeta} (0 at zeta = 0)
        dl = D[l-1]
        sl = slice(offs[l-1], offs[l-1]+a+2-l)
        x[:, sl] = (x[:, sl]+za[:, None]*dl % p+zeta[:, None]*(dl*Bt[dl] % p)) % p
        for j in range(1, l):
            tau[:, j-1] = (tau[:, j-1]+za*Y[l-1][:, j-1]) % p
    tab = least_root_table(p, kappa)
    roots = np.array([tab.get(t, -1) for t in range(p)], dtype=np.int64)
    assert np.all(roots[x] >= 0), "some weight is not a kappa-th power"
    powu = np.array([pow(t, u, p) for t in range(p)], dtype=np.int64)
    return powu[roots[x]], x, K


# ====================================================================== the circuit

class CoherentSDEKappa(CoherentSDEK2):
    """Permutation circuit for (p, a, d), kappa = gcd(d, p-1) >= 2, p not in E_2(kappa).
    Layout: L[c][r] input registers (column c, row r), S[c] outputs, the rest workspace.
    mutate: test hooks {"alpha": tuple, "beta": tuple, "tau1": c, "tau2": c, "out": c,
    "omega_min": bool (skip the least-root normalisation)}."""

    def __init__(self, p, a, d, mutate=None, contraction=None, stop="power"):
        if p < 3 or not is_prime(p):
            raise ValueError("p must be an odd prime")
        if a < 1:
            raise ValueError("a >= 1")
        if stop not in ("power", "general"):
            raise ValueError("stop must be 'power' (Lemma 4') or 'general'")
        self.stop_mode = stop
        self.p, self.a, self.d = p, a, d
        C = kappa_constants(p, d, contraction)
        self.const = C
        self.kappa, self.g, self.h, self.omega = C["kappa"], C["g"], C["h"], C["omega"]
        self.u = C["u"]
        self.mutate = mutate or {}
        self.alpha = tuple(self.mutate.get("alpha", C["alpha"]))
        self.beta = tuple(self.mutate.get("beta", C["beta"]))
        self.M = M = columns(a)
        self.offs = block_offsets(a)
        self.b = b = nbits(p)
        self.nw = 0
        self.free, self.free_bits = [], []
        self.stage_wires = {}
        self.L = [[self._fresh_reg() for _ in range(a)] for _ in range(M)]
        self.S = [self._fresh_reg() for _ in range(M)]
        self.anc = Anc(self._fresh(anc_size(b)), b)
        self.tmp = self._fresh(max(0, b-2, a-1))
        self.n_fd = []
        F = self._forward()
        Cs = self._copy_stage()
        self.F, self.C = F, Cs
        self.prog = Prog(F+Cs+F.inverse())
        self.io_wires = {w for col in self.L for r in col for w in r} | {w for r in self.S for w in r}

    # ---------------------------------------------------------------- blocks
    def _class_flags(self, P, y):
        """Flags f[nu-1] ^= [cos(y) = nu], nu = 1..kappa-1 (y^h == omega^nu; y = 0 sets none)."""
        p, kappa = self.p, self.kappa
        flags = [self._fresh(1)[0] for _ in range(kappa-1)]

        def sink(PP, reg):
            for nu in range(1, kappa):
                self._eq_const_into(PP, reg, pow(self.omega, nu, p), flags[nu-1])
        self._pow_copy(P, y, self.h, sink)
        return flags

    def _less_into(self, P, x, y, out):
        """out ^= [x < y] for b-bit words (x, y restored; uses the arithmetic ancillas e, c0)."""
        sub_ext(P, y, x, self.anc.e, self.anc.c0)      # (x, e) -= y: e = sign = [x < y]
        P.cx(self.anc.e, out)
        add_ext(P, y, x, self.anc.e, self.anc.c0)

    # ---------------------------------------------------------------- forward pass F
    def _forward(self):
        p, a, kappa = self.p, self.a, self.kappa
        alpha, beta, mut = self.alpha, self.beta, self.mutate
        F = Prog()
        V = []
        run = self._fresh(1)[0]
        F.x(run)
        Zs, Z2s, Ds, BDs, Fk = [], [], [], [], []
        for k in range(a+1):
            w0 = self.nw
            blk = [self.L[self.offs[k]+i] for i in range(a+1-k)]
            dep, Z = self._fd(F, V+blk, a)
            D, BD, NQ = [], [], []
            for i in range(a+1-k):
                dr = self._fresh_reg()
                self._scaled(F, dr, Z[k+i], -1)                      # delta_i = -Z = y
                fl = self._class_flags(F, dr)
                breg = self._fresh_reg()                             # beta_{cos delta_i}
                for nu in range(1, kappa):
                    self._load_const(F, breg, beta[nu] % p, fl[nu-1])
                bd = self._fresh_reg()
                self._product(F, bd, dr, breg, 1)                    # bd = beta_{cos delta} delta
                D.append(dr)
                BD.append(bd)
                if self.stop_mode == "power":
                    nq = self._fresh(1)[0]                           # nq_i = [delta_i not in P u 0]
                    for f in fl:
                        F.cx(f, nq)                                  # class flags are one-hot
                    NQ.append(nq)
            vnew = [self._fresh_reg() for _ in range(a)]
            for i in range(a+1-k):
                for r in range(a):
                    self._product(F, vnew[r], BD[i], blk[i][r], 1)
            if self.stop_mode == "general":
                dep2, Z2 = self._fd(F, V+[vnew], a)                  # stop test: v_{k+1} in U_k
                stop = dep2[k]
            else:
                # report Lemma 4': v_{k+1} in U_k <=> every nonzero delta_i lies in P
                stop = self._fresh(1)[0]
                for f in NQ:
                    F.x(f)
                self._and_into(F, NQ, stop)
                for f in NQ:
                    F.x(f)
                Z2 = None
            fk = self._fresh(1)[0]
            F.ccx(run, stop, fk)
            rn = self._fresh(1)[0]
            F.cx(run, rn)
            F.cx(fk, rn)
            run = rn
            Zs.append(Z)
            Z2s.append(Z2)
            Ds.append(D)
            BDs.append(BD)
            Fk.append(fk)
            V.append(vnew)
            self.stage_wires[("round", k)] = self.nw-w0
        self.Fk, self.Ds = Fk, Ds
        # tau_l = y^(K)_{l-1} + y'^(K)_{l-1} = -Z_K[l-1] - Z2_K[l-1]
        w0 = self.nw
        general = self.stop_mode == "general"
        tau = [self._fresh_reg() for _ in range(a)]
        for l in range(1, a+1):
            A1 = self._fresh_reg()
            A2 = self._fresh_reg() if general else None
            for k in range(l, a+1):
                for qs, qd in zip(Zs[k][l-1], A1):
                    F.ccx(Fk[k], qs, qd)
                if general:
                    for qs, qd in zip(Z2s[k][l-1], A2):
                        F.ccx(Fk[k], qs, qd)
            self._scaled(F, tau[l-1], A1, mut.get("tau1", -1))
            if general:                                  # Lemma 4': this term is 0 on every input
                self._scaled(F, tau[l-1], A2, mut.get("tau2", -1))
        self.stage_wires["tau"] = self.nw-w0
        # back substitution l = a..1: za_l = zeta_l alpha_{cos zeta_l}; tau_j += za_l y^(l-1)_{j-1}
        w0 = self.nw
        ZA = [None]*(a+2)
        for l in range(a, 0, -1):
            zeta = tau[l-1]
            fl = self._class_flags(F, zeta)
            areg = self._fresh_reg()
            F.x(areg[0])                                             # alpha_0 = 1 by default
            for nu in range(1, kappa):
                self._load_const(F, areg, 1 ^ (alpha[nu] % p), fl[nu-1])
            za = self._fresh_reg()
            self._product(F, za, zeta, areg, 1)
            ZA[l] = za
            for j in range(1, l):
                self._product(F, tau[j-1], za, Zs[l-1][j-1], -1)
        self.tau, self.ZA = tau, ZA
        self.stage_wires["backsub"] = self.nw-w0
        # weights x_i = (F_k + za_{k+1}) delta_i + (F_k + zeta_{k+1}) bd_i on block k
        w0 = self.nw
        X = [self._fresh_reg() for _ in range(self.M)]
        z0 = self._fresh_reg()
        for k in range(a+1):
            cols = [self.offs[k]+i for i in range(a+1-k)]
            if k < a:
                ga, gz = ZA[k+1], tau[k]
            else:
                ga = gz = z0
            F.cx(Fk[k], ga[0])          # F_k = 1 only at k = K, where za_{K+1} = zeta_{K+1} = 0
            for i, col in enumerate(cols):
                self._product(F, X[col], ga, Ds[k][i], 1)
            if not general:
                # Lemma 4': bd_i = 0 on block K, so the F_k (1 + beta) term is F_k delta_i
                F.cx(Fk[k], ga[0])
                if k < a:
                    for i, col in enumerate(cols):
                        self._product(F, X[col], gz, BDs[k][i], 1)
                continue
            if gz is not ga:
                F.cx(Fk[k], ga[0])
                F.cx(Fk[k], gz[0])
            for i, col in enumerate(cols):
                self._product(F, X[col], gz, BDs[k][i], 1)
            F.cx(Fk[k], gz[0])
        self.X = X
        self.stage_wires["weights"] = self.nw-w0
        self.forward_wires = self.nw
        return F

    # ---------------------------------------------------------------- copy stage
    def _qroot_chain(self, P, x, rp, used, bits):
        """Append to P an oblivious q-th root of x (x a q-th power or 0); returns the
        register of the root r (r^q = x). Generalised Tonelli-Shanks / AMM digits."""
        p, q, S, e1, z, wq = self.p, rp["q"], rp["S"], rp["e1"], rp["z"], rp["wq"]
        if e1 == 1:
            r, aa = x, None
        else:
            aa = self._pow_reg(P, x, e1-1, used)
            r = self._reg()
            used.append(r)
            self._product(P, r, aa, x, 1)                    # r = x^e1
        if S < 2:
            return r
        if aa is None:
            t = self._pow_reg(P, x, q-1, used)               # t = x^(q e1 - 1) = x^(q-1)
        else:
            rq = self._pow_reg(P, r, q-1, used)
            t = self._reg()
            used.append(t)
            self._product(P, t, rq, aa, 1)                   # t = r^(q-1) x^(e1-1) = x^(q e1 - 1)
        zinv = pow(z, -1, p)
        for j in range(S-1):
            uu = t
            for _ in range(S-2-j):
                uu = self._pow_reg(P, uu, q, used)           # t^(q^(S-2-j)) in mu_q
            fl = []
            for nu in range(1, q):
                f = self._bit()
                bits.append(f)
                self._eq_const_into(P, uu, pow(wq, nu, p), f)
                fl.append(f)
            if j < S-2:
                w = self._reg()
                used.append(w)
                P.x(w[0])
                for nu in range(1, q):
                    self._load_const(P, w, 1 ^ pow(zinv, nu*q**(j+1), p), fl[nu-1])
                nt = self._reg()
                used.append(nt)
                self._product(P, nt, t, w, 1)                # t <- t z^(-q^(j+1) k_j)
                t = nt
            w2 = self._reg()
            used.append(w2)
            P.x(w2[0])
            for nu in range(1, q):
                self._load_const(P, w2, 1 ^ pow(zinv, nu*q**j, p), fl[nu-1])
            nr = self._reg()
            used.append(nr)
            self._product(P, nr, r, w2, 1)                   # r <- r z^(-q^j k_j)
            r = nr
        return r

    def _root_chain(self, x):
        """Prog computing rho(x) = least kappa-th root of x (x in P u {0})."""
        p, kappa = self.p, self.kappa
        P, used, bits = Prog(), [], []
        r = x
        for rp in self.const["roots"]:
            r = self._qroot_chain(P, r, rp, used, bits)
        c0 = self._reg()
        used.append(c0)
        self._copy(P, r, c0)
        if not self.mutate.get("omega_min"):
            for t in range(1, kappa):
                ct = self._reg()
                used.append(ct)
                self._scaled(P, ct, r, pow(self.omega, t, p))   # ct = r omega^t
                f = self._bit()
                bits.append(f)
                self._less_into(P, ct, c0, f)                    # f = [ct < c0]
                for qa, qb in zip(c0, ct):
                    self._cswap(P, f, qa, qb)                    # c0 = min
        return P, c0, used, bits

    def _copy_stage(self):
        C = Prog()
        for i in range(self.M):
            P, r, used, bits = self._root_chain(self.X[i])
            res = self._pow_reg(P, r, self.u, used)
            C += P
            self._scaled(C, self.S[i], res, self.mutate.get("out", 1))
            C += P.inverse()
            for reg in reversed(used):
                self._release(reg)
            for q in reversed(bits):
                self.free_bits.append(q)
        return C


# ====================================================================== closed forms

def _ell(n):
    return chain_length(n) if n >= 2 else 0


def qroot_products(rp):
    """Products of one oblivious q-th root (compute only)."""
    q, S, e1 = rp["q"], rp["S"], rp["e1"]
    head = 0 if e1 == 1 else _ell(e1-1)+1
    if S < 2:
        return head
    head += _ell(q-1) if e1 == 1 else _ell(q-1)+1
    return head+_ell(q)*(S-1)*(S-2)//2+(S-2)+(S-1)


def root_products(C):
    return sum(qroot_products(rp) for rp in C["roots"])


def closed_form_macros(p, a, d, contraction=None, stop="power"):
    """Macro counts of F + C + F^-1 (report Section 3). With I = ell(p-2), Lh = ell(h),
    h = (p-1)/kappa, fd(R, n) = fd_products:
      n_F = (a+1) fd(a, a+1) [delta]  (+ sum_{n=1}^{a+1} fd(a, n) [stop test], general only)
            + 2 Lh (M + a) [coset flags of the M deltas and a zetas] + M [bd] + a M [v]
            + a [za] + a(a-1)/2 [back substitution] + 2M - [power] [weights];
      copy: 2 M (T + ell(u)), T = products of the kappa-th root chain;
      add_scaled: 2(M + a + a[general]) [delta, tau] + 2 M (kappa-1) [root candidates] + M."""
    C = kappa_constants(p, d, contraction)
    kappa = C["kappa"]
    M = columns(a)
    gen = stop == "general"
    Ip, Lh = _ell(p-2), _ell(C["h"])
    nF = (a+1)*fd_products(a, a+1, Ip)
    if gen:
        nF += sum(fd_products(a, n, Ip) for n in range(1, a+2))
    nF += 2*Lh*(M+a)+M+a*M+a+a*(a-1)//2+2*M-(0 if gen else 1)
    T = root_products(C)
    return {"kappa": kappa, "I_p": Ip, "L_h": Lh, "T_root": T, "u": C["u"], "products_F": nF,
            "add_product": 2*nF+2*M*(T+_ell(C["u"])),
            "add_scaled": 2*(M+a+(a if gen else 0))+2*M*(kappa-1)+M}


def closed_form_products_poly(a, Ip, Lh, T, eu, stop="power"):
    """#add_product as an explicit polynomial (report Section 3): 2 n_F + 2 M (T + eu),
    M = (a+1)(a+2)/2, with
      power:   n_F = (a^4 + 4a^3 + 14a^2 + 17a + 4)/2 + Ip (2a^2 + 2a) + Lh (a^2 + 5a + 2),
      general: n_F = (4a^4 + 16a^3 + 53a^2 + 71a + 18)/6 + Ip (3a^2 + 5a) + Lh (a^2 + 5a + 2)."""
    M = (a+1)*(a+2)//2
    if stop == "general":
        n6 = 4*a**4+16*a**3+53*a**2+71*a+18
        assert n6 % 6 == 0
        nF = n6//6+Ip*(3*a*a+5*a)+Lh*(a*a+5*a+2)
    else:
        n2 = a**4+4*a**3+14*a**2+17*a+4
        assert n2 % 2 == 0
        nF = n2//2+Ip*(2*a*a+2*a)+Lh*(a*a+5*a+2)
    return 2*nF+2*M*(T+eu)


def _ladder(b):
    """CCX of one b-wire AND ladder (equality test / OR flag)."""
    return 1 if b == 2 else 2*b-3


def root_nonmacro_ccx(C, b):
    """Non-macro CCX of one root chain (compute only): the digit equality tests
    (q-1 per round, S_q - 1 rounds per prime q) and, for the least-root selection,
    kappa-1 comparators (4b: two Cuccaro adders) and Fredkin swaps (b)."""
    s = sum((rp["S"]-1)*(rp["q"]-1)*_ladder(b) for rp in C["roots"] if rp["S"] >= 2)
    return s+(C["kappa"]-1)*5*b


def closed_form_toffoli(p, a, d, contraction=None, stop="power"):
    """Exact CCX count of F + C + F^-1:
      2 * [ (a+1) fdx(a, a+1) + (M+a)(kappa-1) lad [coset equality tests]
            + power:   sum_k (and(a+1-k) + 1) [stop flags] + b a(a+1)/2 [tau select]
            + general: sum_{n=1}^{a+1} fdx(a, n) + (a+1) + b a(a+1) ]
      + 2 M root_nonmacro_ccx + (40b^2+2b) #add_product + add_scaled CCX (by coefficient),
    fdx = fd_nonmacro_ccx (OR ladders, prefix chain, Fredkins, loads, selection)."""
    b = nbits(p)
    C = kappa_constants(p, d, contraction)
    kappa = C["kappa"]
    gen = stop == "general"
    mc = closed_form_macros(p, a, d, contraction, stop)
    lad = _ladder(b)
    M = columns(a)
    nonmacro = (a+1)*fd_nonmacro_ccx(a, a+1, b)+(M+a)*(kappa-1)*lad
    if gen:
        nonmacro += sum(fd_nonmacro_ccx(a, n, b) for n in range(1, a+2))+(a+1)+b*a*(a+1)
    else:
        nonmacro += sum(_and_ccx(a+1-k)+1 for k in range(a+1))+b*a*(a+1)//2
    sc = (2*(M+a+(a if gen else 0))*formula_counts(p, p-1)["add_scaled_ccx"]
          + M*formula_counts(p, 1)["add_scaled_ccx"]
          + 2*M*sum(formula_counts(p, pow(C["omega"], t, p))["add_scaled_ccx"] for t in range(1, kappa)))
    return 2*nonmacro+2*M*root_nonmacro_ccx(C, b)+mc["add_product"]*(40*b*b+2*b)+sc


def fd_qubits(R, n, b):
    """Fresh wires of one first-dependency machine on n <= R+1 columns in F_p^R: copy
    R n b, act 1, per step k < min(n, R): 3(R-k) flag bits (nz, sel, chain, a1) and
    (R+2) b (uinv, w, wi, R-1 multipliers), Z n b. (Normalised rows and the Fermat
    chain come from the shared pool.)"""
    s = R*n*b+1+n*b
    for k in range(min(n, R)):
        s += 3*(R-k)+(R+2)*b
    return s


def copy_pool_registers(C):
    """Pool registers held at once by one copy-stage chain: per prime q, the head
    (ell(e1-1) + 1 if e1 > 1; ell(q-1) [+1] for t if S_q >= 2) and per round j the
    (S_q-2-j) ell(q) powering registers plus 2 (constant, product) per multiplication;
    then c0, kappa-1 candidates and ell(u) for the power."""
    n = 0
    for rp in C["roots"]:
        q, S, e1 = rp["q"], rp["S"], rp["e1"]
        n += 0 if e1 == 1 else _ell(e1-1)+1
        if S >= 2:
            n += _ell(q-1) if e1 == 1 else _ell(q-1)+1
            n += sum(_ell(q)*(S-2-j)+(2 if j < S-2 else 0)+2 for j in range(S-1))
    return n+1+(C["kappa"]-1)+_ell(C["u"])


def pool_registers(p, C):
    """Peak size of the shared register pool: max over the local demands (a Fermat
    chain I_p, a normalisation 1, a coset-test chain ell(h), a copy-stage chain)."""
    return max(1, _ell(p-2), _ell(C["h"]), copy_pool_registers(C))


def closed_form_qubits(p, a, d, contraction=None, stop="power"):
    """Peak qubits = all allocated wires:
      IO (a+1) M b; arithmetic ancillas 3b+5; ladder temporaries max(0, b-2, a-1); run 1;
      first dependencies (a+1) fd_qubits(a, a+1) (+ sum_n fd_qubits(a, n), general);
      per round k: (a+1-k)(3b + kappa-1 + [power]) (delta, flags, beta_cos, bd, nq)
        + a b (v) + 2 (F_k, run) + [power] (stop bit);
      tau a b (1 + 2[general]... ) : tau and A1 (and A2, general);
      back substitution a (kappa-1 + 2b); weights (M+1) b;
      pool pool_registers b; copy-stage flag bits sum_q (S_q-1)(q-1) + kappa-1."""
    b = nbits(p)
    C = kappa_constants(p, d, contraction)
    kappa = C["kappa"]
    gen = stop == "general"
    pw = 0 if gen else 1
    M = columns(a)
    q = (a+1)*M*b+3*b+5+max(0, b-2, a-1)+1
    q += (a+1)*fd_qubits(a, a+1, b)
    if gen:
        q += sum(fd_qubits(a, n, b) for n in range(1, a+2))
    q += sum((a+1-k)*(3*b+kappa-1+pw)+a*b+2+pw for k in range(a+1))
    q += (3 if gen else 2)*a*b
    q += a*(kappa-1+2*b)
    q += (M+1)*b
    q += pool_registers(p, C)*b
    q += sum((rp["S"]-1)*(rp["q"]-1) for rp in C["roots"] if rp["S"] >= 2)+(kappa-1)
    return q



# ====================================================================== checks

def check_circuit(circ, A, gates=None):
    p, a, d, M = circ.p, circ.a, circ.d, circ.M
    N = A.shape[0]
    sim = BitSim(circ.nw, N)
    for c in range(M):
        for r in range(a):
            sim.load(circ.L[c][r], A[:, r, c])
    gates = circ.flatten() if gates is None else gates
    t0 = time.time()
    sim.run(gates)
    dt = time.time()-t0
    s = np.stack([sim.read(circ.S[c]) for c in range(M)], axis=1)
    ref, x, K = canonical_witness_kappa_batch(p, A, d, (circ.const["alpha"], circ.const["beta"]))
    inputs_ok = all(np.array_equal(sim.read(circ.L[c][r]), A[:, r, c])
                    for c in range(M) for r in range(a))
    work_clean = not any(sim.wire_nonzero(w) for w in range(circ.nw) if w not in circ.io_wires)
    sd = np.array([pow(t, d, p) for t in range(p)], dtype=np.int64)[np.minimum(s, p-1)]
    eq_ok = bool(np.all(np.einsum("nrc,nc->nr", A, sd) % p == 0))
    return {"p": p, "a": a, "d": d, "kappa": circ.kappa, "u": circ.u, "M": M, "inputs": int(N),
            "gates": len(gates), "qubits": circ.nw,
            "output_equals_canonical": bool(np.array_equal(s, ref)),
            "inputs_restored": inputs_ok, "workspace_clean": work_clean,
            "witness_nonzero": bool(np.all(s.any(axis=1))), "equation_holds": eq_ok,
            "canonical_padding_free": bool(np.all(s < p)),
            "K_hist": np.bincount(K, minlength=a+1).tolist(), "sim_seconds": round(dt, 3)}


CHECK_KEYS = ("output_equals_canonical", "inputs_restored", "workspace_clean", "witness_nonzero",
              "equation_holds", "canonical_padding_free")


def exhaustive_check(p, a, d):
    circ = CoherentSDEKappa(p, a, d)
    return check_circuit(circ, all_inputs(p, a))


def sampled_check(p, a, d, n=4096, seed=0):
    circ = CoherentSDEKappa(p, a, d)
    return check_circuit(circ, structured_inputs(p, a, n, seed))


def exhaustive_check_chunked(p, a, d, chunk=1 << 20, log=print):
    circ = CoherentSDEKappa(p, a, d)
    gates = circ.flatten()
    N = p**(a*columns(a))
    agg = {k: True for k in CHECK_KEYS}
    K = np.zeros(a+1, dtype=np.int64)
    t0 = time.time()
    for st in range(0, N, chunk):
        r = check_circuit(circ, input_range(p, a, st, min(N, st+chunk)), gates)
        for k in CHECK_KEYS:
            agg[k] &= r[k]
        K += np.array(r["K_hist"])
        log(json.dumps({"done": min(N, st+chunk), "of": N, "ok": all(agg.values()),
                        "elapsed": round(time.time()-t0, 1)}), flush=True)
    return {"p": p, "a": a, "d": d, "M": circ.M, "inputs": int(N), "gates": len(gates),
            "qubits": circ.nw, **agg, "K_hist": K.tolist(), "seconds": round(time.time()-t0, 1)}


def rref_representatives(p, a, n):
    """One a x n matrix per row space of dimension <= a in F_p^n (the RREF, padded by zero
    rows), as an array (N, a, n). The canonical witness depends only on the row space
    (report Lemma 5), so these cover every input up to GL_a."""
    import itertools
    reps = []
    for r in range(a+1):
        for piv in itertools.combinations(range(n), r):
            free = [(i, c) for i in range(r) for c in range(piv[i]+1, n) if c not in piv]
            for vals in itertools.product(range(p), repeat=len(free)):
                Mx = np.zeros((a, n), dtype=np.int64)
                for i, c in enumerate(piv):
                    Mx[i, c] = 1
                for (i, c), v in zip(free, vals):
                    Mx[i, c] = v
                reps.append(Mx)
    return np.array(reps, dtype=np.int64)


def rref_count(p, a, n):
    """Number of subspaces of F_p^n of dimension <= a (Gaussian binomials)."""
    def gb(n, k):
        num = den = 1
        for i in range(k):
            num *= p**(n-i)-1
            den *= p**(i+1)-1
        return num//den
    return sum(gb(n, r) for r in range(a+1))


def rref_iter_chunks(p, a, n, chunk):
    """Stream the RREF representatives in chunks (memory-bounded)."""
    import itertools
    buf = []
    for r in range(a+1):
        for piv in itertools.combinations(range(n), r):
            free = [(i, c) for i in range(r) for c in range(piv[i]+1, n) if c not in piv]
            base = np.zeros((a, n), dtype=np.int64)
            for i, c in enumerate(piv):
                base[i, c] = 1
            nf = len(free)
            tot = p**nf
            for st in range(0, tot, chunk):
                idx = np.arange(st, min(tot, st+chunk), dtype=np.int64)
                B = np.repeat(base[None], len(idx), axis=0)
                for t, (i, c) in enumerate(free):
                    B[:, i, c] = idx % p
                    idx = idx//p
                buf.append(B)
                if sum(len(x) for x in buf) >= chunk:
                    yield np.concatenate(buf)
                    buf = []
    if buf:
        yield np.concatenate(buf)


def rref_check(p, a, d, chunk=1 << 19, log=print):
    """The circuit on every RREF representative (one per row space of dim <= a)."""
    circ = CoherentSDEKappa(p, a, d)
    gates = circ.flatten()
    agg = {k: True for k in CHECK_KEYS}
    K = np.zeros(a+1, dtype=np.int64)
    done, t0 = 0, time.time()
    for A in rref_iter_chunks(p, a, circ.M, chunk):
        r = check_circuit(circ, A, gates)
        for k in CHECK_KEYS:
            agg[k] &= r[k]
        K += np.array(r["K_hist"])
        done += len(A)
        log(json.dumps({"done": done, "of": rref_count(p, a, circ.M), "ok": all(agg.values()),
                        "elapsed": round(time.time()-t0, 1)}), flush=True)
    return {"p": p, "a": a, "d": d, "M": circ.M, "row_spaces": done,
            "expected": rref_count(p, a, circ.M), "gates": len(gates), "qubits": circ.nw, **agg,
            "K_hist": K.tolist(), "seconds": round(time.time()-t0, 1)}


def count_row(p, a, d, stop="power"):
    circ = CoherentSDEKappa(p, a, d, stop=stop)
    c = circ.counts()
    m = closed_form_macros(p, a, d, stop=stop)
    ct = closed_form_toffoli(p, a, d, stop=stop)
    cq = closed_form_qubits(p, a, d, stop=stop)
    return {"p": p, "b": circ.b, "a": a, "d": d, "stop": stop, "kappa": circ.kappa, "M": circ.M,
            "alpha": circ.const["alpha"], "beta": circ.const["beta"], "g": circ.g, **c,
            **{"closed_" + k: v for k, v in m.items()},
            "closed_toffoli": ct, "closed_qubits": cq,
            "toffoli_matches": c["gates"].get("ccx", 0) == ct,
            "macros_match": (c["add_product"], c["add_scaled"]) == (m["add_product"], m["add_scaled"]),
            "qubits_match": c["qubits"] == cq}


def root_circuit(p, d):
    """The copy stage alone on one weight register x (M = 1): |x>|0> -> |x>|rho(x)^u>."""
    c = CoherentSDEKappa.__new__(CoherentSDEKappa)
    c.p, c.d = p, d
    c.const = C = kappa_constants(p, d, need_contraction=False)
    c.kappa, c.g, c.h, c.omega, c.u = C["kappa"], C["g"], C["h"], C["omega"], C["u"]
    c.M, c.mutate = 1, {}
    c.b = b = nbits(p)
    c.nw, c.free, c.free_bits = 0, [], []
    c.X, c.S = [c._fresh_reg()], [c._fresh_reg()]
    c.anc = Anc(c._fresh(anc_size(b)), b)
    c.tmp = c._fresh(max(0, b-2))
    c.prog = c._copy_stage()
    c.io_wires = set(c.X[0]) | set(c.S[0])
    return c


def root_check(p, d):
    """Exhaustive over every x in P u {0}: output (least kappa-th root)^u, x restored,
    workspace 0."""
    c = root_circuit(p, d)
    tab = least_root_table(p, c.kappa)
    xs = np.array(sorted(tab), dtype=np.int64)
    sim = BitSim(c.nw, len(xs))
    sim.load(c.X[0], xs)
    gates = c.flatten()
    sim.run(gates)
    out = sim.read(c.S[0])
    want = np.array([pow(tab[int(t)], c.u, p) for t in xs], dtype=np.int64)
    clean = not any(sim.wire_nonzero(w) for w in range(c.nw) if w not in c.io_wires)
    return {"p": p, "d": d, "kappa": c.kappa, "S": [rp["S"] for rp in C_roots(c)],
            "powers": int(len(xs)), "gates": len(gates),
            "root_ok": bool(np.array_equal(out, want)),
            "x_restored": bool(np.array_equal(sim.read(c.X[0]), xs)), "workspace_clean": clean}


def C_roots(c):
    return c.const["roots"]


def primes_1_mod(kappa, lo, hi):
    return [q for q in range(lo, hi) if is_prime(q) and q % kappa == 1]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None)
    ap.add_argument("--chunked", default=None, help="p,a,d: chunked exhaustive check only")
    ap.add_argument("--rref", default=None, help="p,a,d: all RREF representatives")
    args = ap.parse_args()
    for flag, fn in (("chunked", exhaustive_check_chunked), ("rref", rref_check)):
        spec = getattr(args, flag)
        if spec:
            p, a, d = (int(t) for t in spec.split(","))
            r = fn(p, a, d)
            print(json.dumps(r), flush=True)
            if args.out:
                with open(args.out, "w") as f:
                    json.dump({"status": STATUS, flag: r}, f, indent=1)
            return
    res = {"status": STATUS, "contractions": [], "exhaustive": [], "sampled": [], "roots": [],
           "counts": []}
    for kappa, hi in ((2, 400), (3, 400), (4, 200), (5, 400)):
        for p in primes_1_mod(kappa, 3, hi):
            C = canonical_contraction(p, kappa)
            res["contractions"].append({"kappa": kappa, "p": p, "g": coset_generator(p, kappa),
                                        "alpha": None if C is None else C[0],
                                        "beta": None if C is None else C[1]})
        print(json.dumps({"kappa": kappa, "E2_found": [r["p"] for r in res["contractions"]
                                                      if r["kappa"] == kappa and r["alpha"] is None]}),
              flush=True)
    ex = [(p, 1, 3, "power") for p in primes_1_mod(3, 3, 110)]
    ex += [(7, 1, 9, "power"), (13, 1, 9, "power"), (31, 1, 9, "power"), (37, 1, 15, "power")]
    ex += [(p, 1, 3, "general") for p in (7, 13, 19, 31, 37)]
    ex += [(p, 1, 2, "power") for p in (3, 5, 7, 11, 13)] + [(p, 1, 4, "power") for p in (41, 61, 73)]
    for p, a, d, stop in ex:
        r = check_circuit(CoherentSDEKappa(p, a, d, stop=stop), all_inputs(p, a)) | {"stop": stop}
        print(json.dumps(r), flush=True)
        res["exhaustive"].append(r)
    smp = [(p, 2, 3) for p in (7, 13, 19, 31, 37, 43)] + [(7, 2, 9), (13, 2, 9), (7, 3, 3), (13, 3, 3),
                                                           (19, 3, 3), (7, 4, 3), (13, 4, 3), (7, 5, 3)]
    smp += [(41, 2, 4), (61, 2, 4), (211, 1, 5), (211, 2, 5), (5, 2, 2), (7, 2, 2), (5, 3, 2)]
    smp = [(p, a, d, "power") for p, a, d in smp] + [(7, 2, 3, "general"), (13, 3, 3, "general")]
    for p, a, d, stop in smp:
        c = CoherentSDEKappa(p, a, d, stop=stop)
        r = check_circuit(c, structured_inputs(p, a, 8192, seed=p*100+a*10+d)) | {"stop": stop}
        print(json.dumps(r), flush=True)
        res["sampled"].append(r)
    for p, d in [(7, 3), (13, 3), (19, 3), (37, 3), (109, 3), (163, 3), (487, 3), (1459, 3),
                 (13, 9), (31, 9), (13, 6), (37, 6), (1009, 6), (41, 4), (97, 4), (193, 4),
                 (211, 5), (31, 10)]:
        r = root_check(p, d)
        print(json.dumps(r), flush=True)
        res["roots"].append(r)
    big = [next(q for q in range(lo, 2*lo) if is_prime(q) and q % 3 == 1) for lo in (1000, 65536)]
    for p in [7, 13, 19, 37, 109, 163]+big+[2**31-1, 2**61-1]:
        for a in (1, 2, 3, 4, 8):
            for stop in ("power", "general"):
                r = count_row(p, a, 3, stop)
                print(json.dumps({k: r[k] for k in ("p", "b", "a", "M", "stop", "add_product",
                                                     "add_scaled", "qubits", "toffoli_matches",
                                                     "macros_match", "qubits_match")}
                                 | {"total": r["gates"]["total"], "ccx": r["gates"].get("ccx")}),
                      flush=True)
                res["counts"].append(r)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
