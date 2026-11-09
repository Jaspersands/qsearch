"""Approximate QFT over Z/N (N odd, N = p or p^e) with clean workspace and an
explicit gate count, emitted as Qiskit circuits. AI-checked, pending human review.

Report: research/audits/reviews/2026-11-04-rees-qft-mod.md (construction,
proofs, numbers). This module is new; no existing file is edited.

Target. For b = ceil(log2 N) and the canonical subspace span{|0>,...,|N-1>} of
a b-qubit register X, the ideal map is
    U |x>_X |0>_anc = (QFT_N |x>)_X |0>_anc,  QFT_N |x> = N^{-1/2} sum_y w^{xy} |y>,
w = exp(2 pi i / N). The circuit V satisfies, for every unit vector psi in the
canonical subspace, || V |psi>|0> - (QFT_N psi)|0> || <= B(N, t, r, tp)
(error_bound()), all ancillas included, global phase included.

Construction (registers X, F, Z, K of b qubits, M of t qubits, W of t+b
qubits, one qubit a, and the 3b+5 arithmetic ancillas of
theorems/rees_circuit_arith.py):
 1. uniform state on F by one round of exact amplitude amplification:
    A = H^b (x) Ry(2 theta), sin^2 theta = 2^b/(4N), so the good amplitude
    (F < N and a = 1) is exactly 1/2; Q = -A S_0 A^dag S_chi; Q A|0> = |u_N>|1>,
    then X on a. theta is replaced by the tp-bit dyadic angle theta~, Ry is
    built from S, H, Phase, and the global phases are cancelled exactly;
 2. phase |x>|y> -> w^{xy}|x>|y> (approximately): Z += x*y mod N
    (add_product_ops), Phase(2 pi c_j / 2^tp) on bit j of Z with
    c_j = round(2^tp (2^j mod N)/N), uncompute Z by the reversed gate list.
    Now F holds |phi_{-x}> = QFT_N |x>, an eigenvector of S: |y> -> |y+1 mod N>
    with eigenvalue w^k, k = -x mod N;
 3. coherent phase estimation E of S on F with t bits: H^t on M, controlled
    F += 2^j mod N by bit j of M, then an approximate inverse QFT over Z/2^t
    that drops every controlled rotation CR_k with k > r (output bit i of l on
    qubit M[t-1-i]);
 4. decode k~ = round(l N / 2^t) mod N into K (W = l*N + 2^(t-1) by
    shift-and-add, K = top b bits of W, K := 0 if K = N), X += K mod N
    (X becomes 0 whenever k~ = k), uncompute K and W, then E^{-1};
 5. swap X and F.
Every arithmetic block is a permutation of basis states built from X, CX,
CCX and SWAP; the only non-permutation gates are H, R_k = Phase(2 pi/2^k)
and controlled CR_k^{+-1} with k <= max(r, tp).

What this does NOT show: a fixed finite gate set (R_k for k up to
max(r, tp) = O(log((b + log 1/eta)/eta)) are used as primitives; Clifford+T
synthesis is not done); the Rees circuit generator still uses an exact QFT_p
(it is not edited); a coherent receiver; anything about the oracle.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
import math
import time

import mpmath
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import AncillaRegister, CircuitInstruction
from qiskit.circuit.library import CCXGate, CPhaseGate, CXGate, HGate, PhaseGate, SwapGate, XGate

from theorems.rees_circuit_arith import (
    Anc, Ops, add_product_ops, anc_size, cuccaro_add, less_than_p, load_const, mod_add_reg,
)

STATUS = {
    "status": "approximate_qft_mod_N_explicit_gate_count_finite_checks",
    "qft_mod_N_explicit_construction": True,
    "qft_poly_log_p_implemented": True,          # as a standalone module only
    "rees_generator_uses_this_qft": False,        # rees_circuit_general/arith unchanged
    "fixed_finite_gate_set": False,               # R_k with k <= max(r, tp) are primitives
    "coherent_receiver_implemented": False, "general_sde_implemented": False,
    "formal_compiler_checked": False, "independent_review": False,
    "novelty_established": False, "speedup_claim_allowed": False,
    "review": "AI-checked, pending human review",
}


def _pc(n):
    return bin(n).count("1")


# ====================================================================== gate lists

class QOps(Ops):
    """Gate list: classical entries (name, qubits) as in rees_circuit_arith.Ops,
    plus ("h", (q,)), ("r", (q,), k, s) = Phase(s 2pi/2^k) and
    ("cr", (c, q), k, s) = controlled Phase(s 2pi/2^k), s = +-1."""

    def h(self, q):
        self.append(("h", (q,)))

    def r(self, q, k, sign=1):
        self.append(("r", (q,), k, sign))

    def cr(self, c, q, k, sign=1):
        self.append(("cr", (c, q), k, sign))

    def phase(self, q, num, k):
        """Phase(2 pi num / 2^k) as a product of R_{k-i} over the set bits i of num mod 2^k."""
        num %= 1 << k
        for i in range(k):
            if num >> i & 1:
                self.r(q, k-i)

    def inverse(self):
        return inverse_ops(self)


def inverse_ops(ops):
    out = QOps()
    for g in reversed(ops):
        if g[0] in ("r", "cr"):
            out.append((g[0], g[1], g[2], -g[3]))
        else:
            out.append(g)
    return out


@dataclass
class Layout:
    N: int
    b: int
    t: int
    X: list
    F: list
    Z: list
    K: list
    M: list
    W: list
    a: int
    anc: list
    nq: int

    def regs(self):
        return [("x", self.X), ("f", self.F), ("z", self.Z), ("k", self.K), ("m", self.M),
                ("w", self.W), ("a", [self.a]), ("arith", self.anc)]


def make_layout(N, t):
    if N < 3 or N % 2 == 0:
        raise ValueError("N must be odd and >= 3")
    b = (N-1).bit_length()
    nxt = iter(range(10**6))
    take = lambda n: [next(nxt) for _ in range(n)]
    X, F, Z, K, M, W = take(b), take(b), take(b), take(b), take(t), take(t+b)
    a = next(nxt)
    anc = take(anc_size(b))
    return Layout(N, b, t, X, F, Z, K, M, W, a, anc, 8*b+2*t+6)


# ====================================================================== parameters

def theta_dyadic(N, tp):
    """theta = arcsin(sqrt(2^b/(4N))) and c with theta~ = 2 pi c / 2^tp nearest to theta."""
    b = (N-1).bit_length()
    with mpmath.workprec(256):
        th = mpmath.asin(mpmath.sqrt(mpmath.mpf(2**b)/(4*N)))
        c = int(mpmath.nint(th*2**tp/(2*mpmath.pi)))
        tht = 2*mpmath.pi*c/mpmath.mpf(2**tp)
        return th, c, tht


def phase_numerators(N, tp):
    b = (N-1).bit_length()
    # c_j = round(2^tp (2^j mod N) / N), exact integer rounding (half up), reduced mod 2^tp
    return [((2*(1 << tp)*pow(2, j, N) + N)//(2*N)) % (1 << tp) for j in range(b)]


def params_for_eta(N, eta):
    """(t, r, tp) with error_bound(...)['B_simple'] <= eta (proved in the report, Corollary 8)."""
    b = (N-1).bit_length()
    tp = math.ceil(math.log2(3*math.pi*(b+3)/eta))
    t = math.ceil(math.log2(36*N/eta**2))
    r = math.ceil(math.log2(6*math.sqrt(2)*math.pi*t/eta))
    return t, r, tp


def error_bound(N, t, r, tp):
    """Proved bound on ||(V - U)(Pi (x) |0>)|| (report, Theorem 6), by components.
    B uses the exact prep and phase errors; B_simple the closed forms."""
    b = (N-1).bit_length()
    th, c, tht = theta_dyadic(N, tp)
    with mpmath.workprec(256):
        rho = mpmath.sqrt(mpmath.mpf(N)/2**b)
        alt = mpmath.asin(rho*mpmath.sin(tht))
        prep = float(abs(2*mpmath.sin((mpmath.pi/2-3*alt)/2)))
        prep_lin = float(3*abs(th-tht))
    cs = phase_numerators(N, tp)
    errs = []
    for j in range(b):
        d = (pow(2, j, N)*(1 << tp) - cs[j]*N) / (N*(1 << tp))      # exact-ish rational difference
        d -= round(d)
        errs.append(2*math.pi*abs(d))
    phase_sum = sum(errs)
    if N <= 1 << 16:     # exact max over z < N (float); otherwise the proved sum bound
        phase_max = max(abs(np.exp(2j*math.pi*z/N) - np.exp(2j*math.pi*sum(((z >> j) & 1)*cs[j] for j in range(b))/2**tp))
                        for z in range(N))
    else:
        phase_max = phase_sum
    D = 2**t
    a = D/(2*N)
    pe = math.sqrt(0.5*(1/a+1/a**2))
    aq = sum((t-k+1)*2*math.sin(math.pi/2**k) for k in range(r+1, t+1))
    B = prep + phase_max + math.sqrt(2)*(pe+aq)
    B_simple = (3+b)*math.pi/2**tp + math.sqrt(2)*(math.sqrt(0.5*(1/a+1/a**2)) + 2*math.pi*max(t-r, 0)/2**r)
    return {"prep": prep, "prep_linear_bound": prep_lin, "phase_max": float(phase_max), "phase_sum_bound": phase_sum,
            "pe_tail": pe, "aqft": aq, "erase": math.sqrt(2)*(pe+aq), "B": B, "B_simple": B_simple}


# ====================================================================== construction

def _mcz(ops, qs, chain):
    """Phase -1 on |1...1> of qs (len >= 2), Toffoli chain on clean qubits `chain`."""
    n = len(qs)
    if n == 2:
        ops.cr(qs[0], qs[1], 1)
        return
    up = QOps()
    up.ccx(qs[0], qs[1], chain[0])
    for i in range(2, n-1):
        up.ccx(chain[i-2], qs[i], chain[i-1])
    ops += up
    ops.cr(chain[n-3], qs[n-1], 1)
    ops += up.inverse()


def prep_ops(L, tp):
    """|0>_F |0>_a -> |u_N>_F |0>_a (approximately), ancillas clean."""
    N, b, F, a = L.N, L.b, L.F, L.a
    A = Anc(L.anc, b)
    _, c, _ = theta_dyadic(N, tp)
    Ap = QOps()
    for q in F:
        Ap.h(q)
    Ap.phase(a, 3, 2)             # S^dag
    Ap.h(a)
    Ap.phase(a, 2*c, tp)          # Phase(2 theta~)
    Ap.h(a)
    Ap.phase(a, 1, 2)             # S      -> e^{i theta~} Ry(2 theta~)
    ops = QOps()
    ops += Ap                                     # A'
    less_than_p(ops, N, F, A, A.h)                # S_chi = I - 2 [F < N][a = 1]
    ops.cr(A.h, a, 1)
    less_than_p(ops, N, F, A, A.h)
    ops += Ap.inverse()                           # A'^dag
    for q in F+[a]:                               # S_0 = I - 2|0><0|
        ops.x(q)
    _mcz(ops, F+[a], A.r)
    for q in F+[a]:
        ops.x(q)
    ops += Ap                                     # A'
    beta = ((1 << (tp-1)) - c) % (1 << tp)        # e^{i(pi - theta~)} X_a = Phase X Phase
    ops.phase(a, beta, tp)
    ops.x(a)
    ops.phase(a, beta, tp)
    return ops


def phase_ops(L, tp):
    """|x>|y> -> exp(2 pi i sum_j z_j c_j / 2^tp)|x>|y>, z = xy mod N (Z clean before and after)."""
    A = Anc(L.anc, L.b)
    mul = add_product_ops(L.N, L.Z, L.X, L.F, 1, A)
    ops = QOps()
    ops += mul
    for j, cj in enumerate(phase_numerators(L.N, tp)):
        ops.phase(L.Z[j], cj, tp)
    ops += inverse_ops(mul)
    return ops


def aqft_inv_ops(M, r):
    """Approximate inverse QFT over Z/2^t on M (input bit j on M[j], output bit i of l
    on M[t-1-i]); CR_k^{-1} with k > r dropped."""
    t = len(M)
    ops = QOps()
    for s in range(t-1, -1, -1):
        ops.h(M[s])
        for j in range(s-1, -1, -1):
            k = s+1-j
            if k <= r:
                ops.cr(M[j], M[s], k, -1)
    return ops


def pe_ops(L, r):
    A = Anc(L.anc, L.b)
    ops = QOps()
    for q in L.M:
        ops.h(q)
    for j, mj in enumerate(L.M):
        cj = pow(2, j, L.N)
        load_const(ops, cj, A.Y, (mj,))
        mod_add_reg(ops, L.N, A.Y, L.F, A, mj)      # F += 2^j mod N controlled on m_j
        load_const(ops, cj, A.Y, (mj,))
    ops += aqft_inv_ops(L.M, r)
    return ops


def decoder_ops(L):
    """K = round(l N / 2^t) mod N from l (bit i on M[t-1-i]); W, Z (as padding) used."""
    N, b, t = L.N, L.b, L.t
    A = Anc(L.anc, b)
    lb = [L.M[t-1-i] for i in range(t)]
    ops = QOps()
    ops.x(L.W[t-1])                                  # W = 2^(t-1)
    for i in range(b):
        if N >> i & 1:
            cuccaro_add(ops, lb+L.Z[:b-i], L.W[i:t+b], A.c0, A.e)   # W += l 2^i
    whi = L.W[t:t+b]
    for i in range(b):
        ops.cx(whi[i], L.K[i])
    less_than_p(ops, N, L.K, A, A.h)                 # h = [K < N]
    ops.x(A.h)                                       # h = [K == N]
    load_const(ops, N, L.K, (A.h,))                  # K = 0 if K == N
    ops.x(A.h)
    less_than_p(ops, N, whi, A, A.h)                 # h = 0
    return ops


def qft_mod_ops(N, t, r, tp, inverse=False):
    L = make_layout(N, t)
    A = Anc(L.anc, L.b)
    blocks = {}
    blocks["prep"] = prep_ops(L, tp)
    blocks["phase"] = phase_ops(L, tp)
    pe = pe_ops(L, r)
    dec = decoder_ops(L)
    blocks["pe"] = pe
    blocks["decode"] = dec
    sub = QOps()
    mod_add_reg(sub, N, L.K, L.X, A)                 # X += k~ mod N
    blocks["erase_add"] = sub
    blocks["undecode"] = dec.inverse()
    blocks["unpe"] = pe.inverse()
    sw = QOps()
    for i in range(L.b):
        sw.swap(L.X[i], L.F[i])
    blocks["swap"] = sw
    ops = QOps()
    for name in ("prep", "phase", "pe", "decode", "erase_add", "undecode", "unpe", "swap"):
        ops += blocks[name]
    if inverse:
        ops = ops.inverse()
    return ops, L, blocks


# ====================================================================== counts

def gate_counts(ops):
    c = Counter()
    for g in ops:
        if g[0] in ("r", "cr"):
            c[g[0]] += 1
            c[f"{g[0]}{g[2]}"] += 1
        else:
            c[g[0]] += 1
    c["total"] = sum(c[k] for k in ("x", "cx", "ccx", "swap", "h", "r", "cr"))
    c["max_k"] = max([g[2] for g in ops if g[0] in ("r", "cr")], default=0)
    return dict(c)


def gate_bound(b, t, r, tp):
    """Closed-form upper bound on the total gate count (report, Proposition 7)."""
    return 328*b*b+92*b*t+2*t*r+b*tp+5*tp+26*t+240*b+60


def gate_bound_eta(N, eta):
    b = (N-1).bit_length()
    t, r, tp = params_for_eta(N, eta)
    return gate_bound(b, t, r, tp)


# ====================================================================== Qiskit emission

def to_qiskit(ops, L, name="qft_mod"):
    regs = []
    for nm, qs in L.regs():
        regs.append(QuantumRegister(len(qs), nm) if nm == "x" else AncillaRegister(len(qs), nm))
    qc = QuantumCircuit(*regs, name=f"{name}_{L.N}")
    Q = qc.qubits
    assert len(Q) == L.nq
    cache = {}
    for g in ops:
        nm = g[0]
        if nm == "x":
            op = XGate()
        elif nm == "cx":
            op = CXGate()
        elif nm == "ccx":
            op = CCXGate()
        elif nm == "swap":
            op = SwapGate()
        elif nm == "h":
            op = HGate()
        elif nm in ("r", "cr"):
            key = (nm, g[2], g[3])
            if key not in cache:
                ang = g[3]*2*math.pi/2**g[2]
                cache[key] = PhaseGate(ang) if nm == "r" else CPhaseGate(ang)
            op = cache[key]
        else:
            raise ValueError(nm)
        qc._append(CircuitInstruction(op, tuple(Q[i] for i in g[1])))
    return qc


def qft_mod_circuit(N, t, r, tp, inverse=False):
    """Qiskit circuit for the approximate QFT_N (or its inverse). Register 'x' is the
    data register (LSB first); every ancilla register starts and ends at 0."""
    ops, L, _ = qft_mod_ops(N, t, r, tp, inverse)
    return to_qiskit(ops, L), L


# ====================================================================== sparse simulator

def compile_qiskit(qc):
    """Qiskit circuit -> list of tuples for SparseState (only x, cx, ccx, swap, h, p, cp)."""
    idx = {q: i for i, q in enumerate(qc.qubits)}
    out = []
    for inst in qc.data:
        nm = inst.operation.name
        qs = [idx[q] for q in inst.qubits]
        wo = [(q // 64, q % 64) for q in qs]
        if nm in ("x", "h"):
            out.append((nm, *wo[0]))
        elif nm in ("cx", "swap"):
            out.append((nm, *wo[0], *wo[1]))
        elif nm == "ccx":
            out.append((nm, *wo[0], *wo[1], *wo[2]))
        elif nm == "p":
            out.append((nm, *wo[0], np.exp(1j*float(inst.operation.params[0]))))
        elif nm == "cp":
            out.append((nm, *wo[0], *wo[1], np.exp(1j*float(inst.operation.params[0]))))
        else:
            raise ValueError(f"unsupported gate {nm}")
    return out


class SparseState:
    """State as parallel arrays of multiword uint64 basis keys and complex amplitudes.
    Permutation gates act on keys, diagonal gates on amplitudes, H merges equal keys.
    Amplitudes with |a| < tol after an H are dropped and their squared norm recorded."""

    def __init__(self, nq, init_keys, amps=None, tol=1e-13):
        self.W = (nq+63)//64
        init_keys = list(init_keys)
        self.keys = [np.array([(k >> (64*w)) & ((1 << 64)-1) for k in init_keys], dtype=np.uint64)
                     for w in range(self.W)]
        self.amps = np.ones(len(init_keys), dtype=complex) if amps is None else np.asarray(amps, dtype=complex)
        self.tol = tol
        self.pruned = 0.0
        self.prune_err = 0.0      # sum over H steps of sqrt(pruned mass): bounds the 2-norm deviation
        self.max_support = len(init_keys)

    def _bit(self, w, o):
        return (self.keys[w] >> np.uint64(o)) & np.uint64(1)

    def run(self, gates):
        for g in gates:
            nm = g[0]
            K = self.keys
            if nm == "x":
                K[g[1]] ^= np.uint64(1 << g[2])
            elif nm == "cx":
                K[g[3]] ^= self._bit(g[1], g[2]) << np.uint64(g[4])
            elif nm == "ccx":
                K[g[5]] ^= (self._bit(g[1], g[2]) & self._bit(g[3], g[4])) << np.uint64(g[6])
            elif nm == "swap":
                d = self._bit(g[1], g[2]) ^ self._bit(g[3], g[4])
                K[g[1]] ^= d << np.uint64(g[2])
                K[g[3]] ^= d << np.uint64(g[4])
            elif nm == "p":
                m = self._bit(g[1], g[2]).astype(bool)
                self.amps[m] *= g[3]
            elif nm == "cp":
                m = (self._bit(g[1], g[2]) & self._bit(g[3], g[4])).astype(bool)
                self.amps[m] *= g[5]
            elif nm == "h":
                self._h(g[1], g[2])
            else:
                raise ValueError(nm)
        return self

    def _h(self, w, o):
        K = self.keys
        bit = np.uint64(1 << o)
        bv = ((K[w] >> np.uint64(o)) & np.uint64(1)).astype(bool)
        base = [k.copy() for k in K]
        base[w] &= ~bit
        if self.W == 1:
            u, inv = np.unique(base[0], return_inverse=True)
            ukeys = [u]
        else:
            arr = np.ascontiguousarray(np.stack(base, axis=1))
            v = arr.view(np.dtype((np.void, 8*self.W))).ravel()
            u, inv = np.unique(v, return_inverse=True)
            uu = u.view(np.uint64).reshape(-1, self.W)
            ukeys = [np.ascontiguousarray(uu[:, i]) for i in range(self.W)]
        inv = inv.ravel()
        n = len(ukeys[0])
        a = self.amps
        a0 = np.bincount(inv, weights=np.where(bv, 0, a.real), minlength=n) + \
            1j*np.bincount(inv, weights=np.where(bv, 0, a.imag), minlength=n)
        a1 = np.bincount(inv, weights=np.where(bv, a.real, 0), minlength=n) + \
            1j*np.bincount(inv, weights=np.where(bv, a.imag, 0), minlength=n)
        s = 1/math.sqrt(2)
        new_amps = np.concatenate([s*(a0+a1), s*(a0-a1)])
        new_keys = []
        for i in range(self.W):
            k1 = ukeys[i].copy()
            if i == w:
                k1 |= bit
            new_keys.append(np.concatenate([ukeys[i], k1]))
        keep = np.abs(new_amps) >= self.tol
        pm = float(np.sum(np.abs(new_amps[~keep])**2))
        self.pruned += pm
        self.prune_err += math.sqrt(pm)
        self.keys = [k[keep] for k in new_keys]
        self.amps = new_amps[keep]
        self.max_support = max(self.max_support, len(self.amps))

    def key_ints(self):
        out = np.zeros(len(self.amps), dtype=object)
        for w in range(self.W):
            out = out + (self.keys[w].astype(object) << (64*w))
        return out


def classical_eval(gates, nq, inputs):
    """Apply a permutation-only compiled gate list to integer basis inputs; returns integers."""
    st = SparseState(nq, inputs)
    st.run(gates)
    return list(st.key_ints())


def ops_to_gates(ops, nq):
    """QOps -> compiled tuples (no Qiskit), for fast block tests."""
    out = []
    for g in ops:
        nm = g[0]
        wo = [(q // 64, q % 64) for q in g[1]]
        if nm in ("x", "h"):
            out.append((nm, *wo[0]))
        elif nm in ("cx", "swap"):
            out.append((nm, *wo[0], *wo[1]))
        elif nm == "ccx":
            out.append((nm, *wo[0], *wo[1], *wo[2]))
        elif nm == "r":
            out.append(("p", *wo[0], np.exp(1j*g[3]*2*math.pi/2**g[2])))
        elif nm == "cr":
            out.append(("cp", *wo[0], *wo[1], np.exp(1j*g[3]*2*math.pi/2**g[2])))
        else:
            raise ValueError(nm)
    return out


# ====================================================================== verification

def operator_error(N, t, r, tp, inverse=False, tol=1e-13, via_qiskit=True, log=None):
    """Float check: sigma_max of (V - U) restricted to canonical inputs |x>|0>, x < N,
    over the full output space (all ancillas). Simulates the emitted Qiskit circuit."""
    t0 = time.time()
    ops, L, _ = qft_mod_ops(N, t, r, tp, inverse)
    if via_qiskit:
        qc = to_qiskit(ops, L)
        gates = compile_qiskit(qc)
    else:
        gates = ops_to_gates(ops, L.nq)
    sign = -1 if inverse else 1
    rows_k, rows_v, cols = [], [], []
    pruned, maxsup, perr = 0.0, 0, 0.0
    for x in range(N):
        st = SparseState(L.nq, [x], tol=tol).run(gates)   # X occupies qubits 0..b-1
        pruned = max(pruned, st.pruned)
        perr = max(perr, st.prune_err)
        maxsup = max(maxsup, st.max_support)
        stk = np.stack(st.keys, axis=1) if st.W > 1 else st.keys[0][:, None]
        ideal = np.zeros((N, st.W), dtype=np.uint64)
        ideal[:, 0] = np.arange(N, dtype=np.uint64)
        iamp = np.exp(sign*2j*math.pi*x*np.arange(N)/N)/math.sqrt(N)
        rows_k.append(np.concatenate([stk, ideal]))
        rows_v.append(np.concatenate([st.amps, -iamp]))
        cols.append(np.full(len(st.amps)+N, x))
        if log:
            log(f"  N={N} x={x} support={len(st.amps)} max={st.max_support} {time.time()-t0:.1f}s")
    allk = np.ascontiguousarray(np.concatenate(rows_k))
    v = allk.view(np.dtype((np.void, 8*allk.shape[1]))).ravel()
    _, rid = np.unique(v, return_inverse=True)
    rid = rid.ravel()
    vals = np.concatenate(rows_v)
    col = np.concatenate(cols)
    from scipy.sparse import coo_matrix
    E = coo_matrix((vals, (rid, col)), shape=(rid.max()+1, N)).tocsc()
    Gm = (E.conj().T @ E).toarray()
    ev = np.linalg.eigvalsh((Gm+Gm.conj().T)/2)
    sigma = float(math.sqrt(max(ev[-1], 0.0)))
    colmax = float(math.sqrt(max(np.real(np.diag(Gm)))))
    bd = error_bound(N, t, r, tp)
    cnt = gate_counts(ops)
    return {"N": N, "b": L.b, "t": t, "r": r, "tp": tp, "inverse": inverse, "qubits": L.nq,
            "sigma_max": sigma, "max_column_error": colmax, "bound": bd,
            "pruned_mass_max": pruned, "prune_err_max": perr,
            # sigma_true <= sigma_max + sqrt(N) * prune_err_max (columnwise deviation, Frobenius)
            "sigma_upper": sigma + math.sqrt(N)*perr, "max_support": maxsup,
            "gates": cnt, "gate_bound": gate_bound(L.b, t, r, tp), "seconds": time.time()-t0}


def pe_tail_float(N, t, r):
    """Float check of max_k ||Pi_bad beta~_k|| for the implemented AQFT (dense on t qubits)."""
    D = 2**t
    M = list(range(t))
    gates = ops_to_gates(aqft_inv_ops(M, r), t)
    worst = 0.0
    for k in range(N):
        amps = np.exp(2j*math.pi*np.arange(D)*k/N)/math.sqrt(D)
        st = SparseState(t, range(D), amps, tol=0.0).run(gates)
        ks = st.key_ints()
        tot = 0.0
        for key, a in zip(ks, st.amps):
            l = sum(((int(key) >> (t-1-i)) & 1) << i for i in range(t))
            kt = ((l*N + D//2)//D) % N
            if kt != k:
                tot += abs(a)**2
        worst = max(worst, math.sqrt(tot))
    return worst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--dt", type=int, nargs="+", default=[2, 4, 6], help="t - b values")
    ap.add_argument("--r", type=int, nargs="+", default=[3, 99])
    ap.add_argument("--tp", type=int, nargs="+", default=[6, 12])
    ap.add_argument("--inverse", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    res = []
    for N in args.N:
        b = (N-1).bit_length()
        for dt in args.dt:
            for r in args.r:
                for tp in args.tp:
                    t = b+dt
                    rr = min(r, t)
                    d = operator_error(N, t, rr, tp, inverse=args.inverse)
                    d["pe_tail_float"] = pe_tail_float(N, t, rr) if t <= 14 else None
                    print(json.dumps({k: d[k] for k in ("N", "t", "r", "tp", "sigma_max", "max_column_error",
                                                       "pruned_mass_max", "seconds")},),
                          "B=%.4g" % d["bound"]["B"], "gates=%d<=%d" % (d["gates"]["total"], d["gate_bound"]),
                          flush=True)
                    res.append(d)
                    if args.out:
                        with open(args.out, "w") as f:
                            json.dump({"status": STATUS, "results": res}, f, indent=1)
    return res


if __name__ == "__main__":
    main()
