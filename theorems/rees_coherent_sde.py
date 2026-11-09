"""Coherent (reversible) linear-grade SDE solve for the Rees HSP receiver.

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-04-rees-coherent-sde.md.

At a recursion grade d with kappa_d = gcd(d, p-1) = 1 the merge takes g+1
label columns lambda_0..lambda_g in F_p^g and needs a nonzero s with
sum_l s_l^d lambda_l = 0 (main.tex, thm:power-sde(i)). This module builds a
permutation circuit (X, CX, CCX, SWAP only) that maps

    |lambda_0..lambda_g>|0>_S|0>_work  ->  |lambda_0..lambda_g>|s(lambda)>_S|0>_work

on every canonical input, where s is the CANONICAL witness ("first
dependency", Lemma 1 of the report):

    j*  = min{ j : lambda_j in span(lambda_0..lambda_{j-1}) }   (always <= g),
    lambda_{j*} = sum_{i<j*} c_i lambda_i   (unique c),
    y   = (-c_0, .., -c_{j*-1}, 1, 0, .., 0),   s_l = y_l^e,  e d = 1 mod (p-1).

Construction (Bennett): F computes the reduced row echelon form of a copy of
the columns by an oblivious Gauss-Jordan sweep over columns k = 0..g-1 with a
coherent "still independent" flag act_k, a coherent first-nonzero pivot
search (OR ladders and a prefix chain), controlled row swaps (Fredkin gates),
a Fermat inversion u^(p-2) of the pivot (square-and-multiply, locally
uncomputed), in-place row normalisation by two multiply-accumulates
(t' = w t, then t -= w^-1 t'), and elimination with stored multipliers. It
then selects z = -y by the one-hot flags dep_k. The copy stage computes z_l^e
(square-and-multiply, locally uncomputed) and adds -(z_l^e) = s_l into the
output register. Then F^-1 (the reversed gate list) clears all workspace.

The mod-p arithmetic is the add_product / add_scaled macros of
theorems/rees_circuit_arith.py (imported, not edited): t += k a b mod p with
40b^2+2b Toffoli gates, t += k a mod p, 3b+5 shared ancillas that every macro
returns to 0.

Domain: canonical words (every coordinate < p). Padding words are not
claimed. Gate-level checks: simulate() is an exact bit-sliced basis-state
simulator (the circuit is a permutation, so basis states suffice).

What this does NOT do: grades with kappa_d >= 2 (Schedules 1-3), the
descent itself (the controlled delta_s), QFT_p, the oracle, noise. It does
not flip any claim gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import random
import time

import numpy as np

from theorems.rees_circuit_arith import (Anc, Ops, add_product_ops, add_scaled_ops, anc_size,
                                         formula_counts)

STATUS = {"status": "coherent_linear_grade_sde_solve_finite_checks",
          "scope": "grades with kappa_d = gcd(d, p-1) = 1 only (thm:power-sde(i))",
          "coherent_receiver_implemented": False, "general_sde_implemented": False,
          "coherent_higher_kappa_sde_implemented": False,
          "coherent_linear_sde_implemented": True,
          "wired_into_generated_receiver": False,
          "independent_review": False, "speedup_claim_allowed": False}


def is_prime(n):
    """Deterministic Miller-Rabin for n < 3.3e24 (bases the first 13 primes)."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for q in small:
        if n % q == 0:
            return n == q
    dd, s = n-1, 0
    while dd % 2 == 0:
        dd, s = dd//2, s+1
    for a in small:
        x = pow(a, dd, n)
        if x in (1, n-1):
            continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1:
                break
        else:
            return False
    return True


def nbits(p):
    return max(1, (p-1).bit_length())


def inverse_exponent(p, d):
    """e in [1, p-2] with e d = 1 mod (p-1); requires gcd(d, p-1) = 1."""
    if math.gcd(d, p-1) != 1:
        raise ValueError("kappa_d = gcd(d, p-1) must be 1")
    return pow(d % (p-1), -1, p-1)


def chain_length(n):
    """Number of multiplications of left-to-right square-and-multiply for x^n."""
    return (n.bit_length()-1)+(bin(n).count("1")-1)


# ====================================================================== references

def canonical_witness(p, cols, d):
    """Reference from the DEFINITION (no RREF): j* = first column in the span of
    the earlier ones, c = its unique coefficients, y = (-c, 1, 0..), s = y^e.
    cols: list of g+1 tuples in F_p^g. Returns (s, y, jstar)."""
    e = inverse_exponent(p, d)
    g = len(cols)-1
    basis = []    # echelon basis of span(cols[:j]) with coefficient vectors
    for j, col in enumerate(cols):
        v = [int(x) % p for x in col]
        coef = [0]*(g+1)
        coef[j] = 1                         # v = sum coef_i lambda_i
        for (piv, bv, bc) in basis:
            if v[piv]:
                m = v[piv]
                v = [(x-m*y) % p for x, y in zip(v, bv)]
                coef = [(x-m*y) % p for x, y in zip(coef, bc)]
        if not any(v):
            y = coef                        # sum y_i lambda_i = 0, y_j = 1, y_i = 0 for i > j
            s = [pow(x, e, p) if x else 0 for x in y]
            return s, y, j
        piv = next(i for i, x in enumerate(v) if x)
        inv = pow(v[piv], -1, p)
        basis.append((piv, [x*inv % p for x in v], [x*inv % p for x in coef]))
    raise AssertionError("unreachable: g+1 columns in F_p^g are dependent")


def is_canonical_bruteforce(p, cols, y):
    """Check the defining property of y by enumeration (small p, g only):
    A y = 0, y_{j*} = 1, y_i = 0 beyond j*, and no nonzero combination of
    lambda_0..lambda_{j*-1} vanishes (prefix independence)."""
    from itertools import product as iproduct
    g = len(cols)-1
    jstar = max(i for i, x in enumerate(y) if x)
    if y[jstar] != 1:
        return False
    for r in range(g):
        if sum(int(y[i])*int(cols[i][r]) for i in range(g+1)) % p:
            return False
    for coef in iproduct(range(p), repeat=jstar):
        if any(coef) and all(sum(coef[i]*cols[i][r] for i in range(jstar)) % p == 0
                             for r in range(g)):
            return False
    return True


def canonical_witness_batch(p, A, d):
    """Vectorised reference: A has shape (N, g, g+1) (A[n, r, c] = row r of
    column c). Oblivious Gauss-Jordan with first-nonzero pivoting, written
    independently of the circuit. Returns s of shape (N, g+1)."""
    e = inverse_exponent(p, d)
    A = np.array(A, dtype=np.int64) % p
    N, g, n = A.shape
    inv = np.array([0]+[pow(x, -1, p) for x in range(1, p)], dtype=np.int64)
    jstar = np.full(N, g, dtype=np.int64)
    active = np.ones(N, dtype=bool)
    for k in range(g):
        sub = A[:, k:, k] != 0
        has = sub.any(axis=1)
        jstar[active & ~has] = k
        piv = active & has
        idx = np.nonzero(piv)[0]
        r = k+sub[idx].argmax(axis=1)
        rk, rr = A[idx, k, :].copy(), A[idx, r, :].copy()
        A[idx, k, :], A[idx, r, :] = rr, rk
        A[idx, k, :] = A[idx, k, :]*inv[A[idx, k, k]][:, None] % p
        for j in range(g):
            if j != k:
                m = A[idx, j, k].copy()
                A[idx, j, :] = (A[idx, j, :]-m[:, None]*A[idx, k, :]) % p
        active = piv
    y = np.zeros((N, n), dtype=np.int64)
    ar = np.arange(N)
    y[ar, jstar] = 1
    for i in range(g):
        mask = i < jstar
        y[mask, i] = (-A[ar[mask], i, jstar[mask]]) % p
    powt = np.array([pow(x, e, p) if x else 0 for x in range(p)], dtype=np.int64)
    return powt[y]


# ====================================================================== the circuit

class Macro:
    __slots__ = ("kind", "coeff", "args", "inv")

    def __init__(self, kind, coeff, args, inv=False):
        self.kind, self.coeff, self.args, self.inv = kind, coeff, args, inv

    def inverse(self):
        return Macro(self.kind, self.coeff, self.args, not self.inv)


class Prog(list):
    """Items: gate tuples (name, qubits) or Macro. Inverse = reversed, macros flagged."""

    def x(self, q):
        self.append(("x", (q,)))

    def cx(self, c, t):
        self.append(("cx", (c, t)))

    def ccx(self, a, b, t):
        self.append(("ccx", (a, b, t)))

    def inverse(self):
        return Prog(it.inverse() if isinstance(it, Macro) else it for it in reversed(self))


class CoherentSDE:
    """Builds the permutation circuit for (p, g, d). Layout (wire indices):
    L[c][r] input registers (column c, row r), S[c] output registers, the
    rest workspace. Attributes: prog (F + copy + F^-1 as a Prog), and the
    stage boundaries."""

    def __init__(self, p, g, d):
        if p < 3 or not is_prime(p):
            raise ValueError("p must be an odd prime")
        self.p, self.g, self.d = p, g, d
        self.e = inverse_exponent(p, d)
        self.b = b = nbits(p)
        self.nw = 0
        self.free = []
        self.L = [[self._fresh_reg() for _ in range(g)] for _ in range(g+1)]
        self.S = [self._fresh_reg() for _ in range(g+1)]
        self.anc = Anc(self._fresh(anc_size(b)), b)
        self.tmp = self._fresh(max(0, b-2))         # AND-ladder temporaries
        self.history_regs = 0
        F = self._forward()
        C = self._copy_stage()
        self.F, self.C = F, C
        self.prog = Prog(F+C+F.inverse())
        self.io_wires = {w for col in self.L for r in col for w in r} | {w for r in self.S for w in r}

    # ---------------------------------------------------------------- allocation
    def _fresh(self, n):
        out = list(range(self.nw, self.nw+n))
        self.nw += n
        return out

    def _fresh_reg(self):
        return self._fresh(self.b)

    def _reg(self):
        """A b-wire register that is 0 on every input at this point of F."""
        return self.free.pop() if self.free else self._fresh_reg()

    def _release(self, r):
        self.free.append(r)

    # ---------------------------------------------------------------- small blocks
    def _and_into(self, P, ctrls, out):
        n = len(ctrls)
        if n == 1:
            P.cx(ctrls[0], out)
            return
        if n == 2:
            P.ccx(ctrls[0], ctrls[1], out)
            return
        t = self.tmp
        lad = Prog()
        lad.ccx(ctrls[0], ctrls[1], t[0])
        for i in range(1, n-2):
            lad.ccx(t[i-1], ctrls[i+1], t[i])
        P += lad
        P.ccx(t[n-3], ctrls[n-1], out)
        P += lad.inverse()

    def _or_into(self, P, reg, out):
        """out ^= [reg != 0] (reg restored, temporaries clean)."""
        P.x(out)
        for q in reg:
            P.x(q)
        self._and_into(P, reg, out)
        for q in reg:
            P.x(q)

    @staticmethod
    def _cswap(P, c, x, y):
        """Fredkin: swap bits x, y when c = 1."""
        P.cx(y, x)
        P.ccx(c, x, y)
        P.cx(y, x)

    def _product(self, P, t, a, b, coeff):
        P.append(Macro("add_product", coeff % self.p, (tuple(t), tuple(a), tuple(b))))

    def _scaled(self, P, t, a, coeff):
        P.append(Macro("add_scaled", coeff % self.p, (tuple(t), tuple(a))))

    def _pow_chain(self, base, n):
        """Prog computing base^n (n >= 2) into fresh registers by left-to-right
        square-and-multiply; returns (prog, result_register, registers_used)."""
        P = Prog()
        x = base
        used = []
        for bit in bin(n)[3:]:
            r = self._reg()
            used.append(r)
            self._product(P, r, x, x, 1)            # r = x^2
            x = r
            if bit == "1":
                r = self._reg()
                used.append(r)
                self._product(P, r, x, base, 1)     # r = x * base
                x = r
        return P, x, used

    def _pow_copy(self, P, base, n, sink):
        """sink(P, value_register) is called with a register holding base^n;
        the chain is computed before and uncomputed after (local Bennett)."""
        if n == 1:
            sink(P, base)
            return
        ch, res, used = self._pow_chain(base, n)
        P += ch
        sink(P, res)
        P += ch.inverse()
        for r in reversed(used):
            self._release(r)

    # ---------------------------------------------------------------- forward pass F
    def _forward(self):
        p, g, b = self.p, self.g, self.b
        F = Prog()
        # workspace copy W[r][c] of the input
        W = [[None]*(g+1) for _ in range(g)]
        for c in range(g+1):
            for r in range(g):
                W[r][c] = self._fresh_reg()
                for qi, qo in zip(self.L[c][r], W[r][c]):
                    F.cx(qi, qo)
        act = [self._fresh(1)[0]]
        F.x(act[0])                                  # act_0 = 1
        dep = []
        self.flag_bits = 1
        for k in range(g):
            # --- coherent first-nonzero pivot search in rows k..g-1 of column k
            nz = {}
            for r in range(k, g):
                nz[r] = self._fresh(1)[0]
                self._or_into(F, W[r][k], nz[r])
            z = act[k]
            sel = {}
            for r in range(k, g):
                if r > k:
                    sel[r] = self._fresh(1)[0]
                    F.ccx(z, nz[r], sel[r])          # sel_r = z_r & nz_r
                zn = self._fresh(1)[0]
                F.x(nz[r])
                F.ccx(z, nz[r], zn)                  # z_{r+1} = z_r & ~nz_r
                F.x(nz[r])
                z = zn
            dep.append(z)                            # dep_k = act_k & column k zero below
            a1 = self._fresh(1)[0]
            F.cx(act[k], a1)
            F.cx(z, a1)                              # act_{k+1} = piv_k = act_k & ~dep_k
            act.append(a1)
            piv = a1
            self.flag_bits += (g-k)+(g-k-1)+(g-k)+1
            # --- controlled row swaps (one-hot sel)
            for r in range(k+1, g):
                for c in range(k, g+1):
                    for qa, qb in zip(W[k][c], W[r][c]):
                        self._cswap(F, sel[r], qa, qb)
            # --- Fermat inverse of the pivot u = W[k][k] (u^(p-2), 0 -> 0)
            u = W[k][k]
            uinv = self._fresh_reg()

            def copy_into(P, src, dst=uinv):
                for qs, qd in zip(src, dst):
                    P.cx(qs, qd)
            self._pow_copy(F, u, p-2, copy_into)
            # --- w = piv ? u^-1 : 1, wi = piv ? u : 1
            w, wi = self._fresh_reg(), self._fresh_reg()
            for qs, qd in zip(uinv, w):
                F.ccx(piv, qs, qd)
            for qs, qd in zip(u, wi):
                F.ccx(piv, qs, qd)
            F.x(piv)
            F.cx(piv, w[0])
            F.cx(piv, wi[0])
            F.x(piv)
            # --- normalise row k in place: t' = w t ; t -= wi t' ; relabel
            for c in range(k, g+1):
                t = W[k][c]
                tn = self._reg()
                self._product(F, tn, w, t, 1)
                self._product(F, t, wi, tn, -1)
                self._release(t)
                W[k][c] = tn
            # --- eliminate column k from the other rows with stored multipliers
            for j in range(g):
                if j == k:
                    continue
                m = self._fresh_reg()
                for qs, qd in zip(W[j][k], m):
                    F.ccx(piv, qs, qd)               # m = piv ? W[j][k] : 0
                for c in range(k+1, g+1):
                    self._product(F, W[j][c], m, W[k][c], -1)
                for qs, qd in zip(m, W[j][k]):
                    F.cx(qs, qd)                     # W[j][k] -= m (equal values -> 0)
            self.history_regs += 3+(g-1)
        dep.append(act[g])                           # j* = g if no earlier dependency
        self.dep = dep
        # --- select z = -y: z_i = W[i][j*] (i < j*), z_{j*} = p-1, 0 beyond
        Z = [self._fresh_reg() for _ in range(g+1)]
        for k in range(g+1):
            for i in range(k):
                for qs, qd in zip(W[i][k], Z[i]):
                    F.ccx(dep[k], qs, qd)
            for j, q in enumerate(Z[k]):
                if (p-1) >> j & 1:
                    F.cx(dep[k], q)
        self.Z, self.W = Z, W
        self.forward_wires = self.nw
        return F

    # ---------------------------------------------------------------- copy stage
    def _copy_stage(self):
        C = Prog()
        for l in range(self.g+1):
            out = self.S[l]

            def sink(P, reg, out=out):
                self._scaled(P, out, reg, -1)        # s_l = -(z_l^e)
            self._pow_copy(C, self.Z[l], self.e, sink)
        return C

    # ---------------------------------------------------------------- flatten / count
    def flatten(self):
        """The full gate list (X, CX, CCX, SWAP), macros expanded with the
        rees_circuit_arith gate lists (inverse macro = reversed list)."""
        cache = {}
        out = []
        for it in self.prog:
            if not isinstance(it, Macro):
                out.append(it)
                continue
            key = (it.kind, it.coeff, it.args)
            ops = cache.get(key)
            if ops is None:
                if it.kind == "add_product":
                    ops = add_product_ops(self.p, *it.args, it.coeff, self.anc)
                else:
                    ops = add_scaled_ops(self.p, *it.args, it.coeff, self.anc)
                cache[key] = ops
            out.extend(reversed(ops) if it.inv else ops)
        return out

    def macro_counts(self, part=None):
        part = self.prog if part is None else part
        return Counter((it.kind, it.coeff) for it in part if isinstance(it, Macro))

    def counts(self):
        """Exact gate counts by type, from the program: gate items counted
        directly, each macro by the per-(kind, coeff) counts of one emitted
        instance (emitted once at this p; the closed forms of
        rees_circuit_arith.formula_counts are cross-checked)."""
        per = {}
        tot = Counter()
        for (kind, coeff), n in self.macro_counts().items():
            if (kind, coeff) not in per:
                per[(kind, coeff)] = macro_gate_types(self.p, kind, coeff)
            for k, v in per[(kind, coeff)].items():
                tot[k] += n*v
        for it in self.prog:
            if not isinstance(it, Macro):
                tot[it[0]] += 1
        tot["total"] = sum(v for k, v in tot.items() if k != "total")
        mc = self.macro_counts()
        return {"gates": dict(tot),
                "add_product": sum(n for (k, _), n in mc.items() if k == "add_product"),
                "add_scaled": sum(n for (k, _), n in mc.items() if k == "add_scaled"),
                "fredkin": fredkin_count(self.g)*self.b,
                "qubits": self.nw,
                "qubits_io": len(self.io_wires),
                "qubits_workspace": self.nw-len(self.io_wires)}


_TYPE_CACHE = {}


def macro_gate_types(p, kind, coeff):
    key = (p, kind, coeff)
    if key not in _TYPE_CACHE:
        b = nbits(p)
        A = Anc(list(range(3*b, 3*b+anc_size(b))), b)
        t, a, bb = list(range(b)), list(range(b, 2*b)), list(range(2*b, 3*b))
        ops = add_product_ops(p, t, a, bb, coeff, A) if kind == "add_product" else \
            add_scaled_ops(p, t, a, coeff, A)
        c = Counter(name for name, _ in ops)
        fc = formula_counts(p, coeff)
        assert sum(c.values()) == fc[kind+"_total"] and c["ccx"] == fc[kind+"_ccx"]
        _TYPE_CACHE[key] = dict(c)
    return _TYPE_CACHE[key]


# ====================================================================== closed forms

def fredkin_count(g):
    """Fredkin gates per bit of the pivot swaps: sum_k (g-1-k)(g+1-k) = g(g+1)(2g+1)/6 - g."""
    return g*(g+1)*(2*g+1)//6-g


def closed_form_macros(p, g, d):
    """Macro counts of F + copy + F^-1 in closed form.
    n_F = g(g+3) [normalise] + (g-1)g(g+1)/2 [eliminate] + 2g I_p [inversions],
    I_p = chain_length(p-2); copy stage 2(g+1) E_e products, E_e = chain_length(e),
    and g+1 add_scaled. Total products 2 n_F + 2(g+1) E_e."""
    e = inverse_exponent(p, d)
    Ip, Ee = chain_length(p-2) if p > 3 else 0, chain_length(e) if e > 1 else 0
    nF = g*(g+3)+(g-1)*g*(g+1)//2+2*g*Ip
    return {"I_p": Ip, "E_e": Ee, "products_F": nF,
            "add_product": 2*nF+2*(g+1)*Ee, "add_scaled": g+1}


def closed_form_toffoli(p, g, d):
    """Exact Toffoli (CCX) count of the whole circuit. Non-macro CCX of F:
    OR ladders (2b-3 each for b>=3, 1 for b=2; g(g+1)/2 of them), chain
    g(g+1)/2 + g(g-1)/2, Fredkins b(g(g+1)(2g+1)/6 - g), w/wi loads 2bg,
    multipliers b g(g-1), selection b g(g+1)/2. Doubled for F^-1, plus the
    macros (40b^2+2b per product, 10b^2+8b+2H per add_scaled)."""
    b = nbits(p)
    m = closed_form_macros(p, g, d)
    lad = 1 if b == 2 else 2*b-3
    nonmacro_F = (lad*g*(g+1)//2 + g*(g+1)//2 + g*(g-1)//2 + b*fredkin_count(g)
                  + 2*b*g + b*g*(g-1) + b*g*(g+1)//2)
    sc = formula_counts(p, -1 % p)["add_scaled_ccx"]
    return 2*nonmacro_F + m["add_product"]*(40*b*b+2*b) + m["add_scaled"]*sc


def closed_form_qubits(p, g, d):
    """Peak qubits: inputs g(g+1)b, outputs (g+1)b, arith ancillas 3b+5,
    ladder temps max(0, b-2), workspace matrix g(g+1)b, history per step
    (u^-1, w, wi, g-1 multipliers) (g+2)b, flags 1 + sum_k (3(g-k)) = 1 + 3g(g+1)/2,
    z (g+1)b, plus the peak register pool: one normalisation register, and
    the longer of the two square-and-multiply chains (I_p or E_e registers)."""
    b = nbits(p)
    m = closed_form_macros(p, g, d)
    pool = max(m["I_p"], m["E_e"], 1)
    return (g*(g+1)*b + (g+1)*b + anc_size(b) + max(0, b-2) + g*(g+1)*b
            + g*(g+2)*b + 1 + 3*g*(g+1)//2 + (g+1)*b + pool*b)


# ====================================================================== simulator

class BitSim:
    """Exact bit-sliced simulation of a permutation gate list on N basis
    inputs at once (bit n of row w = value of wire w on input n)."""

    def __init__(self, nwires, N):
        self.N = N
        self.nwords = (N+63)//64
        self.S = np.zeros((nwires, self.nwords), dtype=np.uint64)
        self.loc = list(range(nwires))

    def load(self, reg, vals):
        vals = np.asarray(vals, dtype=np.int64)
        for j, w in enumerate(reg):
            bits = ((vals >> j) & 1).astype(np.uint8)
            packed = np.packbits(bits, bitorder="little")
            buf = np.zeros(self.nwords*8, dtype=np.uint8)
            buf[:packed.size] = packed
            self.S[self.loc[w]] ^= buf.view(np.uint64)

    def read(self, reg):
        out = np.zeros(self.N, dtype=np.int64)
        for j, w in enumerate(reg):
            bits = np.unpackbits(self.S[self.loc[w]].view(np.uint8), bitorder="little")[:self.N]
            out |= bits.astype(np.int64) << j
        return out

    def wire_nonzero(self, w):
        bits = np.unpackbits(self.S[self.loc[w]].view(np.uint8), bitorder="little")[:self.N]
        return bool(bits.any())

    def run(self, gates):
        S, loc = self.S, self.loc
        for name, q in gates:
            if name == "cx":
                S[loc[q[1]]] ^= S[loc[q[0]]]
            elif name == "ccx":
                S[loc[q[2]]] ^= S[loc[q[0]]] & S[loc[q[1]]]
            elif name == "x":
                np.invert(S[loc[q[0]]], out=S[loc[q[0]]])
            elif name == "swap":
                a, b = q
                loc[a], loc[b] = loc[b], loc[a]
            else:
                raise ValueError(name)


def all_inputs(p, g):
    """All p^(g(g+1)) canonical inputs as an array (N, g, g+1)."""
    m = g*(g+1)
    N = p**m
    idx = np.arange(N, dtype=np.int64)
    A = np.zeros((N, g, g+1), dtype=np.int64)
    for t in range(m):
        r, c = divmod(t, g+1)
        A[:, r, c] = (idx // p**t) % p
    return A


def structured_inputs(p, g, n, seed=0):
    """Random inputs biased to rank deficiency: each column is random, zero,
    a copy, or a random combination of earlier columns."""
    rng = np.random.default_rng(seed)
    A = rng.integers(0, p, size=(n, g, g+1), dtype=np.int64)
    for c in range(g+1):
        mode = rng.integers(0, 4, size=n)
        A[mode == 1, :, c] = 0
        if c:
            for i in np.nonzero(mode >= 2)[0]:
                coef = rng.integers(0, p, size=c)
                if mode[i] == 2:
                    coef = np.zeros(c, dtype=np.int64)
                    coef[rng.integers(0, c)] = rng.integers(1, p)
                A[i, :, c] = A[i, :, :c] @ coef % p
    return A


def check_circuit(circ, A, gates=None):
    """Run the circuit on inputs A (N, g, g+1). Returns a dict: output equals
    canonical_witness_batch, inputs restored, every workspace wire 0,
    witness nonzero and satisfying the equation."""
    p, g, d = circ.p, circ.g, circ.d
    N = A.shape[0]
    sim = BitSim(circ.nw, N)
    for c in range(g+1):
        for r in range(g):
            sim.load(circ.L[c][r], A[:, r, c])
    gates = circ.flatten() if gates is None else gates
    t0 = time.time()
    sim.run(gates)
    dt = time.time()-t0
    s = np.stack([sim.read(circ.S[c]) for c in range(g+1)], axis=1)
    ref = canonical_witness_batch(p, A, d)
    inputs_ok = all(np.array_equal(sim.read(circ.L[c][r]), A[:, r, c])
                    for c in range(g+1) for r in range(g))
    work_clean = not any(sim.wire_nonzero(w) for w in range(circ.nw) if w not in circ.io_wires)
    sd = np.array([pow(x, d, p) for x in range(p)], dtype=np.int64)[s]
    eq_ok = bool(np.all(np.einsum("nrc,nc->nr", A, sd) % p == 0))
    nonzero = bool(np.all(s.any(axis=1)))
    return {"p": p, "g": g, "d": d, "e": circ.e, "inputs": int(N), "gates": len(gates),
            "qubits": circ.nw, "output_equals_canonical": bool(np.array_equal(s, ref)),
            "inputs_restored": inputs_ok, "workspace_clean": work_clean,
            "witness_nonzero": nonzero, "equation_holds": eq_ok,
            "canonical_padding_free": bool(np.all(s < p)), "sim_seconds": round(dt, 3)}


def exhaustive_check(p, g, d):
    circ = CoherentSDE(p, g, d)
    return check_circuit(circ, all_inputs(p, g))


def sampled_check(p, g, d, n=4096, seed=0):
    circ = CoherentSDE(p, g, d)
    return check_circuit(circ, structured_inputs(p, g, n, seed))


def count_row(p, g, d):
    circ = CoherentSDE(p, g, d)
    c = circ.counts()
    m = closed_form_macros(p, g, d)
    return {"p": p, "b": circ.b, "g": g, "d": d, "e": circ.e, **c, **{"closed_" + k: v for k, v in m.items()},
            "closed_toffoli": closed_form_toffoli(p, g, d),
            "closed_qubits": closed_form_qubits(p, g, d),
            "toffoli_matches": c["gates"].get("ccx", 0) == closed_form_toffoli(p, g, d),
            "macros_match": (c["add_product"], c["add_scaled"]) == (m["add_product"], m["add_scaled"]),
            "qubits_match": c["qubits"] == closed_form_qubits(p, g, d)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    res = {"status": STATUS, "exhaustive": [], "sampled": [], "counts": []}
    ex = [(3, 1, 1), (3, 1, 3), (5, 1, 3), (7, 1, 5), (3, 2, 1), (3, 2, 3), (5, 2, 1), (5, 2, 3),
          (7, 2, 1), (7, 2, 5), (3, 3, 3)]
    if not args.quick:
        ex += [(11, 2, 3), (13, 2, 5)]
    for p, g, d in ex:
        r = exhaustive_check(p, g, d)
        print(json.dumps(r), flush=True)
        res["exhaustive"].append(r)
    for p, g, d in [(5, 3, 3), (7, 3, 5), (11, 3, 7), (13, 3, 5), (5, 4, 3), (7, 4, 5)]:
        r = sampled_check(p, g, d, n=8192, seed=p*100+g)
        print(json.dumps(r), flush=True)
        res["sampled"].append(r)
    for p in (3, 5, 7, 13, 101, 1031, 65537, 2**31-1, 2**61-1):
        d = next(dd for dd in range(3, 200, 2) if math.gcd(dd, p-1) == 1) if p > 3 else 3
        for g in (2, 4, 8, 16):
            r = count_row(p, g, d)
            print(json.dumps({k: r[k] for k in ("p", "b", "g", "d", "add_product", "qubits",
                                                 "toffoli_matches", "macros_match", "qubits_match")}
                             | {"total": r["gates"]["total"], "ccx": r["gates"].get("ccx")}))
            res["counts"].append(r)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
