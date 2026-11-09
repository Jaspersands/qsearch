"""Coherent (reversible) SDE solve at kappa_d = 2 for the Rees HSP receiver.

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-04-rees-coherent-sde-k2.md.

At a recursion grade d with kappa_d = gcd(d, p-1) = 2 (every grade d = 2 for odd
p) the merge needs a nonzero s with sum_i s_i^d lambda_i = 0 (main.tex,
eq:sde-target), lambda_i in F_p^a. This module builds a permutation circuit
(X, CX, CCX, SWAP only) that maps

    |lambda_1..lambda_M>|0>_S|0>_work  ->  |lambda>|s(lambda)>_S|0>_work

on every canonical input, M = (a+1)(a+2)/2, where s is the CANONICAL
triangular witness of the report (Section 1): the triangular two-level solver
of prop:triangular-sde with
  * the explicit universal contraction alpha = (1, 0), beta = (0, m-1),
    m = least quadratic non-residue (report Lemma 1);
  * first dependencies (the rees_coherent_sde witness with e = 1) for every
    choice of delta and every coordinate computation;
  * the even square root rho(x) and the Bezout exponent u, s_i = rho(x_i)^u.

Construction (Bennett): F runs every round k = 0..a obliviously: a coherent
Gauss-Jordan first dependency of (v_1..v_k, block_k) (the rees_coherent_sde
machine generalised to R x n), Legendre flags by Euler's criterion, v_{k+1},
the stop flag "no delta_i is a non-residue" (report Lemma 4: equivalent to
v_{k+1} in U_k for the first-dependency delta, so no second elimination),
one-hot stop flags F_k, the coordinates tau, the back substitution with
masked alpha, and the weights x. The references below keep the
paper-faithful stop test (a second first dependency). The copy stage computes rho(x_i)^u by an oblivious
Tonelli-Shanks (fixed non-residue, S-1 rounds padded, constant multipliers
loaded under flags), adds it into S_i and uncomputes locally. Then F^-1.

Arithmetic: add_product / add_scaled of theorems/rees_circuit_arith.py
(imported, not edited). Helpers reused from theorems/rees_coherent_sde.py
(imported, not edited).

Domain: canonical words (every coordinate < p). Padding words are not
claimed. Does NOT: wire into the generated receiver, the descent (controlled
delta_s), QFT_p, oracle, noise; flip any claim gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import os
import time

import numpy as np

from theorems.rees_circuit_arith import Anc, anc_size, formula_counts
from theorems.rees_coherent_sde import (BitSim, CoherentSDE, Prog, chain_length, is_prime,
                                        macro_gate_types, nbits)

STATUS = {"status": "coherent_kappa2_sde_solve_finite_checks",
          "scope": "grades with kappa_d = gcd(d, p-1) = 2 (incl. every d = 2), triangular solver "
                   "of prop:triangular-sde at (a+1)(a+2)/2 columns",
          "coherent_receiver_implemented": False, "general_sde_implemented": False,
          "coherent_kappa2_sde_implemented": True,
          "coherent_kappa_ge3_sde_implemented": False,
          "wired_into_generated_receiver": False,
          "independent_review": False, "speedup_claim_allowed": False}


# ====================================================================== constants

def least_nonresidue(p):
    return next(x for x in range(2, p) if pow(x, (p-1)//2, p) == p-1)


def two_adic(p):
    S, Q = 0, p-1
    while Q % 2 == 0:
        S, Q = S+1, Q//2
    return S, Q


def bezout_exponent(p, d):
    """Least u >= 1 with u (d/2) = 1 mod (p-1)/2; needs gcd(d, p-1) = 2."""
    if d < 2 or math.gcd(d, p-1) != 2:
        raise ValueError("kappa_d = gcd(d, p-1) must be 2")
    h = (p-1)//2
    if h == 1:
        return 1
    return pow((d//2) % h, -1, h)


def columns(a):
    return (a+1)*(a+2)//2


def block_offsets(a):
    out, o = [], 0
    for k in range(a+1):
        out.append(o)
        o += a+1-k
    return out


def even_root(p, x):
    if x % p == 0:
        return 0
    r = next(r for r in range(p) if r*r % p == x % p)    # small p reference only
    return r if r % 2 == 0 else p-r


# ====================================================================== references

def first_dependency(p, vecs):
    """Definition-level first dependency: (j*, y) with y_{j*} = 1, sum y_i w_i = 0,
    y_i = 0 beyond j*, or None if the list is independent."""
    n = len(vecs)
    basis = []
    for j, col in enumerate(vecs):
        v = [int(x) % p for x in col]
        coef = [0]*n
        coef[j] = 1
        for piv, bv, bc in basis:
            if v[piv]:
                f = v[piv]
                v = [(x-f*y) % p for x, y in zip(v, bv)]
                coef = [(x-f*y) % p for x, y in zip(coef, bc)]
        if not any(v):
            return j, coef
        piv = next(i for i, x in enumerate(v) if x)
        inv = pow(v[piv], -1, p)
        basis.append((piv, [x*inv % p for x in v], [x*inv % p for x in coef]))
    return None


def _sqrt_any(p, x):
    """A square root of a square x (Tonelli-Shanks, reference; any root)."""
    x %= p
    if x == 0:
        return 0
    m = least_nonresidue(p)
    S, Q = two_adic(p)
    z, r, t, M = pow(m, Q, p), pow(x, (Q+1)//2, p), pow(x, Q, p), S
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt, i = tt*tt % p, i+1
        bb = pow(z, 1 << (M-i-1), p)
        r, z, t, M = r*bb % p, bb*bb % p, t*bb*bb % p, i
    return r


def rho(p, x):
    r = _sqrt_any(p, x)
    assert r*r % p == x % p
    return r if r % 2 == 0 else (p-r) % p


def canonical_witness_k2(p, cols, d):
    """Reference from the DEFINITION (report Section 1). cols: list of M tuples in
    F_p^a. Returns dict with s, x, K and istar (the column with x = 1, Theorem 3)."""
    a = len(cols[0])
    M = columns(a)
    assert len(cols) == M
    m, u = least_nonresidue(p), bezout_exponent(p, d)
    mu = m-1

    def nonres(y):
        return pow(y % p, (p-1)//2, p) == p-1

    def coef(zeta, delta):            # c(zeta, delta) = alpha_{n(zeta)} + beta_{n(delta)}
        return (0 if nonres(zeta) else 1) + (mu if nonres(delta) else 0)
    offs = block_offsets(a)
    V, Y, D, J = [], [], [], []
    K = yprime = None
    for k in range(a+1):
        blk = [list(cols[offs[k]+i]) for i in range(a+1-k)]
        j, y = first_dependency(p, V+blk)
        assert j >= k
        delta = y[k:]
        vnew = [mu*sum(dl*bl[r] for dl, bl in zip(delta, blk) if dl and nonres(dl)) % p
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
        x[offs[K]+i] = dl*coef(1, dl) % p
    tau = [(Y[K][l]+yprime[l]) % p for l in range(K)]     # tau[l-1] <-> v_l
    for l in range(K, 0, -1):
        zeta = tau[l-1]
        for i, dl in enumerate(D[l-1]):
            x[offs[l-1]+i] = zeta*dl*coef(zeta, dl) % p
        if not nonres(zeta):
            for j in range(1, l):
                tau[j-1] = (tau[j-1]+zeta*Y[l-1][j-1]) % p
    s = [pow(rho(p, xi), u, p) for xi in x]
    return {"s": s, "x": x, "K": K, "istar": offs[K]+J[K]-K}


def check_witness(p, cols, d, s):
    """The property the descent needs: s nonzero, canonical words, sum s_i^d lambda_i = 0."""
    a = len(cols[0])
    if not any(s) or any(not 0 <= v < p for v in s):
        return False
    s = [int(v) for v in s]
    return all(sum(pow(si, d, p)*int(c[r]) for si, c in zip(s, cols)) % p == 0 for r in range(a))


# ---------------------------------------------------------------- batched reference

def _fd_batch(p, W, inv):
    """W (N, R, n). Oblivious first dependency, written independently of the
    circuit. Returns (jstar (N,) with n = none, y (N, n))."""
    W = W.copy() % p
    N, R, n = W.shape
    jstar = np.full(N, n, dtype=np.int64)
    active = np.ones(N, dtype=bool)
    ar = np.arange(N)
    for k in range(min(n, R)):
        sub = W[:, k:, k] != 0
        has = sub.any(axis=1)
        jstar[active & ~has] = k
        piv = active & has
        idx = np.nonzero(piv)[0]
        r = k+sub[idx].argmax(axis=1)
        rk, rr = W[idx, k, :].copy(), W[idx, r, :].copy()
        W[idx, k, :], W[idx, r, :] = rr, rk
        W[idx, k, :] = W[idx, k, :]*inv[W[idx, k, k]][:, None] % p
        for j in range(R):
            if j != k:
                f = W[idx, j, k].copy()
                W[idx, j, :] = (W[idx, j, :]-f[:, None]*W[idx, k, :]) % p
        active = piv
    if n == R+1:
        jstar[active] = R
    y = np.zeros((N, n), dtype=np.int64)
    has = jstar < n
    y[ar[has], jstar[has]] = 1
    for i in range(min(R, n)):
        mask = has & (i < jstar)
        y[mask, i] = (-W[ar[mask], i, jstar[mask]]) % p
    return jstar, y


def canonical_witness_k2_batch(p, A, d):
    """Vectorised reference: A (N, a, M). Returns (s (N, M), x (N, M), K (N,))."""
    A = np.array(A, dtype=np.int64) % p
    N, a, M = A.shape
    assert M == columns(a)
    m, u = least_nonresidue(p), bezout_exponent(p, d)
    mu = m-1
    inv = np.array([0]+[pow(t, -1, p) for t in range(1, p)], dtype=np.int64)
    nr = np.array([pow(t, (p-1)//2, p) == p-1 for t in range(p)])
    offs = block_offsets(a)
    ar = np.arange(N)
    V = np.zeros((N, a, 0), dtype=np.int64)
    Y, D, YP = [], [], []
    K = np.full(N, -1, dtype=np.int64)
    for k in range(a+1):
        blk = A[:, :, offs[k]:offs[k]+a+1-k]
        js, y = _fd_batch(p, np.concatenate([V, blk], axis=2), inv)
        delta = y[:, k:]
        dm = np.where(nr[delta], delta, 0)
        vnew = (mu*np.einsum("nri,ni->nr", blk, dm)) % p
        js2, y2 = _fd_batch(p, np.concatenate([V, vnew[:, :, None]], axis=2), inv)
        stop = (K < 0) & (js2 == k)
        K[stop] = k
        Y.append(y)
        D.append(delta)
        YP.append(y2)
        V = np.concatenate([V, vnew[:, :, None]], axis=2)
    assert np.all(K >= 0)
    cR = np.where(nr, m, 1)                      # c(1, delta)
    x = np.zeros((N, M), dtype=np.int64)
    tau = np.zeros((N, a), dtype=np.int64)
    for k in range(a+1):
        sel = K == k
        x[sel, offs[k]:offs[k]+a+1-k] = D[k][sel]*cR[D[k][sel]] % p
        for l in range(k):
            tau[sel, l] = (Y[k][sel, l]+YP[k][sel, l]) % p
    for l in range(a, 0, -1):
        zeta = tau[:, l-1].copy()
        nz = nr[zeta]
        dl = D[l-1]
        c = np.where(nz[:, None], 0, 1)+np.where(nr[dl], mu, 0)
        x[:, offs[l-1]:offs[l-1]+a+2-l] = (x[:, offs[l-1]:offs[l-1]+a+2-l]+zeta[:, None]*dl % p*c) % p
        za = np.where(nz, 0, zeta)
        for j in range(1, l):
            tau[:, j-1] = (tau[:, j-1]+za*Y[l-1][:, j-1]) % p
    roots = np.array([rho(p, t) if not nr[t] else -1 for t in range(p)], dtype=np.int64)
    assert np.all(roots[x] >= 0), "some weight is a non-residue"
    powu = np.array([pow(t, u, p) for t in range(p)], dtype=np.int64)
    return powu[roots[x]], x, K


# ====================================================================== the circuit

class CoherentSDEK2(CoherentSDE):
    """Permutation circuit for (p, a, d), kappa_d = 2. Layout: L[c][r] input
    registers (column c, row r), S[c] outputs, the rest workspace."""

    def __init__(self, p, a, d, mutate=None):
        if p < 3 or not is_prime(p):
            raise ValueError("p must be an odd prime")
        if a < 1:
            raise ValueError("a >= 1")
        self.p, self.a, self.d = p, a, d
        self.u = bezout_exponent(p, d)
        self.m = least_nonresidue(p)
        self.mu = self.m-1
        self.S2, self.Q = two_adic(p)
        self.zgen = pow(self.m, self.Q, p)
        self.M = M = columns(a)
        self.offs = block_offsets(a)
        self.mutate = mutate or {}
        self.b = b = nbits(p)
        self.nw = 0
        self.free, self.free_bits = [], []
        self.L = [[self._fresh_reg() for _ in range(a)] for _ in range(M)]
        self.S = [self._fresh_reg() for _ in range(M)]
        self.anc = Anc(self._fresh(anc_size(b)), b)
        self.tmp = self._fresh(max(0, b-2, a-1))
        self.n_fd = []
        F = self._forward()
        C = self._copy_stage()
        self.F, self.C = F, C
        self.prog = Prog(F+C+F.inverse())
        self.io_wires = {w for col in self.L for r in col for w in r} | {w for r in self.S for w in r}

    # ---------------------------------------------------------------- small helpers
    def _bit(self):
        """A 1-wire flag that is 0 at this point."""
        return self.free_bits.pop() if self.free_bits else self._fresh(1)[0]

    def _eq_const_into(self, P, reg, const, out):
        """out ^= [reg == const] (reg restored, temporaries clean)."""
        flips = [q for j, q in enumerate(reg) if not (const >> j) & 1]
        for q in flips:
            P.x(q)
        self._and_into(P, reg, out)
        for q in flips:
            P.x(q)

    def _load_const(self, P, reg, const, ctrl):
        """reg ^= const if ctrl (reg's bits XORed by CX from ctrl)."""
        for j, q in enumerate(reg):
            if (const >> j) & 1:
                P.cx(ctrl, q)

    def _copy(self, P, src, dst):
        for qs, qd in zip(src, dst):
            P.cx(qs, qd)

    def _pow_reg(self, P, base, n, used):
        """Register holding base^n (n >= 1): alias for n = 1, else a chain in P."""
        if n == 1:
            return base
        ch, res, u = self._pow_chain(base, n)
        P += ch
        used += u
        return res

    def _legendre_flag(self, P, y, flag):
        """flag ^= [y in N] (Euler: y^((p-1)/2) == p-1), chain uncomputed locally."""
        p = self.p

        def sink(PP, reg):
            self._eq_const_into(PP, reg, p-1, flag)
        self._pow_copy(P, y, (p-1)//2, sink)

    # ---------------------------------------------------------------- first dependency
    def _fd(self, F, cols, R):
        """Coherent Gauss-Jordan first dependency of n <= R+1 columns (each a list
        of R registers, read only). Returns (dep, Z): dep[c] = [first dependency at
        column c] for c < len(dep), Z[c] = -y_c (0 if the list is independent)."""
        p, b = self.p, self.b
        n = len(cols)
        assert 1 <= n <= R+1
        W = [[None]*n for _ in range(R)]
        for c in range(n):
            for r in range(R):
                W[r][c] = self._fresh_reg()
                self._copy(F, cols[c][r], W[r][c])
        act = [self._fresh(1)[0]]
        F.x(act[0])
        dep = []
        nprod = 0
        for k in range(min(n, R)):
            nz = {}
            for r in range(k, R):
                nz[r] = self._fresh(1)[0]
                self._or_into(F, W[r][k], nz[r])
            z = act[k]
            sel = {}
            for r in range(k, R):
                if r > k:
                    sel[r] = self._fresh(1)[0]
                    F.ccx(z, nz[r], sel[r])
                zn = self._fresh(1)[0]
                F.x(nz[r])
                F.ccx(z, nz[r], zn)
                F.x(nz[r])
                z = zn
            dep.append(z)
            a1 = self._fresh(1)[0]
            F.cx(act[k], a1)
            F.cx(z, a1)
            act.append(a1)
            piv = a1
            for r in range(k+1, R):
                for c in range(k, n):
                    for qa, qb in zip(W[k][c], W[r][c]):
                        self._cswap(F, sel[r], qa, qb)
            u = W[k][k]
            uinv = self._fresh_reg()
            self._pow_copy(F, u, p-2, lambda P, src, dst=uinv: self._copy(P, src, dst))
            w, wi = self._fresh_reg(), self._fresh_reg()
            for qs, qd in zip(uinv, w):
                F.ccx(piv, qs, qd)
            for qs, qd in zip(u, wi):
                F.ccx(piv, qs, qd)
            F.x(piv)
            F.cx(piv, w[0])
            F.cx(piv, wi[0])
            F.x(piv)
            for c in range(k, n):
                t = W[k][c]
                tn = self._reg()
                self._product(F, tn, w, t, 1)
                self._product(F, t, wi, tn, -1)
                self._release(t)
                W[k][c] = tn
            for j in range(R):
                if j == k:
                    continue
                mreg = self._fresh_reg()
                for qs, qd in zip(W[j][k], mreg):
                    F.ccx(piv, qs, qd)
                for c in range(k+1, n):
                    self._product(F, W[j][c], mreg, W[k][c], -1)
                for qs, qd in zip(mreg, W[j][k]):
                    F.cx(qs, qd)
        if n == R+1:
            dep.append(act[R])
        Z = [self._fresh_reg() for _ in range(n)]
        for k in range(len(dep)):
            for i in range(k):
                for qs, qd in zip(W[i][k], Z[i]):
                    F.ccx(dep[k], qs, qd)
            for j, q in enumerate(Z[k]):
                if (p-1) >> j & 1:
                    F.cx(dep[k], q)
        self.n_fd.append((R, n))
        return dep, Z

    # ---------------------------------------------------------------- forward pass F
    def _forward(self):
        p, a, b, m, mu = self.p, self.a, self.b, self.m, self.mu
        mut = self.mutate
        F = Prog()
        V = []                       # v_1..v_k (lists of a registers)
        run = self._fresh(1)[0]
        F.x(run)
        Zs, Ds, NQ, Fk = [], [], [], []
        for k in range(a+1):
            blk = [self.L[self.offs[k]+i] for i in range(a+1-k)]
            dep, Z = self._fd(F, V+blk, a)
            # delta_i = -Z[k+i]
            D, nq = [], []
            for i in range(a+1-k):
                dr = self._fresh_reg()
                self._scaled(F, dr, Z[k+i], -1)
                D.append(dr)
                f = self._fresh(1)[0]
                self._legendre_flag(F, dr, f)
                nq.append(f)
            # v_{k+1}[r] = mu * sum_{delta_i in N} delta_i lambda_i[r]
            vnew = [self._fresh_reg() for _ in range(a)]
            for i in range(a+1-k):
                dm = self._fresh_reg()
                for qs, qd in zip(D[i], dm):
                    F.ccx(nq[i], qs, qd)
                for r in range(a):
                    self._product(F, vnew[r], dm, blk[i][r], mut.get("mu", mu))
            # stop test (report Lemma 4): v_{k+1} in U_k  <=>  no delta_i in N.
            # allP = AND_i ~nq_i ; F_k = run_k & allP ; run_{k+1} = run_k & ~allP
            allp = self._fresh(1)[0]
            for f in nq:
                F.x(f)
            self._and_into(F, nq, allp)
            for f in nq:
                F.x(f)
            fk = self._fresh(1)[0]
            F.ccx(run, allp, fk)
            rn = self._fresh(1)[0]
            F.cx(run, rn)
            F.cx(fk, rn)
            run = rn
            Zs.append(Z)
            Ds.append(D)
            NQ.append(nq)
            Fk.append(fk)
            V.append(vnew)
        self.Fk, self.Ds = Fk, Ds
        # tau_l = -Z_K[l-1] = y^(K)_{l-1}, l = 1..a (one-hot select, then add; Lemma 4: y' = 0)
        tau = [self._fresh_reg() for _ in range(a)]
        for l in range(1, a+1):
            A1 = self._fresh_reg()
            for k in range(l, a+1):
                for qs, qd in zip(Zs[k][l-1], A1):
                    F.ccx(Fk[k], qs, qd)
            self._scaled(F, tau[l-1], A1, mut.get("tau", -1))
        # back substitution l = a..1
        nzeta = [None]*(a+1)
        for l in range(a, 0, -1):
            zeta = tau[l-1]
            f = self._fresh(1)[0]
            self._legendre_flag(F, zeta, f)
            nzeta[l] = f
            if l > 1:
                za = self._fresh_reg()            # zeta if zeta in P u {0}, else 0
                F.x(f)
                for qs, qd in zip(zeta, za):
                    F.ccx(f, qs, qd)
                F.x(f)
                for j in range(1, l):
                    self._product(F, tau[j-1], za, Zs[l-1][j-1], -1)   # tau_j += za*y_{j-1}
        self.tau = tau
        # weights x_i
        X = [self._fresh_reg() for _ in range(self.M)]
        for k in range(a+1):
            for i in range(a+1-k):
                col = self.offs[k]+i
                dl, nqi = Ds[k][i], NQ[k][i]
                w = self._fresh_reg()
                # round K at zeta = 1: c(1, delta) = 1 (Lemma 4: delta in P u {0} there)
                F.cx(Fk[k], w[0])
                if k < a:
                    zeta, nz = tau[k], nzeta[k+1]
                    c = self._fresh_reg()
                    c1, c2, c3 = self._fresh(1)[0], self._fresh(1)[0], self._fresh(1)[0]
                    F.x(nz)
                    F.x(nqi)
                    F.ccx(nz, nqi, c1)                 # zeta in P u 0, delta in P u 0
                    F.x(nqi)
                    F.ccx(nz, nqi, c2)                 # zeta in P u 0, delta in N
                    F.x(nz)
                    F.ccx(nz, nqi, c3)                 # zeta in N, delta in N
                    self._load_const(F, c, 1, c1)
                    self._load_const(F, c, mut.get("m", m), c2)
                    self._load_const(F, c, mu, c3)
                    self._product(F, w, zeta, c, 1)    # w = [F_k] + zeta c(zeta, delta)
                self._product(F, X[col], dl, w, 1)
        self.X = X
        self.forward_wires = self.nw
        return F

    # ---------------------------------------------------------------- copy stage
    def _sqrt_chain(self, x):
        """Prog computing a square root of x (x in P u {0}) by oblivious
        Tonelli-Shanks with the fixed z = m^Q; returns (prog, root, regs, bits)."""
        p, S, Q = self.p, self.S2, self.Q
        P, used, bits = Prog(), [], []
        h = (Q-1)//2
        if h == 0:
            r = t = x
        else:
            aa = self._pow_reg(P, x, h, used)
            r = self._reg()
            used.append(r)
            self._product(P, r, aa, x, 1)                 # r = x^((Q+1)/2)
            t = self._reg()
            used.append(t)
            self._product(P, t, aa, r, 1)                 # t = x^Q
        zinv = pow(self.zgen, -1, p)
        for j in range(S-1):
            uu = t
            for _ in range(S-2-j):
                nr = self._reg()
                used.append(nr)
                self._product(P, nr, uu, uu, 1)
                uu = nr
            kj = self._bit()
            bits.append(kj)
            self._eq_const_into(P, uu, p-1, kj)           # k_j = [t_j^(2^(S-2-j)) == -1]
            if j < S-2:
                w = self._reg()
                used.append(w)
                P.x(w[0])
                self._load_const(P, w, 1 ^ pow(zinv, 2 << j, p), kj)
                nt = self._reg()
                used.append(nt)
                self._product(P, nt, t, w, 1)             # t_{j+1} = t_j z^(-2^(j+1) k_j)
                t = nt
            w2 = self._reg()
            used.append(w2)
            P.x(w2[0])
            self._load_const(P, w2, 1 ^ pow(zinv, 1 << j, p), kj)
            nr = self._reg()
            used.append(nr)
            self._product(P, nr, r, w2, 1)                # r_{j+1} = r_j z^(-2^j k_j)
            r = nr
        return P, r, used, bits

    def _copy_stage(self):
        C = Prog()
        p = self.p
        for i in range(self.M):
            P, r, used, bits = self._sqrt_chain(self.X[i])
            sg = self._reg()
            used.append(sg)
            P.x(sg[0])
            self._load_const(P, sg, 1 ^ (p-1), r[0])      # sg = -1 if r odd else 1
            rh = self._reg()
            used.append(rh)
            self._product(P, rh, r, sg, 1)                # rho = even root
            res = self._pow_reg(P, rh, self.u, used)
            C += P
            self._scaled(C, self.S[i], res, self.mutate.get("out", 1))
            C += P.inverse()
            for reg in reversed(used):
                self._release(reg)
            for q in reversed(bits):
                self.free_bits.append(q)
        return C

    # ---------------------------------------------------------------- counts
    def counts(self):
        per = {}
        tot = Counter()
        for (kind, coeff), n in self.macro_counts().items():
            if (kind, coeff) not in per:
                per[(kind, coeff)] = macro_gate_types(self.p, kind, coeff)
            for k, v in per[(kind, coeff)].items():
                tot[k] += n*v
        for it in self.prog:
            if not isinstance(it, tuple):
                continue
            tot[it[0]] += 1
        tot["total"] = sum(v for k, v in tot.items() if k != "total")
        mc = self.macro_counts()
        return {"gates": dict(tot),
                "add_product": sum(n for (k, _), n in mc.items() if k == "add_product"),
                "add_scaled": sum(n for (k, _), n in mc.items() if k == "add_scaled"),
                "qubits": self.nw, "qubits_io": len(self.io_wires),
                "qubits_workspace": self.nw-len(self.io_wires)}


# ====================================================================== closed forms

def _ell(n):
    """Products of left-to-right square-and-multiply for x^n (0 for n <= 1)."""
    return chain_length(n) if n >= 2 else 0


def fd_products(R, n, Ip):
    """Products of one first-dependency machine F-pass on n columns in F_p^R."""
    return sum(2*(n-c)+(R-1)*(n-1-c)+2*Ip for c in range(min(n, R)))


def sqrt_products(p):
    """Products of one oblivious Tonelli-Shanks root (compute only)."""
    S, Q = two_adic(p)
    h = (Q-1)//2
    head = 0 if h == 0 else _ell(h)+2
    return head+(S-1)*(S-2)//2+2*(S-1)-(1 if S >= 2 else 0)


def closed_form_macros(p, a, d):
    """Macro counts of F + C + F^-1. With I = ell(p-2), Lp = ell((p-1)/2):
    n_F = (a+1) fd(a, a+1) [one first dependency per round] + 2 Lp (M + a)
    [Legendre flags of the M deltas and the a zetas, chain computed and
    uncomputed] + a M [v] + a(a-1)/2 [back substitution] + (M-1) [zeta c(zeta,
    delta)] + M [x = delta w]; C = 2 M (T + 1 + ell(u)) products, T =
    sqrt_products(p). add_scaled: 2(M + a) (delta, tau; coefficient -1) + M (copy)."""
    M = columns(a)
    Ip, Lp = _ell(p-2), _ell((p-1)//2)
    u = bezout_exponent(p, d)
    nF = (a+1)*fd_products(a, a+1, Ip)+2*Lp*(M+a)+a*M+a*(a-1)//2+(M-1)+M
    T = sqrt_products(p)
    return {"I_p": Ip, "L_p": Lp, "T_sqrt": T, "u": u, "products_F": nF,
            "add_product": 2*nF+2*M*(T+1+_ell(u)),
            "add_scaled": 2*(M+a)+M}


def _ladder(b):
    """CCX of one b-wire AND ladder (OR flag / equality test)."""
    return 1 if b == 2 else 2*b-3


def _and_ccx(n):
    """CCX of _and_into over n controls."""
    return 0 if n == 1 else (1 if n == 2 else 2*n-3)


def fd_nonmacro_ccx(R, n, b):
    """Non-macro CCX of one first-dependency F-pass (n columns in F_p^R): per step
    k, (R-k) OR ladders, (R-k-1) sel + (R-k) chain CCX, b(R-1-k)(n-k) Fredkins,
    2b (w, wi) and b(R-1) (multipliers); selection b*s'(s'-1)/2 with
    s' = min(n, R) + [n = R+1]."""
    lad = _ladder(b)
    s = sum((R-k)*lad+(R-k-1)+(R-k)+b*(R-1-k)*(n-k)+2*b+b*(R-1) for k in range(min(n, R)))
    sp = min(n, R)+(1 if n == R+1 else 0)
    return s+b*sp*(sp-1)//2


def closed_form_toffoli(p, a, d):
    """Exact CCX count of F + C + F^-1:
      2 * [ (a+1) fd(a, a+1) + (M+a) lad [Legendre flags] + bM [masked deltas]
            + sum_k (and(a+1-k) + 1) [stop flags] + b a(a+1)/2 [tau select]
            + b(a-1) [masked zetas] + 3(M-1) [weight cases] ]
      + 2 M (S-1) lad [Tonelli-Shanks flags, computed and uncomputed]
      + (40b^2+2b) #add_product + add_scaled CCX (formula_counts)."""
    b = nbits(p)
    mc = closed_form_macros(p, a, d)
    lad = _ladder(b)
    M = columns(a)
    S, _ = two_adic(p)
    nonmacro = (a+1)*fd_nonmacro_ccx(a, a+1, b)
    nonmacro += (M+a)*lad + b*M + sum(_and_ccx(a+1-k)+1 for k in range(a+1))
    nonmacro += b*a*(a+1)//2 + b*(a-1) + 3*(M-1)
    sc = (2*(M+a)*formula_counts(p, p-1)["add_scaled_ccx"]
          + M*formula_counts(p, 1)["add_scaled_ccx"])
    return 2*nonmacro + 2*M*(S-1)*lad + mc["add_product"]*(40*b*b+2*b) + sc


def pool_registers(p, d):
    """Peak size of the shared b-wire register pool: the largest local demand
    among a normalisation (1), a Fermat inversion chain (I_p), a Legendre chain
    (L_p) and one copy-stage root (T + W_S + 2 + ell(u), W_S = 2S-3 constant
    multiplier registers for S >= 2)."""
    S, _ = two_adic(p)
    WS = 2*S-3 if S >= 2 else 0
    copy = sqrt_products(p)+WS+2+_ell(bezout_exponent(p, d))
    return max(1, _ell(p-2), _ell((p-1)//2), copy)


def closed_form_qubits(p, a, d):
    """Peak qubits = all allocated wires:
      IO (a+1) M b; arith ancillas 3b+5; ladder temps max(0, b-2, a-1); run 1;
      per round one first dependency fd(a, a+1): a(a+1) b (copy) + 1 + 3a(a+1)/2
        (flags) + a(a+2) b (u^-1, w, wi, a-1 multipliers per step) + (a+1) b (Z);
      per round k: (a+1-k)(2b+1) (delta, flag, masked delta) + a b (v) + 3 (allP, F_k, run);
      tau 2ab (tau, select) + a (zeta flags) + (a-1) b (masked zeta);
      weights M b (x) + M b (w) + (M-1)(b+3) (c and three case flags);
      pool pool_registers*b; Tonelli-Shanks flag bits S-1."""
    b = nbits(p)
    M = columns(a)
    S, _ = two_adic(p)
    fdq = a*(a+1)*b+1+3*a*(a+1)//2+a*(a+2)*b+(a+1)*b
    q = (a+1)*M*b + 3*b+5 + max(0, b-2, a-1) + 1
    q += (a+1)*fdq
    q += sum((a+1-k)*(2*b+1)+a*b+3 for k in range(a+1))
    q += 2*a*b + a + (a-1)*b
    q += 2*M*b + (M-1)*(b+3)
    q += pool_registers(p, d)*b + (S-1)
    return q


def closed_form_products_poly(a, Ip, Lp, T, eu):
    """#add_product as an explicit polynomial (report Section 3):
    2 n_F + 2M(T+1+eu), M = (a+1)(a+2)/2,
    n_F = (a^4 + 4a^3 + 13a^2 + 12a + 2)/2 + Ip(2a^2+2a) + Lp(a^2+5a+2)."""
    M = (a+1)*(a+2)//2
    n2 = a**4+4*a**3+13*a**2+12*a+2
    assert n2 % 2 == 0
    nF = n2//2 + Ip*(2*a*a+2*a) + Lp*(a*a+5*a+2)
    return 2*nF+2*M*(T+1+eu)


def check_circuit(circ, A, gates=None):
    """Run the circuit on inputs A (N, a, M); compare with the batched reference."""
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
    ref, x, K = canonical_witness_k2_batch(p, A, d)
    inputs_ok = all(np.array_equal(sim.read(circ.L[c][r]), A[:, r, c])
                    for c in range(M) for r in range(a))
    work_clean = not any(sim.wire_nonzero(w) for w in range(circ.nw) if w not in circ.io_wires)
    sd = np.array([pow(t, d, p) for t in range(p)], dtype=np.int64)[np.minimum(s, p-1)]
    eq_ok = bool(np.all(np.einsum("nrc,nc->nr", A, sd) % p == 0))
    return {"p": p, "a": a, "d": d, "u": circ.u, "M": M, "inputs": int(N), "gates": len(gates),
            "qubits": circ.nw, "output_equals_canonical": bool(np.array_equal(s, ref)),
            "inputs_restored": inputs_ok, "workspace_clean": work_clean,
            "witness_nonzero": bool(np.all(s.any(axis=1))), "equation_holds": eq_ok,
            "canonical_padding_free": bool(np.all(s < p)), "roots_even": bool(np.all(s[:, :] % 2 == 0)) if circ.u == 1 else None,
            "K_hist": np.bincount(K, minlength=a+1).tolist(), "sim_seconds": round(dt, 3)}


def all_inputs(p, a):
    M = columns(a)
    n = a*M
    N = p**n
    idx = np.arange(N, dtype=np.int64)
    A = np.zeros((N, a, M), dtype=np.int64)
    for t in range(n):
        r, c = divmod(t, M)
        A[:, r, c] = (idx // p**t) % p
    return A


def structured_inputs(p, a, n, seed=0):
    """Random inputs biased to degenerate cases: each column random, zero, a
    multiple of one earlier column, or a random combination of earlier columns,
    and a quarter of the inputs with all columns in a random lower-dim subspace."""
    rng = np.random.default_rng(seed)
    M = columns(a)
    A = rng.integers(0, p, size=(n, a, M), dtype=np.int64)
    for c in range(M):
        mode = rng.integers(0, 5, size=n)
        A[mode == 1, :, c] = 0
        if c:
            for i in np.nonzero(mode >= 3)[0]:
                coef = rng.integers(0, p, size=c)
                if mode[i] == 3:
                    coef = np.zeros(c, dtype=np.int64)
                    coef[rng.integers(0, c)] = rng.integers(1, p)
                A[i, :, c] = A[i, :, :c] @ coef % p
    sub = rng.random(n) < 0.25
    for i in np.nonzero(sub)[0]:
        rk = int(rng.integers(0, a))
        B = rng.integers(0, p, size=(a, max(rk, 1)))
        C = rng.integers(0, p, size=(max(rk, 1), M))
        A[i] = (B @ C) % p if rk else 0
    return A


def exhaustive_check(p, a, d):
    circ = CoherentSDEK2(p, a, d)
    return check_circuit(circ, all_inputs(p, a))


def sampled_check(p, a, d, n=4096, seed=0):
    circ = CoherentSDEK2(p, a, d)
    return check_circuit(circ, structured_inputs(p, a, n, seed))


def count_row(p, a, d):
    circ = CoherentSDEK2(p, a, d)
    c = circ.counts()
    m = closed_form_macros(p, a, d)
    ct = closed_form_toffoli(p, a, d)
    cq = closed_form_qubits(p, a, d)
    return {"p": p, "b": circ.b, "a": a, "d": d, "M": circ.M, **c,
            **{"closed_" + k: v for k, v in m.items()},
            "closed_toffoli": ct, "closed_qubits": cq,
            "toffoli_matches": c["gates"].get("ccx", 0) == ct,
            "macros_match": (c["add_product"], c["add_scaled"]) == (m["add_product"], m["add_scaled"]),
            "qubits_match": c["qubits"] == cq}


def root_circuit(p, d=2):
    """The copy stage alone on one weight register x (M = 1): |x>|0> -> |x>|rho(x)^u>."""
    c = CoherentSDEK2.__new__(CoherentSDEK2)
    c.p, c.d, c.u, c.m = p, d, bezout_exponent(p, d), least_nonresidue(p)
    c.mu = c.m-1
    c.S2, c.Q = two_adic(p)
    c.zgen = pow(c.m, c.Q, p)
    c.M, c.mutate = 1, {}
    c.b = b = nbits(p)
    c.nw, c.free, c.free_bits = 0, [], []
    c.X, c.S = [c._fresh_reg()], [c._fresh_reg()]
    c.anc = Anc(c._fresh(anc_size(b)), b)
    c.tmp = c._fresh(max(0, b-2))
    c.prog = c._copy_stage()
    c.io_wires = set(c.X[0]) | set(c.S[0])
    return c


def root_check(p, d=2):
    """Exhaustive over every x in P u {0}: output rho(x)^u (rho from the reference
    Tonelli-Shanks, made even), x restored, all workspace 0."""
    c = root_circuit(p, d)
    xs = np.array(sorted({t*t % p for t in range(p)}), dtype=np.int64)
    sim = BitSim(c.nw, len(xs))
    sim.load(c.X[0], xs)
    gates = c.flatten()
    sim.run(gates)
    out = sim.read(c.S[0])
    want = np.array([pow(rho(p, int(t)), c.u, p) for t in xs], dtype=np.int64)
    clean = not any(sim.wire_nonzero(w) for w in range(c.nw) if w not in c.io_wires)
    return {"p": p, "d": d, "S": c.S2, "squares": int(len(xs)), "gates": len(gates),
            "root_ok": bool(np.array_equal(out, want)),
            "x_restored": bool(np.array_equal(sim.read(c.X[0]), xs)), "workspace_clean": clean}


def input_range(p, a, start, stop):
    """Canonical inputs with indices start..stop-1 in the all_inputs order."""
    M = columns(a)
    idx = np.arange(start, stop, dtype=np.int64)
    A = np.zeros((stop-start, a, M), dtype=np.int64)
    for t in range(a*M):
        r, c = divmod(t, M)
        A[:, r, c] = idx % p
        idx //= p
    return A


def exhaustive_check_chunked(p, a, d, chunk=1 << 21, log=print):
    """All p^(aM) inputs in chunks (one circuit, one gate list)."""
    circ = CoherentSDEK2(p, a, d)
    gates = circ.flatten()
    N = p**(a*columns(a))
    keys = ("output_equals_canonical", "inputs_restored", "workspace_clean", "witness_nonzero",
            "equation_holds", "canonical_padding_free")
    agg = {k: True for k in keys}
    K = np.zeros(a+1, dtype=np.int64)
    t0 = time.time()
    for st in range(0, N, chunk):
        r = check_circuit(circ, input_range(p, a, st, min(N, st+chunk)), gates)
        for k in keys:
            agg[k] &= r[k]
        K += np.array(r["K_hist"])
        log(json.dumps({"done": min(N, st+chunk), "of": N, "ok": all(agg.values()),
                        "elapsed": round(time.time()-t0, 1)}), flush=True)
    return {"p": p, "a": a, "d": d, "M": circ.M, "inputs": int(N), "gates": len(gates),
            "qubits": circ.nw, **agg, "K_hist": K.tolist(), "seconds": round(time.time()-t0, 1)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None)
    ap.add_argument("--chunked", default=None, help="p,a,d: chunked exhaustive check only")
    args = ap.parse_args()
    if args.chunked:
        p, a, d = (int(t) for t in args.chunked.split(","))
        r = exhaustive_check_chunked(p, a, d)
        print(json.dumps(r), flush=True)
        if args.out:
            with open(args.out, "w") as f:
                json.dump({"status": STATUS, "exhaustive_chunked": r}, f, indent=1)
        return
    res = {"status": STATUS, "exhaustive": [], "sampled": [], "roots": [], "counts": []}
    ex = [(p, 1, 2) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)] + [(7, 1, 4), (11, 1, 4), (13, 1, 10),
                                                              (3, 2, 2), (3, 2, 4)]
    for p, a, d in ex:
        r = exhaustive_check(p, a, d)
        print(json.dumps(r), flush=True)
        res["exhaustive"].append(r)
    for p, a, d in [(5, 2, 2), (7, 2, 2), (11, 2, 2), (13, 2, 2), (17, 2, 2), (41, 2, 2), (7, 2, 4),
                    (13, 2, 10), (3, 3, 2), (5, 3, 2), (7, 3, 2), (11, 3, 2), (13, 3, 2), (3, 4, 2),
                    (5, 4, 2)]:
        r = sampled_check(p, a, d, n=8192, seed=p*100+a*10+d)
        print(json.dumps(r), flush=True)
        res["sampled"].append(r)
    for p in (3, 5, 7, 11, 13, 17, 41, 97, 257, 65537):
        r = root_check(p)
        print(json.dumps(r), flush=True)
        res["roots"].append(r)
    for p in (3, 5, 7, 13, 17, 101, 257, 1031, 65537, 2**31-1, 2**61-1):
        for a in (1, 2, 3, 4, 8):
            r = count_row(p, a, 2)
            print(json.dumps({k: r[k] for k in ("p", "b", "a", "M", "add_product", "add_scaled", "qubits",
                                                 "toffoli_matches", "macros_match", "qubits_match")}
                             | {"total": r["gates"]["total"], "ccx": r["gates"].get("ccx")}), flush=True)
            res["counts"].append(r)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
