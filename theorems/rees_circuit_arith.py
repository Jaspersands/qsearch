"""poly(log p) reversible arithmetic backend for the gate-level Rees circuit generator.

Adds to theorems/rees_circuit_general.py (imported, not edited) a drop-in
Builder subclass, ArithBuilder, that emits the SAME macros with the SAME
semantics and the SAME macro records (kind, qudits, coeff mod p, start, end)
as rees_circuit_general.Builder, but synthesises the mod-p arithmetic with
standard reversible binary circuits instead of value-controlled increments.
AI-checked, pending human review.

Gate set: X, CX, CCX and SWAP only (no MCX with more than two controls), so
every gate list is an exact permutation of basis states.

Building blocks (b = ceil(log2 p) bits per F_p coordinate, LSB first):
* Cuccaro-Draper-Kutin-Moulton ripple-carry adder B += A on b bits with the
  carry XORed into an extension bit e, so (B, e) += A mod 2^(b+1)
  (2b CCX, 4b+1 CX); subtraction by two's complement (X on (B, e), add, X);
* modular adder t += y mod p for t, y < p (Vedral-Barenco-Ekert /
  Beauregard pattern): add y, subtract p, copy the sign bit e to a flag f,
  add p back controlled on f, then clear f by comparing the result with y
  (subtract y, CX e->f, add y back); 5 adders. The constant p is loaded into
  a scratch register P with X (or CX from a control) gates and unloaded.
  With an optional control g the p loads are controlled on g and the final
  flag clear is CX(g, f); the caller guarantees y = 0 when g = 0, and then
  the whole block is the identity on EVERY word of t (also padding);
* constant multiplication t += k*a mod p by shift-and-add of doubled
  constants: for each bit a_i the constant k_i = k 2^i mod p is loaded into Y
  controlled on a_i (CX, or CCX with the guard), then t += Y mod p, unload;
* modular doubling r -> 2r mod p (p odd): rotate (r, e) one place with SWAPs,
  subtract p, copy the sign to f, add p back controlled on f, and clear f with
  CX(r_0, f), X(f) (the result is odd iff p was subtracted);
* controlled modular multiply-accumulate t += k*a*b mod p: r = k*b mod p by
  constant multiplication into a clean scratch register r, then for each bit
  a_i: t += r mod p controlled on a_i (load Y = r via CCX through h = g & a_i)
  and r <- 2r mod p; afterwards the doublings and r = k*b are uncomputed by
  the reversed gate list (all gates are involutions).

Padding (words >= p). The existing Builder promises, in increment(), that
"t's padding is fixed", and its macros are permutations of the qudit words;
nothing else is promised about non-canonical words (its value tests may fire
on padding of the operands). This backend keeps both promises, and more:
every macro first computes g = [t < p] into an ancilla (compare by
subtracting p, copy the sign bit, add p back) and controls every update of t
on g, then recomputes g from the final t to clear it (canonical t stays
canonical, padding t is untouched). Exactly, on every basis word:
  (A1) on canonical t, a, b the macro is t += coeff*a(*b) mod p;
  (A2) if t >= p the macro is the identity;
  (A3) if t < p and a, b are any words, t += coeff*[a]*[b] mod p with [a] the
       integer value of the word (so padding operands act as integers);
  (A4) the operands are never targeted and every ancilla returns to 0.
(A1)-(A4) are checked exhaustively for p in {3, 5, 7, 11, 13} on all words.

Ancillas: one AncillaRegister "arith" of 3b+5 qubits per circuit (Y, P, r,
e, c0, f, g, h), allocated on first use and shared by all macros (it is clean
between macros). Gate counts per macro do not depend on p beyond b and the
bit patterns of the loaded constants.

Integration (no existing file edited): arith_backend() is a context manager
that rebinds rees_circuit_general.Builder to ArithBuilder, check_macros to a
version that includes the ancilla register (and checks it returns to 0), and
instrument_semantics (in rees_circuit_general and rees_circuit_sparse) to a
version that first reduces each arithmetic macro to the permutation it
induces on its qudits with ancilla 0 (checked on all words). Every other
function of the two modules (source evaluation from the gate list, prove_merge,
merge_bitlevel, the dense and sparse engines, check_instance(_sparse),
run_algorithm(_sparse)) then runs unchanged on the new circuits.

What this does NOT show: a QFT_p at poly(log p) (QFT_p is still one exact
b-qubit unitary, small p only); a coherent receiver
(coherent_receiver_implemented stays false); anything about the oracle cost
T_f; noise; any asymptotic claim beyond the gate counts of the arithmetic.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from itertools import product
import json
import math
import random
import time

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import AncillaRegister, CircuitInstruction
from qiskit.circuit.library import CCXGate, CXGate, SwapGate, UnitaryGate, XGate

import theorems.rees_circuit_general as G

ARITH_STATUS = {**G.STATUS,
                "status": "poly_log_p_reversible_arithmetic_backend_for_generated_circuits_finite_checks",
                "coherent_receiver_implemented": False, "qft_poly_log_p_implemented": False,
                "poly_log_p_arithmetic_implemented": True}

_GATES = {"x": XGate(), "cx": CXGate(), "ccx": CCXGate(), "swap": SwapGate()}


# ====================================================================== gate-list layer

class Ops(list):
    """A gate list: entries (name, qubits) with name in x, cx, ccx, swap; qubits
    are (control..., target). Every gate is an involution, so the inverse of a
    list is the reversed list."""

    def x(self, q):
        self.append(("x", (q,)))

    def cx(self, c, t):
        self.append(("cx", (c, t)))

    def ccx(self, c1, c2, t):
        self.append(("ccx", (c1, c2, t)))

    def swap(self, a, b):
        self.append(("swap", (a, b)))

    def ctrl_x(self, ctrls, t):
        """X on t controlled on all of ctrls (0, 1 or 2 controls)."""
        if len(ctrls) == 0:
            self.x(t)
        elif len(ctrls) == 1:
            self.cx(ctrls[0], t)
        elif len(ctrls) == 2:
            self.ccx(ctrls[0], ctrls[1], t)
        else:
            raise ValueError("at most two controls")

    def inverse(self):
        return Ops(reversed(self))


class Anc:
    """Ancilla layout: Y, P, r (b qubits each), e, c0, f, g, h."""

    def __init__(self, reg, nb):
        q = list(reg)
        self.Y, self.P, self.r = q[:nb], q[nb:2*nb], q[2*nb:3*nb]
        self.e, self.c0, self.f, self.g, self.h = q[3*nb:3*nb+5]
        self.all = q


def anc_size(nb):
    return 3*nb+5


def cuccaro_add(ops, A, B, c0, z):
    """(B, z) += A: B += A on len(A) bits, carry-out XORed into z; A, c0 restored."""
    n = len(A)
    assert len(B) == n

    def maj(c, b, a):
        ops.cx(a, b)
        ops.cx(a, c)
        ops.ccx(c, b, a)

    def uma(c, b, a):
        ops.ccx(c, b, a)
        ops.cx(a, c)
        ops.cx(c, b)

    maj(c0, B[0], A[0])
    for i in range(1, n):
        maj(A[i-1], B[i], A[i])
    ops.cx(A[n-1], z)
    for i in range(n-1, 0, -1):
        uma(A[i-1], B[i], A[i])
    uma(c0, B[0], A[0])


def add_ext(ops, A, t, e, c0):
    """(t, e) += A mod 2^(b+1)."""
    cuccaro_add(ops, A, t, c0, e)


def sub_ext(ops, A, t, e, c0):
    """(t, e) -= A mod 2^(b+1) (two's complement: NOT(NOT T + A))."""
    for q in list(t)+[e]:
        ops.x(q)
    cuccaro_add(ops, A, t, c0, e)
    for q in list(t)+[e]:
        ops.x(q)


def load_const(ops, k, Y, ctrls=()):
    """Y ^= k (when all ctrls are 1)."""
    for j, q in enumerate(Y):
        if k >> j & 1:
            ops.ctrl_x(list(ctrls), q)


def mod_add_reg(ops, p, Y, t, A, ctrl=None):
    """t += Y mod p for t, Y < p (ctrl None or 1). With ctrl = g = 0 the caller
    guarantees Y = 0, and the block is then the identity on every word of t.
    Uses A.P, A.e, A.c0, A.f; all return to 0."""
    cs = () if ctrl is None else (ctrl,)
    add_ext(ops, Y, t, A.e, A.c0)              # T = t + y
    load_const(ops, p, A.P, cs)
    sub_ext(ops, A.P, t, A.e, A.c0)            # T = t + y - p
    load_const(ops, p, A.P, cs)
    ops.cx(A.e, A.f)                           # f = [t + y < p]
    load_const(ops, p, A.P, (A.f,))
    add_ext(ops, A.P, t, A.e, A.c0)            # T = (t + y) mod p, e = 0
    load_const(ops, p, A.P, (A.f,))
    sub_ext(ops, Y, t, A.e, A.c0)              # e = [r < y]
    ops.cx(A.e, A.f)                           # f = 1 whenever ctrl = 1
    add_ext(ops, Y, t, A.e, A.c0)
    if ctrl is None:
        ops.x(A.f)
    else:
        ops.cx(ctrl, A.f)


def less_than_p(ops, p, t, A, out):
    """out ^= [t < p] for any b-bit word t (t restored)."""
    load_const(ops, p, A.P)
    sub_ext(ops, A.P, t, A.e, A.c0)            # sign bit e = [t < p]
    ops.cx(A.e, out)
    add_ext(ops, A.P, t, A.e, A.c0)
    load_const(ops, p, A.P)


def mod_double(ops, p, r, A):
    """r -> 2 r mod p for r < p, p odd (uses A.e as the (b+1)-th bit, A.P, A.c0, A.f)."""
    n = len(r)
    ops.swap(A.e, r[n-1])                      # (r, e) <- 2 r (rotation, e was 0)
    for i in range(n-1, 0, -1):
        ops.swap(r[i], r[i-1])
    load_const(ops, p, A.P)
    sub_ext(ops, A.P, r, A.e, A.c0)            # e = [2r < p]
    load_const(ops, p, A.P)
    ops.cx(A.e, A.f)
    load_const(ops, p, A.P, (A.f,))
    add_ext(ops, A.P, r, A.e, A.c0)
    load_const(ops, p, A.P, (A.f,))
    ops.cx(r[0], A.f)                          # result odd  <=> p subtracted <=> f = 0
    ops.x(A.f)


def const_mul_acc(ops, p, t, a, k, A, guard):
    """t += k * [a] mod p (shift and add of k 2^i mod p), t < p when guard is None;
    with guard = g, every load is also controlled on g."""
    k %= p
    for i, ai in enumerate(a):
        ki = k*pow(2, i, p) % p
        cs = (ai,) if guard is None else (guard, ai)
        load_const(ops, ki, A.Y, cs)
        mod_add_reg(ops, p, A.Y, t, A, guard)
        load_const(ops, ki, A.Y, cs)


def add_scaled_ops(p, t, a, coeff, A):
    """t += coeff * a mod p on canonical inputs; (A1)-(A4) of the module docstring."""
    ops = Ops()
    less_than_p(ops, p, t, A, A.g)
    const_mul_acc(ops, p, t, a, coeff, A, A.g)
    less_than_p(ops, p, t, A, A.g)
    return ops


def add_product_ops(p, t, a, b, coeff, A):
    """t += coeff * a * b mod p on canonical inputs; (A1)-(A4) of the module docstring."""
    ops = Ops()
    less_than_p(ops, p, t, A, A.g)
    pre = Ops()
    const_mul_acc(pre, p, A.r, b, coeff, A, None)   # r = coeff [b] mod p (r starts at 0)
    ops += pre
    dbl = Ops()
    mod_double(dbl, p, A.r, A)
    n = len(a)
    for i, ai in enumerate(a):
        ops.ccx(A.g, ai, A.h)                       # h = g & a_i
        for rj, yj in zip(A.r, A.Y):
            ops.ccx(A.h, rj, yj)                    # Y = h ? r : 0
        mod_add_reg(ops, p, A.Y, t, A, A.g)         # t += Y mod p
        for rj, yj in zip(A.r, A.Y):
            ops.ccx(A.h, rj, yj)
        ops.ccx(A.g, ai, A.h)
        if i < n-1:
            ops += dbl                              # r = coeff 2^(i+1) [b] mod p
    inv_dbl = dbl.inverse()
    for _ in range(n-1):
        ops += inv_dbl
    ops += pre.inverse()
    less_than_p(ops, p, t, A, A.g)
    return ops


def const_add_ops(p, t, k, A):
    """t += k mod p (guarded as the macros: identity on padding t)."""
    ops = Ops()
    k %= p
    less_than_p(ops, p, t, A, A.g)
    load_const(ops, k, A.Y, (A.g,))
    mod_add_reg(ops, p, A.Y, t, A, A.g)
    load_const(ops, k, A.Y, (A.g,))
    less_than_p(ops, p, t, A, A.g)
    return ops


# ====================================================================== the Builder

class ArithBuilder(G.Builder):
    """rees_circuit_general.Builder with poly(log p) binary arithmetic.
    Same macro kinds, qudits, coefficients and records; extra: an ancilla
    register 'arith' and gate_counts (x, cx, ccx, swap) of the arithmetic.
    count_only=True counts without appending gates (records use a virtual
    gate index); macro costs are then cached per (kind, coeff)."""

    count_only = False

    def __init__(self, qc, enc):
        super().__init__(qc, enc)
        if self.p < 3 or self.p % 2 == 0:
            raise ValueError("odd prime p needed")
        self.nb = enc.nb
        self.anc_reg, self.A = None, None
        self.gate_counts = Counter()
        self._n = 0
        self._cost = {}

    # -- plumbing
    def _ancillas(self):
        if self.A is None:
            self.anc_reg = AncillaRegister(anc_size(self.nb), "arith")
            self.qc.add_register(self.anc_reg)
            self.A = Anc(self.anc_reg, self.nb)
        return self.A

    def _len(self):
        return self._n if self.count_only else len(self.qc.data)

    def _emit(self, ops):
        self.gate_counts.update(name for name, _ in ops)
        self._n += len(ops)
        if not self.count_only:
            app = self.qc._append
            for name, qs in ops:
                app(CircuitInstruction(_GATES[name], qs))

    def _emit_cached(self, key, make):
        if self.count_only and key in self._cost:
            cnt, n = self._cost[key]
            self.gate_counts.update(cnt)
            self._n += n
            return
        ops = make()
        if self.count_only:
            self._cost[key] = (Counter(name for name, _ in ops), len(ops))
        self._emit(ops)

    def _macro(self, kind, qudits, coeff, start):
        self.macros.append((kind, tuple(qudits), coeff % self.p if coeff is not None else None,
                            start, self._len()))

    # -- arithmetic
    def increment(self, t, k, controls=()):
        """t += k (mod p); padding of t fixed. Value-controlled increments are
        exactly what this backend replaces, so controls are not supported."""
        if controls:
            raise NotImplementedError("value-controlled increments are the O(p) synthesis; use add_scaled")
        if not k % self.p:
            return
        A = self._ancillas()
        self._emit_cached(("inc", k % self.p), lambda: const_add_ops(self.p, list(t), k, A))

    def add_scaled(self, t, a, coeff):
        """t += coeff * a."""
        if not coeff % self.p:
            return
        if t == a:
            raise ValueError("add_scaled needs two distinct qudits")
        A = self._ancillas()
        start = self._len()
        self._emit_cached(("add_scaled", coeff % self.p),
                          lambda: add_scaled_ops(self.p, list(t), list(a), coeff, A))
        self._macro("add_scaled", (t, a), coeff, start)

    def add_product(self, t, a, b, coeff):
        """t += coeff * a * b."""
        if not coeff % self.p:
            return
        if len({t, a, b}) != 3:
            raise ValueError("add_product needs three distinct qudits")
        A = self._ancillas()
        start = self._len()
        self._emit_cached(("add_product", coeff % self.p),
                          lambda: add_product_ops(self.p, list(t), list(a), list(b), coeff, A))
        self._macro("add_product", (t, a, b), coeff, start)

    def swap(self, a, b):
        start = self._len()
        ops = Ops()
        for x, y in zip(a, b):                      # qudits (tuples of qubits), as qc.swap broadcasts
            for u, v in (zip(x, y) if isinstance(x, tuple) else [(x, y)]):
                ops.swap(u, v)
        self._emit(ops)
        self.gate_counts["swap"] -= len(ops)        # data movement, not arithmetic
        self.gate_counts["swap_macro"] += len(ops)
        self._macro("swap", tuple(a)+tuple(b), None, start)

    def qft(self, q, role, inverse=False):
        if not self.count_only:
            return super().qft(q, role, inverse)
        start = self._len()
        self._n += 1
        self.counts[role] += 1
        self.gate_counts["qft_unitary"] += 1
        self._macro("qft_dg" if inverse else "qft", (q,), None, start)

    def oracle(self, U, w_reg, y):
        if not self.count_only:
            return super().oracle(U, w_reg, y)
        start = self._len()
        self._n += 1 if U is not None else 0
        self.counts["oracle_calls"] += 1
        self._macro("oracle", (), None, start)


class CountingArithBuilder(ArithBuilder):
    count_only = True


def arith_gate_counts(B):
    """x / cx / ccx / swap counts of the arithmetic (macro swaps listed separately)."""
    c = {k: v for k, v in B.gate_counts.items() if v}
    c["arith_total"] = sum(c.get(k, 0) for k in ("x", "cx", "ccx", "swap"))
    return c


# ====================================================================== checks

def _sim_slice(qc, B, start, end, qudits, values):
    """Run the gate slice on the given qudit values (rows) with every ancilla 0.
    Returns (qudit outputs, ancilla outputs as bit matrix, set of target positions).
    Raises if a gate touches a qubit outside qudits + ancillas."""
    nb = B.enc.nb
    anc = list(getattr(B, "anc_reg", None) or [])
    local = {qb: r*nb+i for r, q in enumerate(qudits) for i, qb in enumerate(q)}
    for j, qb in enumerate(anc):
        local[qb] = nb*len(qudits)+j
    for inst in qc.data[start:end]:
        if any(q not in local for q in inst.qubits):
            raise AssertionError("macro gate touches a qubit outside its qudits and the ancilla register")
    ops = G.compile_ops(qc.data[start:end], local)
    sim = G.BitSim(len(local), len(values))
    wires = [[r*nb+i for i in range(nb)] for r in range(len(qudits))]
    sim.load(wires, values)
    sim.run(ops)
    out = sim.read(wires)
    anc_out = np.stack([sim._unpack(nb*len(qudits)+j) for j in range(len(anc))], axis=1) if anc else \
        np.zeros((len(values), 0), dtype=np.int64)
    targets = {i for i in sim.targets}
    return out, anc_out, targets


def _want(kind, coeff, vals, p):
    want = vals.copy()
    if kind == "add_scaled":
        want[:, 0] = (vals[:, 0]+coeff*vals[:, 1]) % p
    elif kind == "add_product":
        want[:, 0] = (vals[:, 0]+coeff*vals[:, 1]*vals[:, 2]) % p
    else:
        raise AssertionError(kind)
    return want


_ARITH_CACHE = {}


def check_macros_arith(qc, B):
    """rees_circuit_general.check_macros with the ancilla register: every gate
    belongs to exactly one macro; each arithmetic macro's gate slice, on ALL
    canonical values of its qudits with ancillas 0, is the declared map, touches
    only its qudits and the ancillas, returns every ancilla to 0 and never
    targets an operand. qft / oracle / swap macros are checked as in the original."""
    p, nb = B.p, B.enc.nb
    covered = 0
    data = qc.data
    anc = set(B.anc_reg) if getattr(B, "anc_reg", None) is not None else set()
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
        local = {qb: ("q", r, i) for r, q in enumerate(qudits) for i, qb in enumerate(q)}
        for j, qb in enumerate(B.anc_reg or []):
            local[qb] = ("a", j)
        try:
            sig = (kind, coeff, tuple((inst.operation.name, tuple(local[q] for q in inst.qubits))
                                      for inst in data[start:end]))
        except KeyError:
            raise AssertionError("macro gate touches a qubit outside its qudits and the ancilla register")
        if sig in _ARITH_CACHE:
            continue
        vals = np.array(list(product(range(p), repeat=len(qudits))), dtype=np.int64)
        out, anc_out, targets = _sim_slice(qc, B, start, end, qudits, vals)
        if (out != _want(kind, coeff, vals, p)).any():
            raise ArithmeticError(f"macro {kind} gate slice is not its declared map")
        if anc_out.any():
            raise ArithmeticError(f"macro {kind} leaves an ancilla dirty")
        if any(r*nb+i in targets for r in range(1, len(qudits)) for i in range(nb)):
            raise ArithmeticError(f"macro {kind} targets an operand")
        _ARITH_CACHE[sig] = True
    if covered != len(data):
        raise AssertionError("trailing gates outside every macro")
    return len(B.macros)


def _qudit_reg(name, n, enc):
    return G.qudit_register(name, n, enc)


def macro_circuit(p, kind, coeff, builder=None):
    """One macro on fresh qudits t, a (, b): (qc, B, qudits)."""
    enc = G.Encoding(p)
    builder = builder or ArithBuilder
    k = 2 if kind == "add_scaled" else 3
    regs, qds = [], []
    for name in "tab"[:k]:
        r, q = _qudit_reg(name, 1, enc)
        regs.append(r)
        qds.append(q[0])
    qc = QuantumCircuit(*regs)
    B = builder(qc, enc)
    if kind == "add_scaled":
        B.add_scaled(qds[0], qds[1], coeff)
    else:
        B.add_product(qds[0], qds[1], qds[2], coeff)
    return qc, B, qds


def exhaustive_macro_check(p, kinds=("add_scaled", "add_product")):
    """For every coefficient 1..p-1: (A1) on all canonical inputs, (A2)-(A4) and
    bijectivity on ALL 2^(k b) words with ancilla 0; also the promises of the
    ORIGINAL Builder on the same words (padding t fixed, permutation), and
    equality of the two on canonical inputs."""
    enc = G.Encoding(p)
    nb = enc.nb
    rows = []
    for kind in kinds:
        k = 2 if kind == "add_scaled" else 3
        words = np.array(list(product(range(1 << nb), repeat=k)), dtype=np.int64)
        canon = (words < p).all(axis=1)
        for coeff in range(1, p):
            qc, B, qds = macro_circuit(p, kind, coeff)
            (kind_r, qrec, crec, start, end), = B.macros
            out, anc_out, targets = _sim_slice(qc, B, start, end, qds, words)
            new = {"p": p, "kind": kind, "coeff": coeff, "gates": end-start,
                   "gate_counts": arith_gate_counts(B), "words": int(len(words)),
                   "canonical_inputs": int(canon.sum())}
            want = _want(kind, coeff, words, p)
            new["A1_canonical_map"] = bool((out[canon] == want[canon]).all())
            tpad = words[:, 0] >= p
            new["A2_identity_when_t_padding"] = bool((out[tpad] == words[tpad]).all())
            prod_int = words[:, 1] if k == 2 else words[:, 1]*words[:, 2]
            ok3 = ~tpad
            new["A3_integer_operands_when_t_canonical"] = bool(
                (out[ok3, 0] == (words[ok3, 0]+coeff*prod_int[ok3]) % p).all()
                and (out[ok3, 1:] == words[ok3, 1:]).all())
            new["A4_ancilla_clean_all_words"] = not anc_out.any()
            new["A4_operands_never_targeted"] = not any(r*nb+i in targets for r in range(1, k) for i in range(nb))
            enc_w = out @ ((1 << nb)**np.arange(k))
            new["bijective_on_words"] = len(np.unique(enc_w)) == len(words)
            new["macro_record_ok"] = (kind_r, crec, qrec) == (kind, coeff % p, tuple(qds))
            # the original Builder on the same words
            qo, Bo, qdo = macro_circuit(p, kind, coeff, builder=G.Builder)
            (_, _, _, so, eo), = Bo.macros
            outo, _, _ = _sim_slice(qo, Bo, so, eo, qdo, words)
            new["old_gates"] = eo-so
            new["old_t_padding_fixed"] = bool((outo[tpad] == words[tpad]).all())
            new["old_bijective_on_words"] = len(np.unique(outo @ ((1 << nb)**np.arange(k)))) == len(words)
            new["equals_old_on_canonical"] = bool((outo[canon] == out[canon]).all())
            new["equals_old_on_all_words"] = bool((outo == out).all())
            new["ok"] = all(new[f] for f in ("A1_canonical_map", "A2_identity_when_t_padding",
                                             "A3_integer_operands_when_t_canonical", "A4_ancilla_clean_all_words",
                                             "A4_operands_never_targeted", "bijective_on_words", "macro_record_ok",
                                             "old_t_padding_fixed", "old_bijective_on_words",
                                             "equals_old_on_canonical"))
            rows.append(new)
    return rows


def primitive_checks(p):
    """Exhaustive checks of the building blocks on all relevant words (ancilla 0)."""
    enc = G.Encoding(p)
    nb = enc.nb
    out = {}

    def run(build, regs_vals, nregs):
        regs, qds = [], []
        for i in range(nregs):
            r, q = _qudit_reg(f"u{i}", 1, enc)
            regs.append(r)
            qds.append(list(q[0]))
        a = AncillaRegister(anc_size(nb), "arith")
        qc = QuantumCircuit(*regs, a)
        A = Anc(a, nb)
        ops = build(qds, A)
        pos = {q: i for i, q in enumerate(qc.qubits)}
        cops = [("x" if n == "x" else "swap" if n == "swap" else "mcx", [pos[q] for q in qs],
                 (1 << (len(qs)-1))-1, len(qs)-1) for n, qs in ops]
        sim = G.BitSim(qc.num_qubits, len(regs_vals))
        wires = [[pos[q] for q in qd] for qd in qds]
        sim.load(wires, regs_vals)
        sim.run(cops)
        res = sim.read(wires)
        anc = np.stack([sim._unpack(pos[q]) for q in A.all], axis=1)
        return res, anc, len(ops)

    # Cuccaro: (B, z) += A over all b-bit A, B, z = r[0] of the ancilla (borrowed as a clean bit)
    W = np.array(list(product(range(1 << nb), repeat=2)), dtype=np.int64)
    res, anc, n = run(lambda q, A: _tap(lambda o: add_ext(o, q[0], q[1], A.e, A.c0)), W, 2)
    out["cuccaro_low_bits"] = bool((res[:, 1] == (W[:, 0]+W[:, 1]) % (1 << nb)).all())
    out["cuccaro_carry_bit"] = bool((anc[:, 3*nb] == (W[:, 0]+W[:, 1]) >> nb).all())
    out["cuccaro_addend_restored"] = bool((res[:, 0] == W[:, 0]).all())
    out["cuccaro_gates"] = n
    # modular adder, both control modes, on canonical t, y
    C = np.array(list(product(range(p), repeat=2)), dtype=np.int64)
    res, anc, n = run(lambda q, A: _tap(lambda o: mod_add_reg(o, p, q[0], q[1], A)), C, 2)
    out["mod_add_correct"] = bool((res[:, 1] == (C[:, 0]+C[:, 1]) % p).all() and (res[:, 0] == C[:, 0]).all())
    out["mod_add_ancilla_clean"] = not anc.any()
    out["mod_add_gates"] = n
    # modular doubling on r (in the ancilla register r), r = word in u0 copied in by CX
    R = np.arange(p, dtype=np.int64)[:, None]

    def dbl(q, A):
        o = Ops()
        for x, y in zip(q[0], A.r):
            o.cx(x, y)
        mod_double(o, p, A.r, A)
        return o
    res, anc, n = run(dbl, R, 1)
    r_out = sum(anc[:, 2*nb+i] << i for i in range(nb))
    out["mod_double_correct"] = bool((r_out == (2*R[:, 0]) % p).all())
    rest = np.delete(anc, list(range(2*nb, 3*nb)), axis=1)
    out["mod_double_other_ancillas_clean"] = not rest.any()
    out["mod_double_gates"] = n-nb
    # comparator on all words
    T = np.arange(1 << nb, dtype=np.int64)[:, None]
    res, anc, n = run(lambda q, A: _tap(lambda o: less_than_p(o, p, q[0], A, A.g)), T, 1)
    out["less_than_p_correct"] = bool((anc[:, 3*nb+3] == (T[:, 0] < p)).all() and (res[:, 0] == T[:, 0]).all())
    out["less_than_p_gates"] = n
    out["ok"] = all(v for k, v in out.items() if not k.endswith("_gates"))
    return out


def _tap(f):
    o = Ops()
    f(o)
    return o


# ====================================================================== integration hooks

def reduced_instrument_circuit(cfg, d):
    """The instrument circuit built with ArithBuilder, with each arithmetic macro
    replaced by the permutation it induces on its qudits with ancillas 0
    (checked on ALL words: ancillas return to 0, bijective). Same registers
    a, z, so rees_circuit_general.instrument_semantics applies unchanged."""
    qc, B, (a_reg, a, z_reg, z) = _ORIG["instrument_circuit"](cfg, d)
    nb = cfg.enc.nb
    out = QuantumCircuit(a_reg, z_reg, name=qc.name)
    for kind, qudits, coeff, start, end in B.macros:
        if kind in ("add_scaled", "add_product"):
            k = len(qudits)
            words = np.array(list(product(range(1 << nb), repeat=k)), dtype=np.int64)
            res, anc, _ = _sim_slice(qc, B, start, end, qudits, words)
            if anc.any():
                raise ArithmeticError("instrument macro leaves an ancilla dirty")
            w = (1 << nb)**np.arange(k)
            src, dst = words @ w, res @ w
            if len(np.unique(dst)) != len(dst):
                raise ArithmeticError("instrument macro is not a permutation of its qudits")
            M = np.zeros((1 << (nb*k), 1 << (nb*k)))
            M[dst, src] = 1.0
            out.append(UnitaryGate(M, label=f"{kind}_perm"), [qb for q in qudits for qb in q])
        else:
            for inst in qc.data[start:end]:
                out.append(inst.operation, inst.qubits)
    return out, B, (a_reg, a, z_reg, z)


_ORIG = {}


def instrument_semantics_arith(cfg, d, **kw):
    saved = G.instrument_circuit
    G.instrument_circuit = reduced_instrument_circuit
    try:
        return _ORIG["instrument_semantics"](cfg, d, **kw)
    finally:
        G.instrument_circuit = saved


@contextmanager
def arith_backend(builder=None):
    """Rebind the generator's Builder (and the two checks that read gate slices)
    to the poly(log p) backend for the duration of the block."""
    import theorems.rees_circuit_sparse as S
    builder = builder or ArithBuilder
    saved = {"Builder": G.Builder, "check_macros": G.check_macros,
             "instrument_semantics": G.instrument_semantics, "S_instrument_semantics": S.instrument_semantics}
    _ORIG.setdefault("instrument_circuit", G.instrument_circuit)
    _ORIG.setdefault("instrument_semantics", G.instrument_semantics)
    G.Builder = builder
    G.check_macros = check_macros_arith
    G.instrument_semantics = instrument_semantics_arith
    S.instrument_semantics = instrument_semantics_arith
    try:
        yield
    finally:
        G.Builder = saved["Builder"]
        G.check_macros = saved["check_macros"]
        G.instrument_semantics = saved["instrument_semantics"]
        S.instrument_semantics = saved["S_instrument_semantics"]


def merge_bitlevel_arith(cfg, d, s, q_indices=None, x_indices=None):
    """rees_circuit_general.merge_bitlevel (same inputs, flags and perm), run on
    the circuit of the current Builder (call inside arith_backend()), plus the
    flag ancilla_clean: every qubit of the 'arith' register is 0 on every input."""
    qc, B, R = G.merge_circuit(cfg, d, s)
    pos = {q: i for i, q in enumerate(qc.qubits)}
    Gq, Gx = cfg.laws[d-1], cfg.laws[d]
    nQ, nX = cfg.p**cfg.width[d-1], Gx.order
    qi = np.arange(nQ) if q_indices is None else np.asarray(q_indices)
    xi = np.arange(nX) if x_indices is None else np.asarray(x_indices)
    QQ, XX = np.meshgrid(qi, xi, indexing="ij")
    qv = Gq.decode(QQ.ravel())
    xv = Gx.decode(XX.ravel())
    del QQ, XX
    sim = G.BitSim(qc.num_qubits, len(qv))
    sim.load(G.wires_of(R["Q"], pos), qv)
    sim.load(G.wires_of(R["x"], pos), xv)
    sim.run(G.compile_ops(qc.data, pos))
    x_out = sim.read(G.wires_of(R["x"], pos))
    scratch = [R["W"]]+[list(bw.values()) for bw in R["bws"].values()]
    flags = {"q_unchanged": bool((sim.read(G.wires_of(R["Q"], pos)) == qv).all()),
             "scratch_clean": all((sim.read(G.wires_of(qs, pos)) == 0).all() for qs in scratch),
             "x_canonical": bool((x_out < cfg.p).all()),
             "q_never_targeted": not any(pos[qb] in sim.targets for q in R["Q"] for qb in q),
             "inputs": int(len(qv))}
    anc = getattr(B, "anc_reg", None)
    flags["ancilla_clean"] = all(not sim.cols[pos[q]].any() for q in anc) if anc else True
    del sim
    g = -qv*np.array(cfg.scales(d-1, s))[None, :]
    g = np.concatenate([g, np.zeros((len(g), cfg.width[d]-cfg.width[d-1]), dtype=np.int64)], axis=1) % cfg.p
    ref = Gx.mul(xv, g)
    flags["equals_bch"] = bool((x_out == ref).all())
    perm = Gx.encode(np.where(x_out < cfg.p, x_out, 0)).reshape(len(qi), len(xi))
    return perm, flags


def bitlevel_compare(job="n4_f5", rows3=64, log=print):
    """Larger bit-level runs, old vs new perm: n4(F_5) grade 2 on ALL q and all x,
    grade 3 on rows3 evenly spaced q rows (as the circuit-2 report) and all x."""
    from theorems.rees_end_to_end_sim import filiform4
    cfg = G.Config(filiform4(5))
    out = {}
    t0 = time.time()
    for d in (2, 3):
        nQ = cfg.p**cfg.width[d-1]
        rows = None if d == 2 else np.unique(np.linspace(0, nQ-1, rows3).astype(np.int64))
        for s in range(1, cfg.p):
            perm_old, f_old = G.merge_bitlevel(cfg, d, s, q_indices=rows)
            with arith_backend():
                perm_new, f_new = merge_bitlevel_arith(cfg, d, s, q_indices=rows)
            out[f"d{d}_s{s}"] = {"q_rows": "all" if rows is None else len(rows), "new": f_new,
                                 "old_ok": all(v for k, v in f_old.items() if k != "inputs"),
                                 "perm_equal_old": bool(np.array_equal(perm_old, perm_new))}
            del perm_old, perm_new
            log(d, s, out[f"d{d}_s{s}"], round(time.time()-t0, 1), "s")
    out["all_ok"] = all(v["old_ok"] and v["perm_equal_old"] and all(x for k, x in v["new"].items() if k != "inputs")
                        for v in out.values() if isinstance(v, dict))
    out["seconds"] = round(time.time()-t0, 1)
    return out


# ====================================================================== backend comparison

def _sstate_equal(a, b):
    return a.d == b.d and a.scale == b.scale and np.array_equal(a.idx, b.idx) and np.array_equal(a.V, b.V)


def compare_backends(job, *, seeds=(20261103, 20261104), log=print, chunk=None, bit_rows=None):
    """Old vs new backend in sparse mode, state by state: instrument kernels,
    every merge proof (new), merge bit-level permutations (old vs new), then per
    subgroup the source state and flags, every label law and branch, the full
    check_instance_sparse row and seeded run_algorithm_sparse results."""
    import theorems.rees_circuit_sparse as S
    from theorems.rees_end_to_end_sim import filiform4, heisenberg
    t0 = time.time()
    if job == "heis_f3":
        cfg, insts, kw = G.Config(heisenberg(3)), G.heis3_instances(), {}
    elif job == "n4_f5":
        cfg, insts, kw = G.Config(filiform4(5)), G.n4_instances(5), dict(max_cases=4000, sample_tuples=6)
    else:
        raise ValueError(job)
    ck = {} if chunk is None else {"chunk": chunk}
    rec = {"job": job, "config": cfg.name(), "merges": {}, "instances": []}
    eng_old = S.SparseEngine(cfg, **ck)
    with arith_backend():
        eng_new = S.SparseEngine(cfg, **ck)
    rec["instrument_exponents_equal"] = all(
        all(np.array_equal(x, y) for x, y in zip(eng_old.kernels[d][0], eng_new.kernels[d][0]))
        for d in eng_old.kernels)
    rec["instrument_info_new"] = {d: eng_new.kernels[d][1] for d in eng_new.kernels}
    log(job, "instrument exponents equal", rec["instrument_exponents_equal"], round(time.time()-t0, 1), "s")
    rs = np.random.default_rng(0)
    for d in range(2, cfg.c+1):
        nQ = cfg.p**cfg.width[d-1]
        for s in range(1, cfg.p):
            with arith_backend():
                proof = G.prove_merge(cfg, d, s)
                qc, B, _ = G.merge_circuit(cfg, d, s)
                counts = arith_gate_counts(B)
                nq = qc.num_qubits
            qc_old, _, _ = G.merge_circuit(cfg, d, s)
            if bit_rows is None and nQ*cfg.laws[d].order <= 1 << 20:
                rows = None
            else:
                rows = np.unique(rs.integers(nQ, size=bit_rows or 4))
            perm_old, f_old = G.merge_bitlevel(cfg, d, s, q_indices=rows)
            with arith_backend():
                perm_new, f_new = merge_bitlevel_arith(cfg, d, s, q_indices=rows)
            rec["merges"][f"d{d}_s{s}"] = {
                "proof_new": proof, "bitlevel_new": f_new, "bitlevel_old_ok": all(v for k, v in f_old.items()
                                                                                 if k != "inputs"),
                "bitlevel_perm_equal_old": bool(np.array_equal(perm_old, perm_new)),
                "q_rows": "all" if rows is None else [int(r) for r in rows],
                "gates_new": counts, "qubits_new": nq, "gates_old": len(qc_old.data), "qubits_old": qc_old.num_qubits}
            log(job, f"merge d{d} s{s}", proof["proved"], f_new, rec["merges"][f"d{d}_s{s}"]["bitlevel_perm_equal_old"],
                round(time.time()-t0, 1), "s")
    for inst in insts:
        r = {"instance": inst.name}
        so = eng_old.source(inst)
        with arith_backend():
            sn = eng_new.source(inst)
        r["source_state_equal"] = _sstate_equal(so[0], sn[0])
        r["source_S_equal"] = bool(np.array_equal(so[1], sn[1]))
        r["source_info_equal"] = so[2] == sn[2]
        r["source_info_new"] = sn[2]
        # top-grade label law and every conditioned branch, from the two source states
        po, bo = eng_old.label_law(so[0])
        pn, bn = eng_new.label_law(sn[0])
        r["label_laws_equal"] = po == pn and list(po) == list(pn)
        r["branches_equal"] = set(bo) == set(bn) and all(_sstate_equal(bo[k], bn[k]) for k in bo)
        row_o = S.check_instance_sparse(cfg, inst, eng_old, source=so, **kw)
        with arith_backend():
            row_n = S.check_instance_sparse(cfg, inst, eng_new, source=sn, **kw)
        r["check_rows_identical"] = S.comparable_row(row_o) == S.comparable_row(row_n)
        r["check_passed_new"] = row_n["passed"]
        r["cases_new"] = {d: g["cases"] for d, g in row_n["grades"].items()}
        runs = []
        for sd in seeds:
            got_o = S.run_algorithm_sparse(cfg, inst, eng_old, seed=sd, top=so[0])
            with arith_backend():
                got_n = S.run_algorithm_sparse(cfg, inst, eng_new, seed=sd, top=sn[0])
            runs.append({"seed": sd, "identical": got_o == got_n, "recovered_new": got_n[1]["recovered"],
                         "oracle_queries": got_n[1]["oracle_queries"]})
        r["seeded_runs"] = runs
        r["all_equal"] = bool(r["source_state_equal"] and r["source_S_equal"] and r["source_info_equal"]
                              and r["label_laws_equal"] and r["branches_equal"] and r["check_rows_identical"]
                              and r["check_passed_new"] and all(x["identical"] and x["recovered_new"] for x in runs))
        rec["instances"].append(r)
        log(job, inst.name, "all_equal", r["all_equal"], r["cases_new"], round(time.time()-t0, 1), "s")
    rec["all_merges_proved_new"] = all(v["proof_new"]["proved"] for v in rec["merges"].values())
    rec["all_bitlevel_new_ok"] = all(all(x for k, x in v["bitlevel_new"].items() if k != "inputs")
                                     for v in rec["merges"].values())
    rec["all_bitlevel_perm_equal_old"] = all(v["bitlevel_perm_equal_old"] for v in rec["merges"].values())
    rec["all_instances_equal"] = all(r["all_equal"] for r in rec["instances"])
    rec["all_runs_recover_new"] = all(x["recovered_new"] for r in rec["instances"] for x in r["seeded_runs"])
    rec["seconds"] = round(time.time()-t0, 1)
    return rec


# ====================================================================== gate counts at large p

class LightEncoding:
    """Encoding without the O(p) value-test table (not needed by ArithBuilder)."""

    def __init__(self, p):
        self.p, self.nb = p, max(1, (p-1).bit_length())
        self.tests = None


def count_config(alg):
    saved = G.Encoding
    G.Encoding = LightEncoding
    try:
        return G.Config(alg)
    finally:
        G.Encoding = saved


def multiplication_counts(p, coeffs=None, seed=0):
    """Gate counts of one add_product and one add_scaled macro (counting mode),
    for coeff = 1, p-1 and a few random coefficients (the counts depend on the
    coefficient only through the X/CX loads)."""
    enc = LightEncoding(p)
    rng = random.Random(seed)
    coeffs = coeffs or sorted({1, p-1, *(rng.randrange(1, p) for _ in range(3))})
    out = {}
    for kind in ("add_scaled", "add_product"):
        rows = []
        for c in coeffs:
            k = 2 if kind == "add_scaled" else 3
            regs, qds = [], []
            for name in "tab"[:k]:
                r, q = G.qudit_register(name, 1, enc)
                regs.append(r)
                qds.append(q[0])
            qc = QuantumCircuit(*regs)
            B = CountingArithBuilder(qc, enc)
            getattr(B, kind)(*qds, c)
            rows.append({"coeff": c, **arith_gate_counts(B)})
        tot = [r["arith_total"] for r in rows]
        out[kind] = {"min_total": min(tot), "max_total": max(tot), "ccx": rows[0]["ccx"],
                     "rows": rows, "qubits_ancilla": anc_size(enc.nb)}
    return out


def formula_counts(p, coeff):
    """Closed-form gate counts of the two macros, from the block structure
    (b = ceil(log2 p), w = hw(p), H = sum_(i<b) hw(coeff 2^i mod p) <= b^2):
      adder 6b+1 gates (2b CCX), subtraction 8b+3, modular add 34b+12+4w,
      comparison 14b+5+2w, doubling 15b+7+4w (b of them SWAPs);
      add_scaled : 34b^2 + 40b + 10 + 4(b+1)w + 2H gates, 10b^2 + 8b + 2H CCX;
      add_product: 134b^2 + 50b - 4 + (20b-4)w + 4H gates, 40b^2 + 2b CCX.
    Hence at most 40b^2+44b+10 and 158b^2+46b-4 gates (w <= b, H <= b^2)."""
    b = max(1, (p-1).bit_length())
    w = bin(p).count("1")
    H = sum(bin(coeff % p*pow(2, i, p) % p).count("1") for i in range(b))
    return {"add_scaled_total": 34*b*b+40*b+10+4*(b+1)*w+2*H, "add_scaled_ccx": 10*b*b+8*b+2*H,
            "add_product_total": 134*b*b+50*b-4+(20*b-4)*w+4*H, "add_product_ccx": 40*b*b+2*b,
            "add_scaled_bound": 40*b*b+44*b+10, "add_product_bound": 158*b*b+46*b-4}


def merge_counts(alg, ds=None, s=1):
    cfg = count_config(alg)
    out = {}
    for d in (ds or range(2, cfg.c+1)):
        with arith_backend(CountingArithBuilder):
            qc, B, _ = G.merge_circuit(cfg, d, s)
        out[d] = {**arith_gate_counts(B), "macros": G.macro_counts(B), "qubits": qc.num_qubits,
                  "qubits_without_ancilla": qc.num_qubits-anc_size(cfg.enc.nb)}
    return out


def old_add_product_gates(p):
    """Gates of the original add_product macro: (p-1) A_p (increment_gate_cost)."""
    return (p-1)*G.increment_gate_cost(p)


def sampled_macro_check(p, n=2048, n_coeffs=3, seed=0):
    """[sampled] For large p: the emitted add_scaled / add_product gate lists run
    bit-level on n random canonical inputs, all edge inputs from {0, 1, 2, p-1}
    and n/4 inputs with padding t (t >= p, when 2^b > p), for coefficients 1,
    p-1 and n_coeffs random ones. Expected values in Python integers."""
    enc = LightEncoding(p)
    nb = enc.nb
    rng = random.Random(seed)
    coeffs = sorted({1, p-1, *(rng.randrange(1, p) for _ in range(n_coeffs))})
    rows = []
    for kind in ("add_scaled", "add_product"):
        k = 2 if kind == "add_scaled" else 3
        edge = [list(v) for v in product(sorted({0, 1, 2 % p, p-1}), repeat=k)]
        rand = [[rng.randrange(p) for _ in range(k)] for _ in range(n)]
        pad = [[rng.randrange(p, 1 << nb)]+[rng.randrange(1 << nb) for _ in range(k-1)]
               for _ in range(n//4)] if (1 << nb) > p else []
        opnd_pad = [[rng.randrange(p)]+[rng.randrange(1 << nb) for _ in range(k-1)] for _ in range(n//4)]
        vals = edge+rand+pad+opnd_pad
        V = np.array(vals, dtype=np.int64)
        for c in coeffs:
            regs, qds = [], []
            for name in "tab"[:k]:
                r, q = G.qudit_register(name, 1, enc)
                regs.append(r)
                qds.append(q[0])
            qc = QuantumCircuit(*regs)
            B = ArithBuilder(qc, enc)
            getattr(B, kind)(*qds, c)
            out, anc, _ = _sim_slice(qc, B, 0, len(qc.data), qds, V)
            want = []
            for v in vals:
                if v[0] >= p:
                    want.append(list(v))                      # (A2)
                else:
                    pr = v[1] if k == 2 else v[1]*v[2]
                    want.append([(v[0]+c*pr) % p]+list(v[1:]))   # (A1), (A3)
            ok = all(int(o) == w for row_o, row_w in zip(out.tolist(), want) for o, w in zip(row_o, row_w))
            rows.append({"p": p, "kind": kind, "coeff": c, "inputs": len(vals), "padding_t_inputs": len(pad),
                         "padding_operand_inputs": len(opnd_pad), "map_ok": bool(ok),
                         "ancilla_clean": not anc.any(), "gates": len(qc.data)})
    return rows


def sampled_merge_check(alg, d, s, rows=3, xs=1024, seed=0):
    """[sampled] merge_bitlevel_arith at large p on `rows` random q values and
    `xs` random x values (group indices are int64, so p^width(G_d) < 2^62 is required)."""
    cfg = count_config(alg)                         # no O(p) value-test table
    rs = np.random.default_rng(seed)
    nQ, nX = cfg.p**cfg.width[d-1], cfg.laws[d].order
    if nX >= 1 << 62:
        raise ValueError("indices do not fit int64")
    qi = np.unique(rs.integers(nQ, size=rows))
    xi = np.unique(rs.integers(nX, size=xs))
    with arith_backend():
        _, flags = merge_bitlevel_arith(cfg, d, s, q_indices=qi, x_indices=xi)
    return {"algebra": alg.name, "d": d, "s": s, **flags}


def scaling_table(primes, algs=None):
    from theorems.rees_end_to_end_sim import filiform4, filiform5, heisenberg
    algs = algs or (heisenberg, filiform4, filiform5)
    rows = []
    for p in primes:
        t0 = time.time()
        nb = max(1, (p-1).bit_length())
        mc = multiplication_counts(p)
        row = {"p": p, "bits": nb, "add_product_total": mc["add_product"]["max_total"],
               "add_product_total_min": mc["add_product"]["min_total"],
               "add_product_ccx": mc["add_product"]["ccx"], "add_scaled_total": mc["add_scaled"]["max_total"],
               "add_scaled_ccx": mc["add_scaled"]["ccx"], "ancilla_qubits": anc_size(nb), "merges": {},
               "mult_rows": {k: mc[k]["rows"] for k in ("add_scaled", "add_product")}}
        for f in algs:
            alg = f(p)
            if len(alg.lower_central_series()) >= p:
                continue                                  # Lazard needs class < p
            mc_ = merge_counts(alg)
            row["merges"][alg.name] = {d: {"total": v["arith_total"], "ccx": v.get("ccx", 0),
                                           "macros": v["macros"], "qubits": v["qubits"]} for d, v in mc_.items()}
        if p <= 1031:
            row["old_add_product_gates"] = old_add_product_gates(p)
            row["old_add_scaled_gates"] = G.increment_gate_cost(p)
        row["seconds"] = round(time.time()-t0, 2)
        rows.append(row)
    return rows


def fit_loglog(xs, ys):
    """Least-squares slope of log y against log x."""
    lx, ly = np.log(np.asarray(xs, float)), np.log(np.asarray(ys, float))
    A = np.vstack([lx, np.ones_like(lx)]).T
    (k, c), *_ = np.linalg.lstsq(A, ly, rcond=None)
    return float(k), float(math.exp(c))


def fit_quadratic(xs, ys):
    """Exact-ish fit y = a b^2 + b1 b + c0 by least squares (b = bits)."""
    x = np.asarray(xs, float)
    A = np.vstack([x**2, x, np.ones_like(x)]).T
    coef, res, *_ = np.linalg.lstsq(A, np.asarray(ys, float), rcond=None)
    return [float(v) for v in coef]


# ====================================================================== CLI

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--job", choices=["exhaustive", "agree", "counts", "sampled", "bitlevel"], required=True)
    ap.add_argument("--jobs", default="heis_f3,n4_f5")
    ap.add_argument("--primes", default="3,5,7,11,13")
    ap.add_argument("--out")
    args = ap.parse_args()
    lg = lambda *a: print(*a, flush=True)
    t0 = time.time()
    if args.job == "exhaustive":
        res = {**ARITH_STATUS, "primitives": {}, "macros": []}
        for p in map(int, args.primes.split(",")):
            res["primitives"][p] = primitive_checks(p)
            rows = exhaustive_macro_check(p)
            res["macros"] += rows
            lg(p, "primitives", res["primitives"][p]["ok"], "macros", all(r["ok"] for r in rows), len(rows),
               round(time.time()-t0, 1), "s")
        res["all_ok"] = all(v["ok"] for v in res["primitives"].values()) and all(r["ok"] for r in res["macros"])
    elif args.job == "agree":
        res = {**ARITH_STATUS, "runs": {}}
        for job in args.jobs.split(","):
            res["runs"][job] = compare_backends(job, log=lg)
            lg(job, {k: v for k, v in res["runs"][job].items() if k.startswith("all_")})
    elif args.job == "bitlevel":
        res = {**ARITH_STATUS, "n4_f5": bitlevel_compare(log=lg)}
    elif args.job == "sampled":
        from theorems.rees_end_to_end_sim import filiform4, heisenberg
        res = {**ARITH_STATUS, "macros": [], "merges": []}
        for p in map(int, args.primes.split(",")):
            res["macros"] += sampled_macro_check(p)
            lg(p, "macros", all(r["map_ok"] and r["ancilla_clean"] for r in res["macros"] if r["p"] == p),
               round(time.time()-t0, 1), "s")
        for alg_f, p, d, s in ((heisenberg, 101, 2, 1), (heisenberg, 101, 2, 37), (filiform4, 101, 2, 1),
                               (filiform4, 101, 3, 1), (filiform4, 101, 3, 58), (heisenberg, 1031, 2, 1),
                               (heisenberg, 1031, 2, 500), (filiform4, 1031, 2, 3)):
            res["merges"].append(sampled_merge_check(alg_f(p), d, s))
            lg(res["merges"][-1], round(time.time()-t0, 1), "s")
        res["all_macros_ok"] = all(r["map_ok"] and r["ancilla_clean"] for r in res["macros"])
        res["all_merges_ok"] = all(all(v for k, v in r.items() if k not in ("inputs", "algebra", "d", "s"))
                                   for r in res["merges"])
    else:
        primes = [int(x) for x in args.primes.split(",")]
        res = {**ARITH_STATUS, "rows": scaling_table(primes)}
        bits = [r["bits"] for r in res["rows"]]
        res["fit_add_product_loglog"] = fit_loglog(bits, [r["add_product_total"] for r in res["rows"]])
        res["fit_add_product_quadratic"] = fit_quadratic(bits, [r["add_product_total"] for r in res["rows"]])
        res["fit_add_product_ccx_quadratic"] = fit_quadratic(bits, [r["add_product_ccx"] for r in res["rows"]])
        res["fit_add_scaled_quadratic"] = fit_quadratic(bits, [r["add_scaled_total"] for r in res["rows"]])
        big = [r for r in res["rows"] if r["p"] >= 101]
        bb = [r["bits"] for r in big]
        res["fit_p_ge_101_loglog"] = {
            "add_product": fit_loglog(bb, [r["add_product_total"] for r in big]),
            "add_product_ccx": fit_loglog(bb, [r["add_product_ccx"] for r in big]),
            "add_scaled": fit_loglog(bb, [r["add_scaled_total"] for r in big]),
            **{f"merge {a.split('(')[0]} d{d}": fit_loglog(bb, [[v for k, v in r["merges"].items()
                                                                 if k.startswith(a)][0][d]["total"] for r in big])
               for a, d in (("Heis", 2), ("n4", 3), ("n5", 4))}}
        res["formula_matches"] = all(
            (x["arith_total"], x["ccx"]) == (formula_counts(r["p"], x["coeff"])[k+"_total"],
                                             formula_counts(r["p"], x["coeff"])[k+"_ccx"])
            for r in res["rows"] for k in ("add_scaled", "add_product") for x in r["mult_rows"][k])
    res["seconds"] = round(time.time()-t0, 1)
    text = json.dumps(res, indent=1, default=str)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text+"\n")
    lg(text[:3000])


if __name__ == "__main__":
    main()
