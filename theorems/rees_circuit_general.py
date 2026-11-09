"""Gate-level Qiskit circuit generator for the Rees algorithm on general (L, c, p).

Generalises theorems/rees_circuit.py (one fixed instance, Heis(F_3)) to any
Lazard Lie algebra L over F_p given by structure constants, of class c < p,
with given evaluation points, a hidden subgroup H (for the oracle) and
per-grade merge arities M_d. AI-checked, pending human review.

Emitted circuits (Qiskit, qubit-only):
* source on G_c = (A, *): QFT_p on every cover coordinate, then for each
  evaluation point s: w += E_s(a), coherent table oracle U_f(w, y_s),
  w -= E_s(a) (uncomputed evaluation workspace);
* complete central instrument at grade d: per top coordinate an ancilla
  QFT_p, the controlled central subtraction a_top -= z, inverse QFT_p;
* controlled right translation x -> x * (-delta_s(sigma(q))) on G_d, with the
  class-d BCH law compiled to reversible F_p arithmetic: the BCH series is
  written in right-nested brackets (Dynkin-Specht-Wever, derived and checked
  exactly in the free associative algebra), each distinct suffix bracket is
  computed into its own workspace, and the four-pass Bennett schedule of
  thm:uniform-compilation(ii) is used (compute-copy-uncompute, swap, erase);
* abelian Fourier sampling (QFT_p on every grade-one coordinate).
The SDE solve between quantum segments is a classical step: the deterministic
Ivanyos-Santha solver of theorems/rees_is_sde_solver.py whenever the merge
arity reaches its column count, otherwise brute force over F_p^M.

Encoding. Each F_p coordinate is b = ceil(log2 p) qubits, value sum_i b_i 2^i;
words >= p are padding. Arithmetic uses only X, CX, multi-controlled X and
SWAP, so it is an exact permutation of basis states. A controlled increment
t += k is a product of p-1 transpositions of t's words, each a Gray-code
conjugated MCX that fixes every other word of t; a control "qudit = v" tests
the smallest set of bits that singles v out among the canonical words. For
p = 3 this reproduces theorems/rees_circuit.py gate for gate. QFT_p is one
exact b-qubit unitary F_p + identity on padding (small p only).

Exact simulation (modules from their own gate lists, then composed through
the tensor / Schur structure of prop:descent):
* source: bit-sliced exact evaluation of the permutation part on ALL
  canonical addresses (QFT head checked to be QFT_p on |0>); gives the label
  fibres, so the address density is 1_S-coset exactly; S, the fibres and the
  clean workspace are all checked;
* instrument: per top coordinate, the Operator of its own (2b)-qubit gate
  block (the block partition is checked); its Kraus operators are checked
  to be central-translation circulants. By default (INSTRUMENT_EXPONENTS =
  "exact") the block is evaluated in Z[zeta_p] with integer coefficients (QFT_p
  as zeta^(vw)/sqrt(p), permutation gates as integer permutations) and the
  exponents are read off exact monomials, with no floating point; the original
  float path (Operator, angle, rounding to |err| < 1e-9) is kept as "float";
* merge: each arithmetic macro's gate slice is checked exhaustively on its
  qudits, the macro program is replayed symbolically over F_p[q, x] and
  compared with the classical BCH polynomial (proof on ALL canonical inputs),
  and the whole gate list is also run bit-sliced (merge_bitlevel: all inputs,
  or a chosen set of q rows with all x);
* states: left-invariant densities rho[x, y] = phi(x^-1 y)/|G| stored as
  exact Z[zeta_p] vectors; conditioning, Schur-product merges (checked to
  descend: constant on central fibres) and Fourier readout are exact.

What this does NOT show: anything asymptotic; a coherent receiver
(coherent_receiver_implemented stays false); finite-gate QFT synthesis;
poly(log p) arithmetic (the value-controlled increments cost O(p^3 log p)
gates per multiply, a small-p construction); noise; the oracle cost T_f.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import json
from math import factorial, gcd, prod
import random
import time

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit import ControlledGate, Gate
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

from theorems.rees_end_to_end_sim import (
    LieAlgebra, brute_force_sde, cyc_canon, cyc_mul, cyc_rational, expected_label_support,
    filiform4, graded_hidden, heisenberg, lie_from_brackets, make_cover, nullspace, pow_mod, rref,
    span_elements,
)
from theorems.rees_is_sde_solver import columns_required, is_sde_solve

TOL = 1e-9
STATUS = {"status": "gate_level_circuit_generator_simulated_finite_instances_not_a_coherent_receiver",
          "coherent_receiver_implemented": False, "general_sde_implemented": False,
          "formal_compiler_checked": False, "independent_review": False,
          "novelty_established": False, "speedup_claim_allowed": False,
          "review": "AI-checked, pending human review"}


# ====================================================================== BCH in right-nested brackets

def _fa_mul(A, B, c):
    out = {}
    for u, a in A.items():
        for v, b in B.items():
            if len(u)+len(v) <= c:
                out[u+v] = out.get(u+v, 0)+a*b
    return {w: x for w, x in out.items() if x}


def _right_nested(word):
    """[w1, [w2, ..., [w_(n-1), w_n]]] expanded in the free associative algebra."""
    if len(word) == 1:
        return {word: Fraction(1)}
    inner = _right_nested(word[1:])
    out = {}
    for w, x in inner.items():
        out[word[0]+w] = out.get(word[0]+w, 0)+x
        out[w+word[0]] = out.get(w+word[0], 0)-x
    return {w: x for w, x in out.items() if x}


@lru_cache(maxsize=None)
def bch_nodes(c):
    """BCH(x, y) = x + y + sum_node alpha_node [node] up to degree c.

    A node is a word a_1 ... a_(n-2) x y over {x, y}; [node] is the right-nested
    bracket [a_1, [a_2, ..., [x, y]]]. Derived from log(e^x e^y) in the free
    associative algebra with the Dynkin-Specht-Wever map (Z_n = theta(Z_n)/n)
    and CHECKED: the bracket expansion is re-expanded and compared exactly.
    Returns a tuple of (word, Fraction alpha), parents after their suffixes,
    containing every suffix needed (alpha may be 0 for pure intermediates)."""
    ex = {"x"*i+"y"*j: Fraction(1, factorial(i)*factorial(j))
          for i in range(c+1) for j in range(c+1-i) if i+j}
    Z, power = {}, dict(ex)
    for k in range(1, c+1):
        for w, x in power.items():
            Z[w] = Z.get(w, 0)+Fraction((-1)**(k+1), k)*x
        power = _fa_mul(power, ex, c)
    Z = {w: x for w, x in Z.items() if x}
    alpha = {}
    for w, x in Z.items():
        n = len(w)
        if n < 2 or w[-1] == w[-2]:
            continue
        sign, node = (1, w) if w[-2:] == "xy" else (-1, w[:-2]+"xy")
        alpha[node] = alpha.get(node, 0)+sign*x/n
    alpha = {w: a for w, a in alpha.items() if a}
    # check: x + y + sum alpha [node] == Z exactly
    recon = {"x": Fraction(1), "y": Fraction(1)}
    for w, a in alpha.items():
        for u, v in _right_nested(w).items():
            recon[u] = recon.get(u, 0)+a*v
    if {w: x for w, x in recon.items() if x} != Z:
        raise ArithmeticError("Dynkin-Specht-Wever bracket form does not reproduce BCH")
    needed = set()
    for w in alpha:
        for k in range(len(w)-1):
            needed.add(w[k:])
    return tuple((w, alpha.get(w, Fraction(0))) for w in sorted(needed, key=lambda u: (len(u), u)))


def _mod_fraction(x, p):
    if x.denominator % p == 0:
        raise ArithmeticError("BCH denominator divisible by p")
    return x.numerator*pow(x.denominator, -1, p) % p


# ====================================================================== groups (any class < p)

class GroupLaw:
    """(F_p^n, BCH product) for a nilpotent Lie tensor of class <= c < p; any c.
    Encoding as rees_end_to_end_sim.NilGroup: big-endian base-p index."""

    def __init__(self, tensor, nil_class, p):
        if not 1 <= nil_class < p:
            raise ValueError("Lazard needs class < p")
        self.p, self.c = p, nil_class
        self.tensor = np.asarray(tensor, dtype=np.int64) % p
        self.n = self.tensor.shape[0]
        self.order = p**self.n
        self._terms = [(int(i), int(j), int(k), int(self.tensor[i, j, k]))
                       for i, j, k in zip(*np.nonzero(self.tensor))]
        self._weights = p**np.arange(self.n-1, -1, -1, dtype=np.int64)
        self.nodes = [(w, _mod_fraction(a, p)) for w, a in bch_nodes(nil_class)]

    def bracket(self, X, Y):
        out = np.zeros(np.broadcast_shapes(X.shape, Y.shape), dtype=np.int64)
        for i, j, k, v in self._terms:
            out[..., k] += v*X[..., i]*Y[..., j]
        return out % self.p

    def mul(self, X, Y):
        X, Y = np.asarray(X, dtype=np.int64), np.asarray(Y, dtype=np.int64)
        out, val = X+Y, {}
        for w, a in self.nodes:
            left = X if w[0] == "x" else Y
            val[w] = self.bracket(left, Y if w == "xy" else val[w[1:]])
            if a:
                out = out+a*val[w]
        return out % self.p

    def encode(self, X):
        return (np.asarray(X, dtype=np.int64) % self.p) @ self._weights

    def decode(self, idx):
        return (np.asarray(idx, dtype=np.int64)[..., None]//self._weights) % self.p

    def elements(self):
        return self.decode(np.arange(self.order, dtype=np.int64))

    def closure(self, generators):
        gens = np.asarray(generators, dtype=np.int64).reshape(-1, self.n)
        seen = np.zeros(self.order, dtype=bool)
        seen[0] = True
        frontier = np.zeros((1, self.n), dtype=np.int64)
        while len(frontier):
            new = []
            for g in gens:
                idx = self.encode(self.mul(frontier, g[None, :]))
                idx = np.unique(idx[~seen[idx]])
                seen[idx] = True
                new.append(idx)
            frontier = self.decode(np.unique(np.concatenate(new))) if new else frontier[:0]
        return np.nonzero(seen)[0]


# ====================================================================== input: algebra, points, arities

@dataclass
class Hidden:
    """Hiding function f(x) = min index of xH, and (separately) the truth for grading."""
    name: str
    algebra: LieAlgebra
    generators: tuple
    log_h: list = field(init=False)
    oracle_table: np.ndarray = field(init=False)
    normal: bool = field(init=False)
    subgroup: np.ndarray = field(init=False)

    def __post_init__(self):
        alg = self.algebra
        law = GroupLaw(alg.tensor, len(alg.lower_central_series()), alg.p)
        self.subgroup = law.closure(self.generators) if self.generators else np.array([0])
        self.log_h = alg.lie_closure(self.generators) if self.generators else []
        if set(law.encode(span_elements(self.log_h, alg.dim, alg.p)).tolist()) != set(self.subgroup.tolist()):
            raise ArithmeticError("log of the generated subgroup is not its Lie closure")
        E = law.elements()
        table = np.full(law.order, law.order, dtype=np.int64)
        for h in law.decode(self.subgroup):
            table = np.minimum(table, law.encode(law.mul(E, h[None, :])))
        self.oracle_table = table
        self.normal = alg.is_ideal(self.log_h)


class Encoding:
    """F_p coordinates on b = ceil(log2 p) qubits; minimal value tests."""

    def __init__(self, p):
        self.p, self.nb = p, max(1, (p-1).bit_length())
        self.tests = {v: self._minimal_tests(v) for v in range(p)}

    def _minimal_tests(self, v):
        for size in range(1, self.nb+1):
            for bits in combinations(range(self.nb), size):
                hits = [u for u in range(self.p) if all((u >> i & 1) == (v >> i & 1) for i in bits)]
                if hits == [v]:
                    return [(i, v >> i & 1) for i in bits]
        raise AssertionError


def increment_sequence(p, k):
    """Transpositions whose product (applied left to right) is t -> t + k mod p."""
    k %= p
    if not k:
        return []
    if k <= (p-1)//2:
        a = [i*k % p for i in range(p)]
        return [(a[i], a[i+1]) for i in range(p-2, -1, -1)]
    return list(reversed(increment_sequence(p, p-k)))


class Config:
    """Public data of one run: cover, encoding, grade laws, BCH nodes, arities."""

    def __init__(self, algebra, points=None, arities=None):
        self.algebra, self.p = algebra, algebra.p
        self.cover = make_cover(algebra)
        p, c = self.p, self.cover.c
        self.c, self.m = c, algebra.dim
        if points is not None:
            points = tuple(int(s) % p for s in points)
            if len(set(points)) != len(points) or 0 in points:
                raise ValueError("evaluation points must be distinct and nonzero")
            self.cover.points = points
        self.points = self.cover.points
        self.enc = Encoding(p)
        self.dims = self.cover.dims
        self.width = {d: self.cover.width(d) for d in range(0, c+1)}
        self.grades = [int(g) for g in self.cover.grades]
        self.laws = {d: GroupLaw(self.cover.tensor[:self.width[d], :self.width[d], :self.width[d]], max(d, 1), p)
                     if d < p else None for d in range(1, c+1)}
        self.L_law = GroupLaw(algebra.tensor, c, p)
        default = {d: gcd(d, p-1)*self.dims[d-1]+1 for d in range(2, c+1)}
        self.arity = {**default, **(arities or {})}
        self.label_bits = max(1, (p**self.m-1).bit_length())
        self.nodes = {d: self._grade_nodes(d) for d in range(2, c+1)}

    def name(self):
        return f"{self.algebra.name} c={self.c} dims={self.dims} points={self.points} M={self.arity}"

    def top(self, d):
        return list(range(self.width[d-1], self.width[d]))

    def scales(self, d, s):
        return [pow(s, self.grades[j], self.p) for j in range(self.width[d])]

    def _grade_nodes(self, d):
        """BCH nodes for the class-d law of G_d with their output supports;
        nodes whose bracket is identically zero (with all their parents) are dropped."""
        T = self.laws[d].tensor
        n = self.width[d]
        g_supp = set(range(self.width[d-1]))        # g = -delta_s(sigma(q)) has zero top grade
        x_supp = set(range(n))
        supp, out = {}, []
        for w, a in bch_nodes(d):
            right = g_supp if w == "xy" else supp.get(w[1:])
            if right is None:
                continue
            left = x_supp if w[0] == "x" else g_supp
            s = sorted({k for i in left for j in right for k in range(n) if T[i, j, k]})
            if not s:
                continue
            supp[w] = s
            out.append((w, _mod_fraction(a, self.p), s))
        # drop intermediates with no surviving alpha != 0 descendant
        keep = {w for w, a, _ in out if a}
        changed = True
        while changed:
            changed = False
            for w, _, _ in out:
                if w not in keep and any(u != w and u.endswith(w) for u in keep):
                    keep.add(w)
                    changed = True
        return [(w, a, s) for w, a, s in out if w in keep]


# ====================================================================== gates

def qudit_register(name, n, enc):
    """QuantumRegister of b n qubits; qudit j uses qubits b(n-1-j) .. b(n-1-j)+b-1."""
    reg = QuantumRegister(enc.nb*n, name)
    return reg, [tuple(reg[enc.nb*(n-1-j)+i] for i in range(enc.nb)) for j in range(n)]


@lru_cache(maxsize=None)
def canonical_index(n, p):
    nb = max(1, (p-1).bit_length())
    digits = np.array(list(product(range(p), repeat=n)), dtype=np.int64).reshape(-1, n)
    return digits @ ((1 << nb)**np.arange(n-1, -1, -1, dtype=np.int64))


def qft_matrix(p, inverse=False):
    nb = max(1, (p-1).bit_length())
    F = np.eye(2**nb, dtype=complex)
    F[:p, :p] = np.exp(2j*np.pi*np.outer(np.arange(p), np.arange(p))/p)/np.sqrt(p)
    return F.conj().T if inverse else F


@lru_cache(maxsize=None)
def qft_gate(p, inverse=False):
    nb = max(1, (p-1).bit_length())
    sub = QuantumCircuit(nb, name=f"qft{p}_dg" if inverse else f"qft{p}")
    sub.append(UnitaryGate(qft_matrix(p, inverse)), list(range(nb)))
    return sub.to_gate()


class TableOracle(Gate):
    """U_f |w>|y> = |w>|y xor f(w)> on canonical w (padding left alone).
    Its definition is the table of fully controlled MCX gates of
    rees_circuit.oracle_gate; these gates are T_f and are not counted."""

    def __init__(self, table, m, enc, label_bits):
        super().__init__("U_f", enc.nb*m+label_bits, [])
        self.table, self.m_coords, self.enc, self.label_bits = np.asarray(table), m, enc, label_bits

    def _define(self):
        enc, m = self.enc, self.m_coords
        w_reg, w = qudit_register("w", m, enc)
        y = QuantumRegister(self.label_bits, "y")
        qc = QuantumCircuit(w_reg, y, name="U_f")
        controls = [qb for q in w for qb in q]
        for idx, digits in enumerate(product(range(enc.p), repeat=m)):
            value = int(self.table[idx])
            if not value:
                continue
            state = sum(((d >> i) & 1) << (enc.nb*j+i) for j, d in enumerate(digits) for i in range(enc.nb))
            for bit in range(self.label_bits):
                if value >> bit & 1:
                    qc.mcx(controls, y[bit], ctrl_state=state)
        self.definition = qc


class Builder:
    """Emits mod-p arithmetic as X/CX/MCX gates, counts the paper's primitives and
    records every arithmetic macro (kind, qudits, coefficient, gate slice)."""

    def __init__(self, qc, enc):
        self.qc, self.enc, self.p = qc, enc, enc.p
        self.counts = Counter()
        self.macros = []

    def _x(self, target, controls):
        if not controls:
            self.qc.x(target)
            return
        qubits = [q for q, _ in controls]
        state = sum(bit << i for i, (_, bit) in enumerate(controls))
        if len(qubits) == 1:
            self.qc.cx(qubits[0], target, ctrl_state=state)
        else:
            self.qc.mcx(qubits, target, ctrl_state=state)

    def _transposition(self, t, u, v, ext):
        nb = self.enc.nb
        diff = [i for i in range(nb) if (u ^ v) >> i & 1]
        piv = max(diff)
        if u >> piv & 1:
            u, v = v, u
        others = [i for i in diff if i != piv]
        for j in others:
            self.qc.cx(t[piv], t[j])
        self._x(t[piv], ext+[(t[i], u >> i & 1) for i in range(nb) if i != piv])
        for j in reversed(others):
            self.qc.cx(t[piv], t[j])

    def increment(self, t, k, controls=()):
        """t += k (mod p) when every control (qudit, value) holds; t's padding is fixed."""
        ext = [(q[i], bit) for q, v in controls for i, bit in self.enc.tests[v]]
        for u, v in increment_sequence(self.p, k):
            self._transposition(t, u, v, ext)

    def _macro(self, kind, qudits, coeff, start):
        self.macros.append((kind, tuple(qudits), coeff % self.p if coeff is not None else None,
                            start, len(self.qc.data)))

    def add_scaled(self, t, a, coeff):
        """t += coeff * a."""
        if not coeff % self.p:
            return
        start = len(self.qc.data)
        for v in range(1, self.p):
            self.increment(t, coeff*v, [(a, v)])
        self._macro("add_scaled", (t, a), coeff, start)

    def add_product(self, t, a, b, coeff):
        """t += coeff * a * b."""
        if not coeff % self.p:
            return
        if len({t, a, b}) != 3:
            raise ValueError("add_product needs three distinct qudits")
        start = len(self.qc.data)
        for va, vb in product(range(1, self.p), repeat=2):
            self.increment(t, coeff*va*vb, [(a, va), (b, vb)])
        self._macro("add_product", (t, a, b), coeff, start)

    def qft(self, q, role, inverse=False):
        start = len(self.qc.data)
        self.qc.append(qft_gate(self.p, inverse), list(q))
        self.counts[role] += 1
        self._macro("qft_dg" if inverse else "qft", (q,), None, start)

    def swap(self, a, b):
        start = len(self.qc.data)
        for x, y in zip(a, b):
            self.qc.swap(x, y)
        self._macro("swap", tuple(a)+tuple(b), None, start)

    def oracle(self, U, w_reg, y):
        start = len(self.qc.data)
        if U is not None:
            self.qc.append(U, list(w_reg)+list(y))
        self.counts["oracle_calls"] += 1
        self._macro("oracle", (), None, start)


# ====================================================================== modules

def evaluation_pass(cfg, B, a, w, s, inverse=False):
    """w += E_s(a) (or -=), E_s(sum_k t^k b) = sum_k s^k b; public linear map."""
    E = cfg.cover.evaluation_matrix(s)
    sign = -1 if inverse else 1
    for i in range(E.shape[0]):
        for j in range(E.shape[1]):
            if E[i, j]:
                B.add_scaled(w[j], a[i], sign*int(E[i, j]))
    B.counts["E_s_uncompute" if inverse else "E_s_compute"] += 1


def source_ops(cfg, B, a, w, labels, U, points, uncompute=True):
    for q in a:
        B.qft(q, "qft_leaf")
    for s, y in zip(points, labels):
        evaluation_pass(cfg, B, a, w, s)
        B.oracle(U, _flat_reg(w), y)            # coherent call U_f(w, y_s)
        if uncompute:
            evaluation_pass(cfg, B, a, w, s, inverse=True)


def _flat_reg(qudits):
    """Qubits of a qudit list in register order (qudit n-1 first, bit 0 first)."""
    return [qb for q in reversed(qudits) for qb in q]


def make_oracle(cfg, inst):
    return TableOracle(inst.oracle_table, cfg.m, cfg.enc, cfg.label_bits) if inst is not None else None


def source_circuit(cfg, inst, points=None, uncompute=True):
    """One lifted source on G_c: uniform address, c evaluations, c oracle calls."""
    points = cfg.points if points is None else points
    a_reg, a = qudit_register("a", cfg.width[cfg.c], cfg.enc)
    w_reg, w = qudit_register("w", cfg.m, cfg.enc)
    labels = [QuantumRegister(cfg.label_bits, f"y{s}") for s in points]
    qc = QuantumCircuit(a_reg, w_reg, *labels, name="source")
    B = Builder(qc, cfg.enc)
    source_ops(cfg, B, a, w, labels, make_oracle(cfg, inst), points, uncompute)
    return qc, B, (a_reg, a, w_reg, w, labels)


def instrument_ops(cfg, B, d, a, z):
    role = f"qft_grade{d}"
    top = cfg.top(d)
    for j in range(len(top)):
        B.qft(z[j], role)
    for j, t in enumerate(top):
        B.add_scaled(a[t], z[j], -1)            # R_z |x> = |x z^-1> = |x - z> on the centre
        B.counts["central_subtractions"] += 1
    for j in range(len(top)):
        B.qft(z[j], role, inverse=True)


def instrument_circuit(cfg, d):
    """Complete central instrument on the top grade of G_d (unmeasured)."""
    a_reg, a = qudit_register("a", cfg.width[d], cfg.enc)
    z_reg, z = qudit_register("z", cfg.dims[d-1], cfg.enc)
    qc = QuantumCircuit(a_reg, z_reg, name=f"instrument_d{d}")
    B = Builder(qc, cfg.enc)
    instrument_ops(cfg, B, d, a, z)
    return qc, B, (a_reg, a, z_reg, z)


def merge_ops(cfg, B, d, Q, x, W, bws, s, bennett=True, nodes=None):
    """In place x -> x * g, g = -delta_s(sigma(q)), class-d BCH, four Bennett passes.

    bws[node] maps each output coordinate of the node's bracket to a workspace qudit."""
    p = cfg.p
    T = cfg.laws[d].tensor
    nodes = cfg.nodes[d] if nodes is None else nodes
    nq = cfg.width[d-1]
    gcoef = [-pow(s, cfg.grades[j], p) for j in range(nq)]     # g_j = gcoef_j q_j

    def bracket_pass(u, sign_g, sign):
        """Compute (sign=+1) or uncompute (sign=-1) every node for X = u, Y = sign_g g."""
        order = nodes if sign > 0 else list(reversed(nodes))
        for w, _, supp in order:
            out = bws[w]
            for k in supp:
                if w == "xy":                               # [u, Y]_k
                    for i in range(cfg.width[d]):
                        for j in range(nq):
                            if T[i, j, k]:
                                B.add_product(out[k], u[i], Q[j], sign*int(T[i, j, k])*sign_g*gcoef[j])
                else:
                    child = bws[w[1:]]
                    for i in range(cfg.width[d]):
                        for j in child:
                            if not T[i, j, k]:
                                continue
                            if w[0] == "x":
                                B.add_product(out[k], u[i], child[j], sign*int(T[i, j, k]))
                            elif i < nq:
                                B.add_product(out[k], Q[i], child[j], sign*int(T[i, j, k])*sign_g*gcoef[i])
            B.counts["bracket_evaluations"] += 1
        B.counts["bch_passes"] += 1

    def bch_linear(u, sign_g, sign):        # W += sign * (u + Y + sum alpha [node])
        for j in range(cfg.width[d]):
            B.add_scaled(W[j], u[j], sign)
        for j in range(nq):
            B.add_scaled(W[j], Q[j], sign*sign_g*gcoef[j])
        for w, alpha, supp in nodes:
            if alpha:
                for k in supp:
                    B.add_scaled(W[k], bws[w][k], sign*alpha)

    bracket_pass(x, 1, 1)
    bch_linear(x, 1, 1)
    if bennett:
        bracket_pass(x, 1, -1)
    B.swap(x, W)                            # x = x * g, W = old x = x_new * g^-1
    bracket_pass(x, -1, 1)
    bch_linear(x, -1, -1)
    bracket_pass(x, -1, -1)
    B.counts["controlled_right_actions"] += 1


def workspace_registers(cfg, d, prefix="b", nodes=None):
    nodes = cfg.nodes[d] if nodes is None else nodes
    regs, bws = [], {}
    for idx, (w, _, supp) in enumerate(nodes):
        name = prefix if len(nodes) == 1 else f"{prefix}{idx}"
        r, qd = qudit_register(name, len(supp), cfg.enc)
        regs.append(r)
        bws[w] = {k: qd[i] for i, k in enumerate(supp)}
    return regs, bws


def merge_circuit(cfg, d, s, bennett=True, nodes=None):
    Q_reg, Q = qudit_register("q", cfg.width[d-1], cfg.enc)
    x_reg, x = qudit_register("x", cfg.width[d], cfg.enc)
    W_reg, W = qudit_register("W", cfg.width[d], cfg.enc)
    regs, bws = workspace_registers(cfg, d, nodes=nodes)
    qc = QuantumCircuit(Q_reg, x_reg, W_reg, *regs, name=f"merge_d{d}_s{s}")
    B = Builder(qc, cfg.enc)
    merge_ops(cfg, B, d, Q, x, W, bws, s, bennett=bennett, nodes=nodes)
    return qc, B, dict(Q_reg=Q_reg, Q=Q, x_reg=x_reg, x=x, W_reg=W_reg, W=W, b_regs=regs, bws=bws)


def fourier_circuit(cfg, width, role):
    Q_reg, Q = qudit_register("q", width, cfg.enc)
    qc = QuantumCircuit(Q_reg, name=role)
    B = Builder(qc, cfg.enc)
    for q in Q:
        B.qft(q, role)
    return qc, B


# ====================================================================== assembled terminal sample

def sources_per_grade(cfg):
    """N_d = number of grade-d sources in one terminal sample = prod_(k=2..d) M_k."""
    return {d: prod(cfg.arity[k] for k in range(2, d+1)) for d in range(1, cfg.c+1)}


def terminal_sample_circuit(cfg, inst=None, witness=None):
    """The whole circuit for ONE terminal sample (one descent tree, depth first),
    for fixed classical records (witnesses are classical feed-forward).
    witness: None (all ones), a tuple used at every grade-2 merge when c = 2, a
    dict {d: tuple} or a callable (d, merge_index) -> tuple. No register reuse."""
    c, enc, N = cfg.c, cfg.enc, sources_per_grade(cfg)

    def wit(d, idx):
        if witness is None:
            return (1,)*cfg.arity[d]
        if callable(witness):
            return witness(d, idx)
        if isinstance(witness, dict):
            return witness[d]
        return witness

    regs, top_addr, top_labels, top_anc = [], [], [], []
    for i in range(N[c]):
        r, a = qudit_register(f"a{i}", cfg.width[c], enc)
        regs.append(r); top_addr.append(a)
    for i in range(N[c]):
        ys = [QuantumRegister(cfg.label_bits, f"y{i}{s}" if c == 2 else f"y{i}_{s}") for s in cfg.points]
        regs += ys; top_labels.append(ys)
    if c >= 2:
        for i in range(N[c]):
            r, z = qudit_register(f"z{i}" if c == 2 else f"z{c}_{i}", cfg.dims[c-1], enc)
            regs.append(r); top_anc.append(z)
    w_reg, w = qudit_register("w", cfg.m, enc)
    regs.append(w_reg)
    mid_q, mid_anc = {}, {}
    for d in range(c-1, 0, -1):
        mid_q[d], mid_anc[d] = [], []
        for i in range(N[d]):
            r, qd = qudit_register("q" if (d == 1 and c == 2) else f"q{d}_{i}", cfg.width[d], enc)
            regs.append(r); mid_q[d].append(qd)
            if d >= 2:
                r, z = qudit_register(f"z{d}_{i}", cfg.dims[d-1], enc)
                regs.append(r); mid_anc[d].append(z)
    work = {}
    for d in range(c, 1, -1):
        r, Wd = qudit_register("W" if c == 2 else f"W{d}", cfg.width[d], enc)
        bregs, bws = workspace_registers(cfg, d, prefix="b" if c == 2 else f"b{d}_")
        regs += [r]+bregs
        work[d] = (Wd, bws)
    n_lam = enc.nb*sum(cfg.dims[d-1]*N[d] for d in range(2, c+1))
    lam_bits, k_bits = ClassicalRegister(max(n_lam, 1), "lam"), ClassicalRegister(enc.nb*cfg.m, "k")
    qc = QuantumCircuit(*regs, lam_bits, k_bits)
    B = Builder(qc, enc)
    U = make_oracle(cfg, inst)
    counters = {"top": 0, "lam": 0, **{d: 0 for d in range(1, c)}, "merge": Counter()}

    def measure_anc(z):
        bits = [qb for q in z for qb in q]
        qc.measure(bits, lam_bits[counters["lam"]:counters["lam"]+len(bits)])
        counters["lam"] += len(bits)

    def emit(d):
        if d == c:
            i = counters["top"]
            counters["top"] += 1
            a = top_addr[i]
            source_ops(cfg, B, a, w, top_labels[i], U, cfg.points)
            if c >= 2:
                instrument_ops(cfg, B, c, a, top_anc[i])
                measure_anc(top_anc[i])
            return a
        children = [emit(d+1) for _ in range(cfg.arity[d+1])]
        i = counters[d]
        counters[d] += 1
        Qd = mid_q[d][i]
        for q in Qd:
            B.qft(q, f"qft_grade{d+1}")
        sv = wit(d+1, counters["merge"][d+1])
        counters["merge"][d+1] += 1
        Wd, bws = work[d+1]
        for child, s in zip(children, sv):
            if s % cfg.p:
                merge_ops(cfg, B, d+1, Qd, child, Wd, bws, s % cfg.p)
        if d >= 2:
            instrument_ops(cfg, B, d, Qd, mid_anc[d][i])
            measure_anc(mid_anc[d][i])
        return Qd

    root = emit(1) if c >= 2 else emit(c)
    for q in root:
        B.qft(q, "qft_final")
    qc.measure(_flat_reg(root), k_bits)
    return qc, B


# ====================================================================== bit-sliced exact evaluation

ALL_ONES = np.uint64(0xFFFFFFFFFFFFFFFF)


def compile_ops(instructions, pos):
    ops = []
    for inst in instructions:
        op = inst.operation
        wires = [pos[q] for q in inst.qubits]
        if op.name == "x":
            ops.append(("x", wires, 0, 0))
        elif op.name == "swap":
            ops.append(("swap", wires, 0, 0))
        elif isinstance(op, ControlledGate) and op.base_gate.name == "x":
            ops.append(("mcx", wires, int(op.ctrl_state), op.num_ctrl_qubits))
        elif isinstance(op, TableOracle):
            ops.append(("oracle", wires, op, 0))
        elif op.name in ("measure", "barrier"):
            continue
        else:
            raise ValueError(f"not a permutation gate: {op.name}")
    return ops


class BitSim:
    """Bit-sliced exact evaluation of X/CX/MCX/SWAP/table-oracle gate lists:
    column k of qubit i holds that qubit's bit on 64 inputs."""

    def __init__(self, num_qubits, n_inputs):
        self.N, self.nw = n_inputs, (n_inputs+63)//64
        self.cols = np.zeros((num_qubits, self.nw), dtype=np.uint64)
        self.targets = set()

    def _pack(self, bits):
        by = np.packbits(bits.astype(np.uint8), bitorder="little")
        out = np.zeros(self.nw*8, dtype=np.uint8)
        out[:len(by)] = by
        return out.view(np.uint64)

    def _unpack(self, i):
        return np.unpackbits(self.cols[i].view(np.uint8), bitorder="little")[:self.N].astype(np.int64)

    def load(self, wires_by_qudit, values):
        """values[:, j] = canonical value of qudit j; wires_by_qudit[j] = its qubit positions."""
        for j, wires in enumerate(wires_by_qudit):
            for i, wpos in enumerate(wires):
                self.cols[wpos] = self._pack((values[:, j] >> i) & 1)

    def read(self, wires_by_qudit):
        out = np.zeros((self.N, len(wires_by_qudit)), dtype=np.int64)
        for j, wires in enumerate(wires_by_qudit):
            for i, wpos in enumerate(wires):
                out[:, j] |= self._unpack(wpos) << i
        return out

    def read_bits(self, wires):
        return sum(self._unpack(wpos) << i for i, wpos in enumerate(wires))

    def run(self, ops, expand_oracle=False):
        cols = self.cols
        for kind, w, st, nc in ops:
            if kind == "mcx":
                c0 = cols[w[0]]
                fire = c0.copy() if st & 1 else ~c0
                for i in range(1, nc):
                    ci = cols[w[i]]
                    if st >> i & 1:
                        np.bitwise_and(fire, ci, out=fire)
                    else:
                        np.bitwise_and(fire, ~ci, out=fire)
                np.bitwise_xor(cols[w[-1]], fire, out=cols[w[-1]])
                self.targets.add(w[-1])
            elif kind == "x":
                np.bitwise_xor(cols[w[0]], ALL_ONES, out=cols[w[0]])
                self.targets.add(w[0])
            elif kind == "swap":
                cols[[w[0], w[1]]] = cols[[w[1], w[0]]]
                self.targets.update(w)
            elif kind == "oracle":
                if expand_oracle:
                    inner = st.definition
                    sub = {q: w[i] for i, q in enumerate(inner.qubits)}
                    self.run(compile_ops(inner.data, sub))
                    continue
                self._apply_table(st, w)

    def _apply_table(self, U, w):
        enc, m, nb = U.enc, U.m_coords, U.enc.nb
        word = sum(self._unpack(w[k]) << k for k in range(nb*m))
        digits = [(word >> (nb*(m-1-j))) & ((1 << nb)-1) for j in range(m)]
        ok = np.ones(self.N, dtype=bool)
        idx = np.zeros(self.N, dtype=np.int64)
        for dgt in digits:
            ok &= dgt < enc.p
            idx = idx*enc.p+np.where(dgt < enc.p, dgt, 0)
        val = np.where(ok, U.table[idx], 0)
        for bit in range(U.label_bits):
            wpos = w[nb*m+bit]
            np.bitwise_xor(self.cols[wpos], self._pack((val >> bit) & 1), out=self.cols[wpos])
            self.targets.add(wpos)


def wires_of(qudits, pos):
    return [[pos[qb] for qb in q] for q in qudits]


# ====================================================================== macro-level proof of the arithmetic

class Poly:
    """Polynomial over F_p; monomials are sorted tuples of variable indices."""
    __slots__ = ("p", "t")

    def __init__(self, p, terms=None):
        self.p = p
        self.t = {m: c % p for m, c in (terms or {}).items() if c % p}

    @classmethod
    def var(cls, p, i):
        return cls(p, {(i,): 1})

    def __add__(self, o):
        t = dict(self.t)
        for m, c in o.t.items():
            t[m] = t.get(m, 0)+c
        return Poly(self.p, t)

    def __neg__(self):
        return Poly(self.p, {m: -c for m, c in self.t.items()})

    def __sub__(self, o):
        return self+(-o)

    def __mul__(self, o):
        if isinstance(o, int):
            return Poly(self.p, {m: c*o for m, c in self.t.items()})
        t = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                m = tuple(sorted(m1+m2))
                t[m] = t.get(m, 0)+c1*c2
        return Poly(self.p, t)

    __rmul__ = __mul__

    def __eq__(self, o):
        return self.t == o.t

    def is_zero(self):
        return not self.t


def sym_bracket(T, U, V, p):
    n = T.shape[0]
    out = [Poly(p) for _ in range(n)]
    for i, j, k in zip(*np.nonzero(T % p)):
        out[k] = out[k]+(U[i]*V[j])*int(T[i, j, k])
    return out


def sym_bch_reference(T, d, X, Y, p):
    """Classical BCH polynomial (the rees_end_to_end_sim.NilGroup formula) for
    class <= 4, written independently of bch_nodes; for d > 4 the checked
    right-nested form is used."""
    inv = lambda k: pow(k, -1, p)
    out = [X[k]+Y[k] for k in range(len(X))]
    if d > 4:
        val = {}
        for w, a in bch_nodes(d):
            left = X if w[0] == "x" else Y
            val[w] = sym_bracket(T, left, Y if w == "xy" else val[w[1:]], p)
            a = _mod_fraction(a, p)
            out = [o+val[w][k]*a for k, o in enumerate(out)]
        return out
    if d >= 2:
        xy = sym_bracket(T, X, Y, p)
        out = [o+v*inv(2) for o, v in zip(out, xy)]
        if d >= 3:
            xxy, yxy = sym_bracket(T, X, xy, p), sym_bracket(T, Y, xy, p)
            out = [o+(a-b)*inv(12) for o, a, b in zip(out, xxy, yxy)]
            if d >= 4:
                yxxy = sym_bracket(T, Y, xxy, p)
                out = [o-v*inv(24) for o, v in zip(out, yxxy)]
    return out


_MACRO_CACHE = {}


def check_macros(qc, B):
    """Every gate belongs to exactly one macro, and each macro's gate slice is,
    exhaustively on the canonical values of its qudits, the declared map, touching
    no other qubit. Returns the number of macro instances checked."""
    p, nb = B.p, B.enc.nb
    covered = 0
    data = qc.data
    for kind, qudits, coeff, start, end in B.macros:
        if start != covered:
            raise AssertionError(f"gate {covered} is outside every macro")
        covered = end
        if kind in ("qft", "qft_dg"):
            if end-start != 1 or data[start].operation.name != f"qft{p}"+("_dg" if kind == "qft_dg" else ""):
                raise AssertionError("bad qft macro")
            continue
        if kind == "oracle":
            if end-start > 1 or (end-start == 1 and data[start].operation.name != "U_f"):
                raise AssertionError("bad oracle macro")
            continue
        if kind == "swap":
            half = len(qudits)//2
            want = [(a, b) for qa, qb in zip(qudits[:half], qudits[half:]) for a, b in zip(qa, qb)]
            got = [tuple(inst.qubits) for inst in data[start:end]]
            if got != want or any(inst.operation.name != "swap" for inst in data[start:end]):
                raise AssertionError("bad swap macro")
            continue
        local = {qb: (r, i) for r, q in enumerate(qudits) for i, qb in enumerate(q)}
        sig = (kind, coeff, tuple((inst.operation.name, getattr(inst.operation, "ctrl_state", None),
                                    tuple(local[q] for q in inst.qubits)) for inst in data[start:end]))
        if sig in _MACRO_CACHE:
            continue
        pos = {qb: r*nb+i for qb, (r, i) in local.items()}
        ops = compile_ops(data[start:end], pos)
        vals = np.array(list(product(range(p), repeat=len(qudits))), dtype=np.int64)
        sim = BitSim(nb*len(qudits), len(vals))
        wires = [[r*nb+i for i in range(nb)] for r in range(len(qudits))]
        sim.load(wires, vals)
        sim.run(ops)
        out = sim.read(wires)
        want = vals.copy()
        if kind == "add_scaled":
            want[:, 0] = (vals[:, 0]+coeff*vals[:, 1]) % p
        elif kind == "add_product":
            want[:, 0] = (vals[:, 0]+coeff*vals[:, 1]*vals[:, 2]) % p
        else:
            raise AssertionError(kind)
        if (out != want).any():
            raise ArithmeticError(f"macro {kind} gate slice is not its declared map")
        _MACRO_CACHE[sig] = True
    if covered != len(data):
        raise AssertionError("trailing gates outside every macro")
    return len(B.macros)


def symbolic_replay(B, init):
    """Run the macro program on polynomial registers {qudit: Poly}."""
    P = dict(init)
    zero = Poly(B.p)
    for kind, qudits, coeff, _, _ in B.macros:
        if kind == "add_scaled":
            t, a = qudits
            P[t] = P.get(t, zero)+P.get(a, zero)*coeff
        elif kind == "add_product":
            t, a, b = qudits
            P[t] = P.get(t, zero)+(P.get(a, zero)*P.get(b, zero))*coeff
        elif kind == "swap":
            half = len(qudits)//2
            for qa, qb in zip(qudits[:half], qudits[half:]):
                P[qa], P[qb] = P.get(qb, zero), P.get(qa, zero)
        else:
            raise ValueError(f"no symbolic semantics for {kind}")
    return P


def prove_merge(cfg, d, s, bennett=True, nodes=None):
    """Proof, on ALL canonical inputs, that the merge gate list maps
    |q, x, 0, 0> to |q, x * (-delta_s(sigma(q))), 0, 0> (classical BCH of G_d)."""
    qc, B, R = merge_circuit(cfg, d, s, bennett=bennett, nodes=nodes)
    n_macros = check_macros(qc, B)
    p, nq, nx = cfg.p, cfg.width[d-1], cfg.width[d]
    qv = [Poly.var(p, j) for j in range(nq)]
    xv = [Poly.var(p, nq+j) for j in range(nx)]
    init = {R["Q"][j]: qv[j] for j in range(nq)}
    init.update({R["x"][j]: xv[j] for j in range(nx)})
    P = symbolic_replay(B, init)
    zero = Poly(p)
    g = [qv[j]*(-pow(s, cfg.grades[j], p)) for j in range(nq)]+[zero]*(nx-nq)
    ref = sym_bch_reference(cfg.laws[d].tensor, d, xv, g, p)
    targeted = {q for inst in qc.data for q in inst.qubits[-1:]} | \
        {q for inst in qc.data if inst.operation.name == "swap" for q in inst.qubits}
    flags = {
        "macros_checked": n_macros,
        "x_equals_bch_right_translation": all(P.get(R["x"][j], zero) == ref[j] for j in range(nx)),
        "W_clean": all(P.get(q, zero).is_zero() for q in R["W"]),
        "brackets_clean": all(P.get(q, zero).is_zero() for bw in R["bws"].values() for q in bw.values()),
        "q_unchanged": all(P.get(R["Q"][j], zero) == qv[j] for j in range(nq)),
        "q_never_targeted": not any(qb in targeted for q in R["Q"] for qb in q),
    }
    flags["proved"] = all(v for k, v in flags.items() if k != "macros_checked")
    return flags


def merge_bitlevel(cfg, d, s, q_indices=None, x_indices=None, bennett=True):
    """Direct bit-sliced evaluation of the whole merge gate list on the inputs
    (q, x) for q in q_indices (default all) and x in x_indices (default all),
    zero scratch. Returns (perm[q_row, x_row] as G_d index, flags)."""
    qc, B, R = merge_circuit(cfg, d, s, bennett=bennett)
    pos = {q: i for i, q in enumerate(qc.qubits)}
    Gq, Gx = cfg.laws[d-1] if d > 1 else None, cfg.laws[d]
    nQ, nX = cfg.p**cfg.width[d-1], Gx.order
    qi = np.arange(nQ) if q_indices is None else np.asarray(q_indices)
    xi = np.arange(nX) if x_indices is None else np.asarray(x_indices)
    QQ, XX = np.meshgrid(qi, xi, indexing="ij")
    qv = Gq.decode(QQ.ravel())
    xv = Gx.decode(XX.ravel())
    sim = BitSim(qc.num_qubits, len(qv))
    sim.load(wires_of(R["Q"], pos), qv)
    sim.load(wires_of(R["x"], pos), xv)
    sim.run(compile_ops(qc.data, pos))
    x_out = sim.read(wires_of(R["x"], pos))
    scratch = [R["W"]]+[list(bw.values()) for bw in R["bws"].values()]
    flags = {"q_unchanged": bool((sim.read(wires_of(R["Q"], pos)) == qv).all()),
             "scratch_clean": all((sim.read(wires_of(qs, pos)) == 0).all() for qs in scratch),
             "x_canonical": bool((x_out < cfg.p).all()),
             "q_never_targeted": not any(pos[qb] in sim.targets for q in R["Q"] for qb in q),
             "inputs": int(len(qv))}
    g = -qv*np.array(cfg.scales(d-1, s))[None, :]
    g = np.concatenate([g, np.zeros((len(g), cfg.width[d]-cfg.width[d-1]), dtype=np.int64)], axis=1) % cfg.p
    ref = Gx.mul(xv, g)
    flags["equals_bch"] = bool((x_out == ref).all())
    perm = Gx.encode(np.where(x_out < cfg.p, x_out, 0)).reshape(len(qi), len(xi))
    return perm, flags


# ====================================================================== instrument semantics

@lru_cache(maxsize=None)
def _qft_ok(p):
    nb = max(1, (p-1).bit_length())
    for inv in (False, True):
        sub = QuantumCircuit(nb)
        sub.append(qft_gate(p, inv), list(range(nb)))
        if np.abs(Operator(sub).data-qft_matrix(p, inv)).max() > 1e-12:
            return False
    return True


# Exponent derivation for the instrument. "exact" (default): the instrument gate
# list is evaluated in Z[zeta_p] with integer coefficients (no floating point
# enters the exponents). "float": the original path (qiskit Operator in complex
# floating point, phase angle * p/(2 pi), rounded). Override per call with
# instrument_semantics(cfg, d, exact=...), or set this flag / the CLI option.
INSTRUMENT_EXPONENTS = "exact"


def _instrument_blocks(cfg, d):
    """The instrument circuit and its gate list split into one block per top
    coordinate (top qudit a[t] + ancilla z[j]); a gate outside one block raises."""
    qc, B, (a_reg, a, z_reg, z) = instrument_circuit(cfg, d)
    top = cfg.top(d)
    blocks = [set(a[t]) | set(z[j]) for j, t in enumerate(top)]
    sub_insts = [[] for _ in top]
    for inst in qc.data:
        qs = set(inst.qubits)
        hit = [j for j, blk in enumerate(blocks) if qs <= blk]
        if len(hit) != 1:
            raise AssertionError("instrument gate straddles coordinate blocks or touches lower grades")
        sub_insts[hit[0]].append(inst)
    orders = [list(a[t])+list(z[j]) for j, t in enumerate(top)]
    return qc, top, sub_insts, orders


def instrument_semantics(cfg, d, exact=None):
    """From the instrument gate list: per top coordinate j the exact conditioning
    kernel exponents e_j[lam][u] (Python/NumPy integers mod p) with
    kappa_lam(u) = zeta^e / p, where kappa(u) = sum_z k(z) conj k(z+u) and
    K_lam = sum_z k_lam(z) R_z. Checks: block partition, no leakage to padding,
    completeness, circulant form. exact=None reads INSTRUMENT_EXPONENTS."""
    if exact is None:
        exact = INSTRUMENT_EXPONENTS == "exact"
    return _instrument_semantics_exact(cfg, d) if exact else _instrument_semantics_float(cfg, d)


def _instrument_semantics_float(cfg, d):
    """The original derivation: complex floating point, then rounding (|err| < 1e-9)."""
    qc, top, sub_insts, orders = _instrument_blocks(cfg, d)
    p, nb = cfg.p, cfg.enc.nb
    omega = np.exp(2j*np.pi/p)
    expo, info = [], {"mode": "float", "leak": 0.0, "completeness_err": 0.0, "circulant_err": 0.0,
                      "round_err": 0.0}
    for j, t in enumerate(top):
        order = orders[j]
        loc = {q: i for i, q in enumerate(order)}
        sub = QuantumCircuit(2*nb)
        for inst in sub_insts[j]:
            sub.append(inst.operation, [loc[q] for q in inst.qubits])
        U = Operator(sub).data
        K = np.array([[[U[tp+(lam << nb), tt] for tt in range(p)] for tp in range(p)] for lam in range(p)])
        kept = np.sum(np.abs(K)**2, axis=(0, 1))                    # per input t
        info["leak"] = max(info["leak"], float(np.abs(1-kept).max()))
        comp = sum(K[l].conj().T @ K[l] for l in range(p))
        info["completeness_err"] = max(info["completeness_err"], float(np.abs(comp-np.eye(p)).max()))
        e = np.zeros((p, p), dtype=np.int64)
        for lam in range(p):
            k = np.array([K[lam][(-zz) % p, 0] for zz in range(p)])
            circ = max(abs(K[lam][(tt-zz) % p, tt]-k[zz]) for tt in range(p) for zz in range(p))
            info["circulant_err"] = max(info["circulant_err"], float(circ))
            for u in range(p):
                kap = p*sum(k[zz]*np.conj(k[(zz+u) % p]) for zz in range(p))
                ex = int(round(np.angle(kap)*p/(2*np.pi))) % p
                info["round_err"] = max(info["round_err"], float(abs(kap-omega**ex)))
                e[lam, u] = ex
        expo.append(e)
    info["ok"] = all(info[k] < TOL for k in ("leak", "completeness_err", "circulant_err", "round_err")) \
        and _qft_ok(p)
    if not info["ok"]:
        raise ArithmeticError(f"instrument gate list is not the complete central instrument: {info}")
    return expo, info


def _cyc_conj(v, p):
    """Complex conjugation on Z[zeta_p] coefficient vectors: zeta^j -> zeta^(-j)."""
    return v[..., (-np.arange(p)) % p]


def _exact_permutation(inst, loc, nq):
    """Basis-state permutation dest[i] of one permutation gate on nq local qubits,
    in integer arithmetic. X/CX/MCX/SWAP use the generator's own BitSim semantics;
    a UnitaryGate (the reduced macros of rees_circuit_arith) must have every entry
    exactly 0.0 or 1.0 and be a permutation matrix (an exact read, no rounding)."""
    D = 1 << nq
    idx = np.arange(D, dtype=np.int64)
    try:
        ops = compile_ops([inst], loc)
    except ValueError:
        ops = None
    if ops is not None:
        if any(kind == "oracle" for kind, *_ in ops):
            raise AssertionError("oracle inside the instrument")
        sim = BitSim(nq, D)
        sim.load([[i] for i in range(nq)], (idx[:, None] >> np.arange(nq)[None, :]) & 1)
        sim.run(ops)
        return (sim.read([[i] for i in range(nq)]) << np.arange(nq)[None, :]).sum(axis=1)
    M = np.asarray(inst.operation.to_matrix())
    if not (np.all((M == 0) | (M == 1)) and (M.sum(axis=0) == 1).all() and (M.sum(axis=1) == 1).all()):
        raise ValueError(f"not an exact permutation gate: {inst.operation.name}")
    perm = np.argmax(M == 1, axis=0)                                  # local dest of local src
    wires = [loc[q] for q in inst.qubits]
    local = sum(((idx >> w) & 1) << i for i, w in enumerate(wires))
    clear = idx & ~sum(1 << w for w in wires)
    dl = perm[local]
    return clear | sum(((dl >> i) & 1) << w for i, w in enumerate(wires))


def _instrument_block_exact(insts, loc, p, nb):
    """Exact evaluation of one (2b)-qubit instrument block on the inputs a = tt (tt < p), z = 0.
    Returns (A, k): A[i, tt] is the canonical Z[zeta_p] coefficient vector (int64) of basis
    state i (little-endian over loc: a = low b bits, z = high b bits), and the block is
    p^(-k/2) * A, k = number of QFT_p gates. QFT_p gates are the generator's qft_gate
    (exact unitary F_p + identity on padding): they are applied as zeta^(+-vw)/sqrt(p) on
    canonical values, and any amplitude on padding at a QFT raises. All others must be
    exact permutation gates."""
    nq, mask = 2*nb, (1 << nb)-1
    D = 1 << nq
    idx = np.arange(D, dtype=np.int64)
    A = np.zeros((D, p, p), dtype=np.int64)
    A[np.arange(p), np.arange(p), 0] = 1                             # |a = tt, z = 0>
    k = 0
    for inst in insts:
        name = inst.operation.name
        wires = [loc[q] for q in inst.qubits]
        if name in (f"qft{p}", f"qft{p}_dg"):
            if wires not in (list(range(nb)), list(range(nb, nq))):
                raise AssertionError("QFT_p not on one qudit of the block")
            off, sign = wires[0], (-1 if name.endswith("_dg") else 1)
            v, rest = (idx >> off) & mask, idx & ~(mask << off)
            if A[v >= p].any():
                raise ArithmeticError("QFT_p applied to a state with amplitude on padding")
            new = np.zeros_like(A)
            for i in np.nonzero((v < p) & A.reshape(D, -1).any(axis=1))[0]:
                for w in range(p):
                    new[rest[i] | (w << off)] += np.roll(A[i], (sign*int(v[i])*w) % p, axis=-1)
            A, k = new, k+1
        else:
            dest = _exact_permutation(inst, loc, nq)
            if len(np.unique(dest)) != D:
                raise ArithmeticError("gate is not a bijection of basis states")
            new = np.zeros_like(A)
            new[dest] = A
            A = new
    return cyc_canon(A), k


def _instrument_semantics_exact(cfg, d):
    """The exact derivation: every quantity is an integer coefficient vector in
    Z[zeta_p] (int64) times a power of p; each exponent is the position of the unique
    monomial p^(k-1) zeta^e equal to sum_z m(z) conj m(z+u). The info fields leak,
    completeness_err, circulant_err, round_err are mismatch COUNTS (0 = exact equality)."""
    qc, top, sub_insts, orders = _instrument_blocks(cfg, d)
    p, nb = cfg.p, cfg.enc.nb
    expo = []
    info = {"mode": "exact", "leak": 0, "completeness_err": 0, "circulant_err": 0, "round_err": 0,
            "qft_factors": [], "counts_are_exact_mismatches": True}
    for j, t in enumerate(top):
        loc = {q: i for i, q in enumerate(orders[j])}
        A, k = _instrument_block_exact(sub_insts[j], loc, p, nb)
        info["qft_factors"].append(k)
        idx = np.arange(1 << (2*nb))
        canon = ((idx & ((1 << nb)-1)) < p) & ((idx >> nb) < p)
        info["leak"] += int(A[~canon].any(axis=-1).sum())            # nonzero padding amplitudes
        # M[lam, tp, tt] with K_lam = p^(-k/2) M_lam
        M = np.stack([np.stack([A[tp+(lam << nb)] for tp in range(p)]) for lam in range(p)])
        prodM = cyc_mul(_cyc_conj(M, p)[:, :, :, None, :], M[:, :, None, :, :], p)   # [lam, tp, tt', tt]
        comp = cyc_canon(prodM.sum(axis=(0, 1)))
        target = np.zeros((p, p, p), dtype=np.int64)
        target[np.arange(p), np.arange(p), 0] = p**k                 # sum K^dag K = 1
        info["completeness_err"] += int((comp != cyc_canon(target)).any(axis=-1).sum())
        if k < 1:
            raise ArithmeticError("instrument block has no QFT_p")
        monos = cyc_canon(np.eye(p, dtype=np.int64)*p**(k-1))        # row e: p^(k-1) zeta^e
        e = np.zeros((p, p), dtype=np.int64)
        for lam in range(p):
            m = np.stack([M[lam, (-zz) % p, 0] for zz in range(p)])
            info["circulant_err"] += sum(int((M[lam, (tt-zz) % p, tt] != m[zz]).any())
                                         for tt in range(p) for zz in range(p))
            for u in range(p):
                S = cyc_canon(cyc_mul(m, _cyc_conj(m[(np.arange(p)+u) % p], p), p).sum(axis=0))
                hits = [ex for ex in range(p) if (S == monos[ex]).all()]
                if len(hits) != 1:
                    info["round_err"] += 1
                    continue
                e[lam, u] = hits[0]
        expo.append(e)
    info["qft_matrix_float_consistency"] = _qft_ok(p)   # stored matrix of qft_gate vs F_p (1e-12); not used above
    info["ok"] = all(info[k] == 0 for k in ("leak", "completeness_err", "circulant_err", "round_err")) \
        and info["qft_matrix_float_consistency"]
    if not info["ok"]:
        raise ArithmeticError(f"instrument gate list is not the complete central instrument: {info}")
    return expo, info


def instrument_exponent_agreement(cfg):
    """Both derivations on every grade: gate counts and per-entry exponent comparison."""
    out = {"config": cfg.name(), "grades": {}, "mismatches": 0, "entries": 0}
    for d in range(2, cfg.c+1):
        qc, top, sub_insts, _ = _instrument_blocks(cfg, d)
        ex, ie = _instrument_semantics_exact(cfg, d)
        fl, if_ = _instrument_semantics_float(cfg, d)
        mism = sum(int((a != b).sum()) for a, b in zip(ex, fl))
        n = sum(int(a.size) for a in ex)
        out["grades"][d] = {"gates": len(qc.data), "gates_per_block": [len(s) for s in sub_insts],
                            "blocks": len(top), "entries": n, "mismatches": mism,
                            "exact_info": ie, "float_info": if_}
        out["mismatches"] += mism
        out["entries"] += n
    return out


# ====================================================================== exact states

@dataclass
class XState:
    """rho[x, y] = phi(x^-1 y)/|G_d|, phi(g) = scale * sum_j v[g, j] zeta^j (canonical)."""
    d: int
    scale: Fraction
    v: np.ndarray

    def normalized(self):
        g = int(np.gcd.reduce(np.abs(self.v).ravel())) if self.v.any() else 1
        return XState(self.d, self.scale*g, self.v//g) if g > 1 else self

    def value_at_identity(self):
        q = cyc_rational(self.v[0])
        if q is None:
            raise ArithmeticError("trace is not rational")
        return self.scale*q

    def equals_indicator(self, indices):
        if self.v[:, 1:].any():
            return False
        target = np.zeros(len(self.v), dtype=np.int64)
        target[indices] = 1
        return bool((self.v[:, 0]*self.scale.numerator == target*self.scale.denominator).all())

    def dense(self, law):
        zeta = np.exp(2j*np.pi*np.arange(self.v.shape[1])/self.v.shape[1])
        phi = (self.v @ zeta)*float(self.scale)
        E = law.elements()
        inv = law.encode((-E) % law.p)
        diff = np.stack([law.encode(law.mul(E[inv[u]][None, :], E)) for u in range(law.order)])
        return phi[diff]/law.order


class Engine:
    """Exact composition of the simulated modules for one Config."""

    def __init__(self, cfg):
        self.cfg, self.p = cfg, cfg.p
        self.kernels = {d: instrument_semantics(cfg, d) for d in range(2, cfg.c+1)}
        self._dil, self._shift = {}, {}

    def dil(self, d, s):
        key = (d, s)
        if key not in self._dil:
            law = self.cfg.laws[d]
            self._dil[key] = law.encode(law.elements()*np.array(self.cfg.scales(d, s))[None, :])
        return self._dil[key]

    def shifts(self, d):
        if d not in self._shift:
            g, p = self.cfg.dims[d-1], self.p
            Z = np.array(list(product(range(p), repeat=g)), dtype=np.int64).reshape(-1, g)
            w = p**np.arange(g-1, -1, -1)
            self._shift[d] = (Z, [((Z+u) % p) @ w for u in Z])
        return self._shift[d]

    # -- source from the source gate list
    def source(self, inst, points=None, uncompute=True, expand_oracle=False):
        cfg = self.cfg
        qc, B, (a_reg, a, w_reg, w, labels) = source_circuit(cfg, inst, points, uncompute)
        head = qc.data[:len(a)]
        if [i.operation.name for i in head] != [f"qft{cfg.p}"]*len(a) or \
                [tuple(i.qubits) for i in head] != list(a) or not _qft_ok(cfg.p):
            raise AssertionError("source must start with exact QFT_p on each address coordinate")
        pos = {q: i for i, q in enumerate(qc.qubits)}
        law = cfg.laws[cfg.c]
        X = law.elements()
        sim = BitSim(qc.num_qubits, law.order)
        sim.load(wires_of(a, pos), X)
        sim.run(compile_ops(qc.data[len(a):], pos), expand_oracle=expand_oracle)
        addr_ok = bool((sim.read(wires_of(a, pos)) == X).all())
        work_clean = bool((sim.read(wires_of(w, pos)) == 0).all())
        ys = np.stack([sim.read_bits([pos[q] for q in y]) for y in labels], axis=1)
        rest = np.concatenate([ys, sim.read(wires_of(w, pos))], axis=1)
        _, fibre = np.unique(rest, axis=0, return_inverse=True)
        fibre = fibre.ravel()
        S = np.nonzero(fibre == fibre[0])[0]
        sizes = np.bincount(fibre)
        info = {"address_unchanged": addr_ok, "workspace_clean": work_clean,
                "fibres": int(len(sizes)), "lifted_order": int(len(S)),
                "equal_fibres": bool((sizes == len(S)).all())}
        Sset = set(S.tolist())
        gens, gen_set = [], {0}
        for x in S:
            if int(x) not in gen_set:
                gens.append(int(x))
                gen_set = set(law.closure(law.decode(np.array(gens))).tolist())
        info["identity_fibre_is_subgroup"] = gen_set == Sset
        info["fibres_are_left_cosets"] = info["equal_fibres"] and all(
            (fibre[law.encode(law.mul(X, law.decode(g)[None, :]))] == fibre).all() for g in gens)
        info["coset_state"] = info["identity_fibre_is_subgroup"] and info["fibres_are_left_cosets"] and addr_ok
        v = np.zeros((law.order, self.p), dtype=np.int64)
        if info["coset_state"]:
            v[S, 0] = 1                         # rho[x, y] = [x^-1 y in S]/|G| exactly
        return XState(cfg.c, Fraction(1), v), S, info

    # -- complete central instrument
    def condition_unnormalized(self, st, lam):
        d, p = st.d, self.p
        expo, _ = self.kernels[d]
        Z, sh = self.shifts(d)
        g = self.cfg.dims[d-1]
        v = st.v.reshape(-1, p**g, p)
        out = np.zeros_like(v)
        for u, idx in zip(Z, sh):
            e = sum(int(expo[j][lam[j], u[j]]) for j in range(g)) % p
            out += np.roll(v[:, idx, :], e, axis=-1)
        out = cyc_canon(out.reshape(-1, p))
        return XState(d, st.scale/p**g, out)

    def label_law(self, st):
        g = self.cfg.dims[st.d-1]
        probs, states = {}, {}
        for lam in product(range(self.p), repeat=g):
            un = self.condition_unnormalized(st, lam)
            pr = un.value_at_identity()
            if pr < 0:
                raise ArithmeticError("negative branch probability")
            probs[lam] = pr
            if pr:
                states[lam] = XState(st.d, un.scale/pr, un.v).normalized()
        if sum(probs.values()) != 1:
            raise ArithmeticError("instrument probabilities do not sum to one")
        return probs, states

    # -- controlled right-action channel (verified gate semantics) and descent
    def merge(self, states, witness, factors=None):
        """Output on Q: sigma[q, r] = |Q|^-1 prod_i phi_i(g_q g_r^-1) with the merge
        permutation pi_q(x) = x g_q proved above; = psi(q^-1 r)/|Q| with
        psi = F o sigma, F(y) = prod_i phi_i(delta_si(y)), checked central-fibre constant."""
        d, p = states[0].d, self.p
        active = [(st, s) for st, s in zip(states, witness) if s % p]
        if not active:
            raise ValueError("zero witness")
        F, scale = None, Fraction(1)
        for k, (st, s) in enumerate(active):
            fac = factors[k] if factors is not None else st.v[self.dil(d, s % p)]
            scale *= st.scale
            F = fac if F is None else cyc_mul(F, fac, p)
            g = int(np.gcd.reduce(np.abs(F).ravel())) if F.any() else 1
            if g > 1:
                F, scale = F//g, scale*g
        Zs = p**self.cfg.dims[d-1]
        fib = F.reshape(-1, Zs, p)
        if (fib != fib[:, :1, :]).any():
            raise ArithmeticError("merge output does not descend (not constant on central fibres)")
        out = XState(d-1, scale, fib[:, 0, :].copy()).normalized()
        if out.value_at_identity() != 1:
            raise ArithmeticError("merge output lost normalization")
        return out

    # -- terminal Fourier sampling
    def readout(self, st):
        if st.d != 1:
            raise ValueError("readout on grade one only")
        p, law = self.p, self.cfg.laws[1]
        W = law.elements()
        E = (-(W @ W.T)) % p                        # P(k) = |G_1|^-1 sum_w zeta^(-k.w) psi(w)
        acc = np.zeros((law.order, p), dtype=np.int64)
        for r in range(p):
            acc += np.roll((E == r).astype(np.int64) @ st.v, r, axis=-1)
        acc = cyc_canon(acc)
        if acc[:, 1:].any():
            raise ArithmeticError("Fourier probability is not rational")
        probs = {tuple(int(x) for x in k): st.scale*int(a)/law.order for k, a in zip(W, acc[:, 0]) if a}
        if sum(probs.values()) != 1 or min(probs.values()) < 0:
            raise ArithmeticError("Fourier distribution invalid")
        return probs


# ====================================================================== truth for grading

def stage_indices(cfg, log_h, d):
    """Indices in G_d of H_d = exp(sum_(k<=d) t^k (h cap gamma_k)); exp(h~) at d = c."""
    grade_bases = graded_hidden(cfg.cover, log_h)[:d]
    rows, offset, n = [], 0, cfg.width[d]
    for k, basis in enumerate(grade_bases):
        for v in basis:
            row = [0]*n
            row[offset:offset+len(v)] = v
            rows.append(row)
        offset += cfg.dims[k]
    return np.sort(cfg.laws[d].encode(span_elements(rows, n, cfg.p)))


def allowed_labels(cfg, log_h, d):
    K_perp = expected_label_support(cfg.cover, log_h, d)
    return sorted(tuple(int(x) for x in r) for r in span_elements(K_perp, cfg.dims[d-1], cfg.p))


@lru_cache(maxsize=None)
def _nonzero_vectors(p, M):
    return np.array(list(product(range(p), repeat=M))[1:], dtype=np.int64)


def all_witnesses(labels, d, p):
    S = _nonzero_vectors(p, len(labels))
    sums = (pow_mod(S, d, p) @ np.array(labels, dtype=np.int64)) % p
    return S[~sums.any(axis=1)]


def solve_sde(labels, d, p, rng, prefer="auto"):
    """Classical SDE step. 'auto': the deterministic IS solver when the arity reaches
    its column count for the actual rank, else brute force over F_p^M."""
    cols = [tuple(int(x) for x in l) for l in labels]
    rank = len(rref(cols, p))
    if prefer in ("auto", "is") and len(cols) >= columns_required(p, d, rank):
        return tuple(int(x) for x in is_sde_solve(p, d, cols).s), "is"
    if prefer == "is":
        raise ValueError("IS solver does not apply at this arity")
    if p**len(cols) > 5*10**6:
        raise ValueError("brute force too large; raise the arity to the IS column count")
    s, _ = brute_force_sde(cols, d, p, rng)
    return s, "brute_force"


# ====================================================================== checks and runs

def check_instance(cfg, inst, engine=None, *, max_cases=4000, sample_tuples=6, max_witnesses=None, seed=0):
    """Exact check of one hidden subgroup through every grade.

    Grade d: the source / merged state must be rho_(H_d), its label law uniform on
    K_d^perp; for label tuples (all of them when |allowed|^M_d <= max_cases, else
    `sample_tuples` structured + random ones) EVERY valid witness is merged (or,
    in sampled mode with max_witnesses set, that many random valid witnesses per
    tuple) and the output must be rho_(H_(d-1)). "All" mode is used when the
    expected case count |allowed|^M p^M / |allowed| is at most max_cases. The
    readout must be uniform on h^perp."""
    eng = engine or Engine(cfg)
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    t0 = time.time()
    st, S, sinfo = eng.source(inst)
    row = {"instance": inst.name, "normal": inst.normal, "dim_h": len(inst.log_h), "source": sinfo,
           "source_equals_rho_lift": bool(sinfo["coset_state"] and
                                          np.array_equal(np.sort(S), stage_indices(cfg, inst.log_h, c))),
           "source_workspace_clean": sinfo["workspace_clean"], "grades": {}}
    ok = row["source_equals_rho_lift"] and row["source_workspace_clean"]
    for d in range(c, 1, -1):
        probs, states = eng.label_law(st)
        allowed = allowed_labels(cfg, inst.log_h, d)
        law_ok = all(pr == (Fraction(1, len(allowed)) if lam in allowed else 0) for lam, pr in probs.items())
        M = cfg.arity[d]
        total = len(allowed)**M
        expected_cases = total*p**M//len(allowed)     # about p^M / |allowed| witnesses per tuple
        if expected_cases <= max_cases:
            tuples, mode = list(product(allowed, repeat=M)), "all"
        else:
            zero = tuple([0]*cfg.dims[d-1])
            tuples = [tuple([zero]*M), tuple([allowed[-1]]*M)]
            tuples += [tuple(rng.choice(allowed) for _ in range(M)) for _ in range(max(0, sample_tuples-2))]
            mode = f"sampled {len(tuples)} of {total}"
        target = stage_indices(cfg, inst.log_h, d-1)
        cases = good = 0
        fac_cache = {}
        capped = 0
        for labels in tuples:
            wits = all_witnesses(labels, d, p)
            if mode != "all" and max_witnesses is not None and len(wits) > max_witnesses:
                wits = wits[sorted(rng.sample(range(len(wits)), max_witnesses))]
                capped += 1
            for s in wits:
                facs = []
                for lam, si in zip(labels, s):
                    if si:
                        key = (lam, int(si))
                        if key not in fac_cache:
                            fac_cache[key] = states[lam].v[eng.dil(d, int(si))]
                        facs.append(fac_cache[key])
                act = [states[lam] for lam, si in zip(labels, s) if si]
                out = eng.merge(act, [int(x) for x in s if x], factors=facs)
                cases += 1
                good += out.equals_indicator(target)
        row["grades"][d] = {"label_support": len(allowed), "label_law_uniform_on_K_perp": bool(law_ok),
                            "arity": M, "tuples": mode, "tuples_with_witnesses_capped": capped,
                            "cases": cases, "merge_outputs_equal_rho_H": good == cases}
        ok = ok and law_ok and good == cases and cases > 0
        v = np.zeros((cfg.laws[d-1].order, p), dtype=np.int64)
        v[target, 0] = 1
        st = XState(d-1, Fraction(1), v)          # every merged output equals this (checked)
    probs = eng.readout(st)
    h_perp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    row["readout_uniform_on_h_perp"] = set(probs) == h_perp and \
        all(v == Fraction(1, len(h_perp)) for v in probs.values())
    row["nullspace_of_readout_support_equals_log_H"] = \
        rref(nullspace(sorted(h_perp), cfg.m, p), p) == rref(inst.log_h, p)
    row["passed"] = bool(ok and row["readout_uniform_on_h_perp"] and row["nullspace_of_readout_support_equals_log_H"])
    row["seconds"] = round(time.time()-t0, 2)
    return row


def run_algorithm(cfg, inst, engine=None, seed=0, extra_samples=4, solver="auto"):
    """Seeded run from oracle access only: exact laws of the simulated modules,
    classical SDE solves between segments, Fourier samples, nullspace."""
    eng = engine or Engine(cfg)
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    top, _, _ = eng.source(inst)
    law_cache = {}
    stats = Counter()

    def law_of(st, key):
        if key not in law_cache:
            law_cache[key] = eng.label_law(st)
        return law_cache[key]

    def sample(probs):
        keys = [k for k in probs if probs[k]]
        return rng.choices(keys, weights=[float(probs[k]) for k in keys], k=1)[0]

    def make(d):
        """Returns (measured label, conditioned state, key) of one grade-d source."""
        if d == c:
            stats["top_sources"] += 1
            probs, states = law_of(top, ("top",))
            lam = sample(probs)
            return lam, states[lam]
        kids = [make(d+1) for _ in range(cfg.arity[d+1])]
        labels = [k[0] for k in kids]
        s, used = solve_sde(labels, d+1, p, rng, solver)
        stats[f"solver_{used}_d{d+1}"] += 1
        out = eng.merge([k[1] for k in kids], s)
        if d == 1:
            return None, out
        key = (d, out.scale, out.v.tobytes())
        probs, states = law_of(out, key)
        lam = sample(probs)
        return lam, states[lam]

    samples = []
    for _ in range(cfg.m+extra_samples):
        if c == 1:
            stats["top_sources"] += 1
            st = top
        else:
            _, st = make(1)
        probs = eng.readout(st)
        samples.append(sample(probs))
    got = rref(nullspace(samples, cfg.m, p), p)
    return got, {"oracle_queries": len(cfg.points)*stats["top_sources"], **dict(stats),
                 "recovered": got == rref(inst.log_h, p)}


def merge_trace_crosscheck(cfg, eng, st, d, s, q_rows):
    """T[q, r] = tr(U_q rho U_r^dagger) = |G|^-1 sum_u phi(u^-1 pi_r^-1(pi_q(u))) from
    the BIT-LEVEL merge permutation (no BCH identity used), against phi(g_q g_r^-1)."""
    perm, flags = merge_bitlevel(cfg, d, s, q_indices=q_rows)
    law = cfg.laws[d]
    E = law.elements()
    inv_idx = law.encode((-E) % cfg.p)
    worst = 0
    for a, q in enumerate(q_rows):
        for b, r in enumerate(q_rows):
            inv_r = np.argsort(perm[b])
            y = inv_r[perm[a]]                              # pi_r^-1(pi_q(u)) for every u
            idx = law.encode(law.mul(E[inv_idx], E[y]))     # u^-1 * y
            T = cyc_canon(st.v[idx].sum(axis=0)[None, :])[0]
            # reference phi(g_q g_r^-1) with g = -delta_s(sigma(.)), all times |G|
            gq = np.zeros(law.n, dtype=np.int64)
            gr = np.zeros(law.n, dtype=np.int64)
            sc = np.array(cfg.scales(d-1, s))
            gq[:cfg.width[d-1]] = -cfg.laws[d-1].decode(q)*sc
            gr[:cfg.width[d-1]] = -cfg.laws[d-1].decode(r)*sc
            k = int(law.encode(law.mul(gq % cfg.p, (-gr) % cfg.p)))
            ref = cyc_canon(st.v[k][None, :]*law.order)[0]
            worst = max(worst, int(np.abs(T-ref).max()))
    return {"pairs": len(q_rows)**2, "max_abs_diff_integer_units": worst, **flags}


# ====================================================================== resources

def primitive_formula(cfg):
    """Primitive counts of one terminal sample (all witness entries nonzero), as
    functions of m, c, the cover dims g_d, D_d = sum_(k<=d) g_k and arities M_d."""
    c, N, D = cfg.c, sources_per_grade(cfg), cfg.width
    out = {"oracle_calls": len(cfg.points)*N[c], "E_s_compute": len(cfg.points)*N[c],
           "E_s_uncompute": len(cfg.points)*N[c], "qft_leaf": D[c]*N[c], "qft_final": cfg.m,
           "central_subtractions": sum(cfg.dims[d-1]*N[d] for d in range(2, c+1)),
           "controlled_right_actions": sum(N[d] for d in range(2, c+1)),
           "bch_passes": 4*sum(N[d] for d in range(2, c+1)),
           "bracket_evaluations": 4*sum(N[d]*len(cfg.nodes[d]) for d in range(2, c+1))}
    for d in range(2, c+1):
        out[f"qft_grade{d}"] = 2*cfg.dims[d-1]*N[d]+D[d-1]*N[d-1]
    return out


def paper_bracket_bound(cfg):
    """thm:uniform-compilation(i): 4 passes x (d-1)d(d+1)(d+2)/6 brackets per action."""
    N = sources_per_grade(cfg)
    return 4*sum(N[d]*(d-1)*d*(d+1)*(d+2)//6 for d in range(2, cfg.c+1))


def width_formula(cfg):
    """Qubits of the assembled terminal-sample circuit without register reuse."""
    c, N, D, nb = cfg.c, sources_per_grade(cfg), cfg.width, cfg.enc.nb
    qudits = N[c]*D[c]+cfg.m+sum(cfg.dims[d-1]*N[d] for d in range(2, c+1)) \
        + sum(D[d]*N[d] for d in range(1, c)) \
        + sum(D[d]+sum(len(sp) for _, _, sp in cfg.nodes[d]) for d in range(2, c+1))
    return nb*qudits+len(cfg.points)*cfg.label_bits*N[c]


def macro_counts(B):
    return dict(Counter(k for k, *_ in B.macros))


def logical_ops(qc):
    ops = Counter()
    for inst in qc.data:
        op = inst.operation
        if isinstance(op, ControlledGate) and op.base_gate.name == "x":
            ops[f"x_with_{op.num_ctrl_qubits}_controls"] += 1
        else:
            ops[op.name] += 1
    return dict(sorted(ops.items()))


def gate_profile(qc, transpile_it=True):
    out = {"qubits": qc.num_qubits, "logical_ops": logical_ops(qc)}
    if transpile_it:
        stripped = QuantumCircuit(*qc.qregs)
        for inst in qc.data:
            if inst.operation.name not in ("measure", "U_f", "barrier"):
                stripped.append(inst.operation, inst.qubits)
        t = transpile(stripped, basis_gates=["cx", "u"], optimization_level=1)
        out["transpiled_cx_u_excluding_oracle"] = dict(t.count_ops())
        out["transpiled_depth_excluding_oracle"] = t.depth()
    return out


def increment_gate_cost(p):
    """A_p = gates of one add_scaled macro = sum_(k=1..p-1) tau(k), tau(k) = sum over the
    transpositions (u, v) of t -> t + k of 2 h(u, v) - 1 (h = Hamming distance).
    An add_product macro costs (p-1) A_p; the counts do not depend on the coefficient."""
    return sum(2*bin(u ^ v).count("1")-1 for k in range(1, p) for u, v in increment_sequence(p, k))


def module_sum_counts(cfg, witness_scale=1):
    """Logical counts of one terminal sample as a sum of module counts with their
    multiplicities (all witness entries = witness_scale), without assembling it."""
    N = sources_per_grade(cfg)
    parts = [(source_circuit(cfg, None)[0], N[cfg.c]), (fourier_circuit(cfg, cfg.m, "qft_final")[0], 1)]
    for d in range(2, cfg.c+1):
        parts += [(instrument_circuit(cfg, d)[0], N[d]), (merge_circuit(cfg, d, witness_scale)[0], N[d]),
                  (fourier_circuit(cfg, cfg.width[d-1], f"qft_grade{d}")[0], N[d-1])]
    total = Counter({"measure": cfg.enc.nb*(cfg.m+sum(cfg.dims[d-1]*N[d] for d in range(2, cfg.c+1)))})
    for qc, mult in parts:
        for k, v in logical_ops(qc).items():
            total[k] += mult*v
    return dict(sorted(total.items()))


def resource_report(cfg, witness=None, transpile_modules=True, transpile_total=False):
    modules = {"source_without_oracle": source_circuit(cfg, None)[0]}
    for d in range(2, cfg.c+1):
        modules[f"instrument_d{d}"] = instrument_circuit(cfg, d)[0]
        for s in range(1, cfg.p):
            modules[f"merge_d{d}_s{s}"] = merge_circuit(cfg, d, s)[0]
        modules[f"q_preparation_d{d}"] = fourier_circuit(cfg, cfg.width[d-1], f"qft_grade{d}")[0]
    modules["readout"] = fourier_circuit(cfg, cfg.m, "qft_final")[0]
    profiles = {k: gate_profile(v, transpile_modules) for k, v in modules.items()}
    qc, B = terminal_sample_circuit(cfg, None, witness)
    total = gate_profile(qc, transpile_total)
    formula = primitive_formula(cfg)
    return {"instance": cfg.name(), "bits_per_coordinate": cfg.enc.nb, "label_bits": cfg.label_bits,
            "bch_nodes": {d: [w for w, _, _ in cfg.nodes[d]] for d in cfg.nodes},
            "modules": profiles,
            "terminal_sample": {"profile": total, "primitive_counts": dict(B.counts),
                                "formula": formula, "width_formula": width_formula(cfg),
                                "bracket_bound_thm_uniform_compilation_i": paper_bracket_bound(cfg),
                                "macro_counts": macro_counts(B)}}


# ====================================================================== instances

def all_subalgebras(alg):
    """Every Lie subalgebra (RREF basis) by enumerating RREF subspaces."""
    p, n = alg.p, alg.dim
    out = [[]]
    for k in range(1, n+1):
        for piv in combinations(range(n), k):
            free = [(r, j) for r in range(k) for j in range(piv[r]+1, n) if j not in piv]
            for vals in product(range(p), repeat=len(free)):
                M = np.zeros((k, n), dtype=np.int64)
                for r in range(k):
                    M[r, piv[r]] = 1
                for (r, j), v in zip(free, vals):
                    M[r, j] = v
                basis = [tuple(int(x) for x in row) for row in M]
                if alg.lie_closure(basis) == basis:
                    out.append(basis)
    return out


def heis3_instances():
    alg = heisenberg(3)
    out = []
    for basis in all_subalgebras(alg):
        tag = "normal" if alg.is_ideal(basis) else "non-normal"
        out.append(Hidden(f"Heis(F_3) H=<{basis}> {tag}", alg, tuple(tuple(v) for v in basis)))
    return out


N4_SUBGROUPS = [("<e2> non-normal", ((0, 1, 0, 0),)), ("<e1> non-normal", ((1, 0, 0, 0),)),
                ("<e1+e3> non-normal", ((1, 0, 1, 0),)), ("<e2,e4> non-normal", ((0, 1, 0, 0), (0, 0, 0, 1))),
                ("<e1+e2,e3> (closure)", ((1, 1, 0, 0), (0, 0, 1, 0))),
                ("<e3,e4> = gamma_2", ((0, 0, 1, 0), (0, 0, 0, 1))),
                ("<e2,e3> non-normal", ((0, 1, 0, 0), (0, 0, 1, 0))), ("Z(G)", ((0, 0, 0, 1),)),
                ("trivial", ())]


def n4_instances(p=5):
    alg = filiform4(p)
    return [Hidden(f"{alg.name} H={n}", alg, g) for n, g in N4_SUBGROUPS]


# ====================================================================== report

def report(jobs=("heis_f3", "n4_f5"), seeds=(20261103, 20261104), log=print):
    """Full exact run. Settings per job: (config, instances, check kwargs, bit-level plan)."""
    t0 = time.time()
    out = {**STATUS, "runs": {}}
    plans = {
        "heis_f3": (lambda: Config(heisenberg(3)), heis3_instances, {}, "all"),
        "n4_f5": (lambda: Config(filiform4(5)), lambda: n4_instances(5),
                  dict(max_cases=4000, sample_tuples=6), "d2_all_d3_rows"),
        "n4_f5_is_arity18": (lambda: Config(filiform4(5), arities={2: 18}), lambda: n4_instances(5),
                             None, None),
        "n4_f7": (lambda: Config(filiform4(7)), lambda: n4_instances(7),
                  dict(max_cases=50, sample_tuples=4, max_witnesses=12), "rows"),
    }
    for key in jobs:
        make_cfg, make_insts, kw, bit_plan = plans[key]
        cfg, insts = make_cfg(), make_insts()
        rec = {"config": cfg.name(), "merge_proofs": {}, "merge_bitlevel": {}}
        if kw is not None:
            for d in range(2, cfg.c+1):
                for s in range(1, cfg.p):
                    rec["merge_proofs"][f"d{d}_s{s}"] = prove_merge(cfg, d, s)
                    nQ = cfg.p**cfg.width[d-1]
                    if bit_plan == "all" or (bit_plan == "d2_all_d3_rows" and d == 2):
                        rows = None
                    else:
                        rows = np.unique(np.linspace(0, nQ-1, 16 if cfg.p > 5 else 64).astype(np.int64))
                    rec["merge_bitlevel"][f"d{d}_s{s}"] = merge_bitlevel(cfg, d, s, q_indices=rows)[1]
            log(key, "merges", round(time.time()-t0, 1), "s")
        eng = Engine(cfg)
        rec["instrument"] = {d: eng.kernels[d][1] for d in eng.kernels}
        rec["checks"] = []
        if kw is not None:
            for inst in insts:
                row = check_instance(cfg, inst, eng, **kw)
                rec["checks"].append(row)
                log(key, inst.name, "OK" if row["passed"] else "FAIL", row["seconds"], "s")
        rec["seeded_runs"] = []
        for inst in insts:
            for seed in (seeds if kw is not None and key != "n4_f7" else seeds[:1]):
                got, info = run_algorithm(cfg, inst, eng, seed=seed,
                                          extra_samples=2 if key in ("n4_f7", "n4_f5_is_arity18") else 4)
                rec["seeded_runs"].append({"instance": inst.name, "normal": inst.normal, "seed": seed, **info})
        rec["all_checks_pass"] = all(r["passed"] for r in rec["checks"])
        rec["all_runs_recover"] = all(r["recovered"] for r in rec["seeded_runs"])
        rec["all_merges_proved"] = all(f["proved"] for f in rec["merge_proofs"].values())
        rec["all_bitlevel_ok"] = all(all(v for k, v in f.items() if k != "inputs")
                                     for f in rec["merge_bitlevel"].values())
        out["runs"][key] = rec
        log(key, "checks", rec["all_checks_pass"], "runs", rec["all_runs_recover"], "merges",
            rec["all_merges_proved"], "bitlevel", rec["all_bitlevel_ok"], round(time.time()-t0, 1), "s")
    out["seconds"] = round(time.time()-t0, 1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", help="write JSON here")
    ap.add_argument("--jobs", default="heis_f3,n4_f5,n4_f5_is_arity18",
                    help="comma list of heis_f3, n4_f5, n4_f5_is_arity18, n4_f7")
    ap.add_argument("--resources", action="store_true", help="also write resource reports")
    ap.add_argument("--instrument", choices=["exact", "float"], default="exact",
                    help="instrument exponent derivation (INSTRUMENT_EXPONENTS)")
    args = ap.parse_args()
    global INSTRUMENT_EXPONENTS
    INSTRUMENT_EXPONENTS = args.instrument
    res = report(jobs=tuple(args.jobs.split(",")), log=lambda *a: print(*a, flush=True))
    if args.resources:
        res["resources"] = {}
        for key, alg in (("heis_f3", heisenberg(3)), ("n4_f5", filiform4(5))):
            res["resources"][key] = resource_report(Config(alg), witness=(1, 2, 1) if key == "heis_f3" else None,
                                                    transpile_total=(key == "heis_f3"))
    text = json.dumps(res, indent=1, default=str)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text+"\n")
    print(json.dumps({k: v for k, v in res.items() if k != "runs"}, default=str)[:2000])


if __name__ == "__main__":
    main()
