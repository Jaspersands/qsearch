"""Gate-level Qiskit circuit for the whole Rees algorithm on Heis(F_3).

Instance. L = Heis(F_3) with [x, y] = z, class c = 2, evaluation points 1, 2.
The positive Rees cover A = t L + t^2 [L, L] has dimension 4 (cover
coordinates a1, a2, a3 of grade one and a4 = t^2 z of grade two), so the top
group G_2 = (A, *) has order 81, the quotient G_1 = F_3^3 is abelian, and the
merge arity is the Chevalley-Warning arity kappa_2 g_2 + 1 = 3. Every one of
the 19 subgroups of Heis(F_3) is tested, including the 12 non-normal lines.

Encoding (why qubit pairs and not a qudit simulator). Qiskit circuits are
qubit-only, and a real compilation would also use binary registers, so each
F_3 coordinate is a qubit pair with value v = b0 + 2 b1; the pattern 11 is
padding. Arithmetic is built from X, CX and multi-controlled X gates (so it is
an exact permutation of basis states), and QFT_3 is one exact two-qubit
unitary F_3 + [1] (padding fixed). Oracle labels are 5-bit binary registers
written by XOR, as in the input contract U_f|g, y> = |g, y xor f(g)>.
Simulation keeps track of padding: every module is checked to leave zero
amplitude on padding words.

Circuit, per terminal sample (Sections 2-5 of main.tex):

1. Source (x3): QFT_3 on the 4 address qutrits; for s = 1, 2: compute
   E_s(a) into a 3-qutrit workspace, call U_f into the label register s,
   uncompute E_s. Labels are discarded.
2. Complete central instrument (x3): ancilla QFT_3, controlled central
   subtraction a4 -= z (R_z|x> = |x z^-1>), inverse QFT_3, measure lambda.
3. Classical SDE solve s_1^2 l_1 + s_2^2 l_2 + s_3^2 l_3 = 0 (brute force,
   imported from rees_end_to_end_sim). The merge circuit is then emitted for
   that classical witness (classical feed-forward).
4. Merge: Q register (G_1 address) in uniform superposition by QFT_3; on
   each active target the controlled right translation
   x -> x * (-delta_s(sigma(q))) with the four-pass Bennett schedule of
   thm:uniform-compilation(ii): out-of-place BCH by compute (bracket into a
   workspace) - copy - uncompute, swap, then erase the old x by recomputing
   it the same way. Targets are discarded.
5. Readout: QFT_3 on each Q qutrit and measure; the F_3-nullspace of the
   samples is returned as log H.

Simulation method. The assembled circuit for one terminal sample has 82
qubits (45 with register reuse), far beyond statevector or density-matrix
simulation. It is simulated exactly, module by module, with the modules'
actual gate lists:
* source: 4 QFT_3 on |0> followed by permutation gates only (E_s passes and
  the table oracle), so the state is (1/9) sum_a |pi(a, 0)> with pi evaluated
  bit by bit on all 81 addresses; this gives the reduced address density and
  P(workspace = |0>) exactly. An Aer statevector run (24 qubits) of the same
  circuit cross-checks it;
* instrument and readout: the qiskit.quantum_info Operator of the circuit;
* merge: it contains only X/CX/MCX/SWAP gates, so it is a permutation of
  basis states and is evaluated exactly on every canonical input (27 x 81),
  which checks clean scratch on ALL inputs and compares with the BCH product;
  an Aer statevector run cross-checks it on given target states.
Modules are composed with two exact identities, both checked on the gate list:
independent sources are tensor factors (disjoint registers), and the merge is
controlled-diagonal in Q (no gate targets a Q qubit), so the channel on Q is
the Schur multiplier T_i[q, r] = tr(U_q rho_i U_r^dagger) and several
targets compose by entrywise products.

What this does NOT show. It is one fixed instance at p = 3: no asymptotic
cost, no Schedule 1 arity B_2 = 64 (the arity is 3), no Ivanyos-Santha
solver, no finite-gate QFT approximation (QFT_3 is exact), no noise, and the
oracle is a table-built gate whose own cost is not counted. Padding words are
not mapped to themselves by the arithmetic (only canonical inputs are
guaranteed and checked), unlike the identity-on-invalid convention of
research/REES_UNIFORM_INSTRUMENT_COMPILATION.md. It does not implement or
certify a coherent receiver; coherent_receiver_implemented stays false.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json
import random
import time

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit import ControlledGate
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

from theorems.rees_end_to_end_sim import (
    DenseBackend, HiddenInstance, brute_force_sde, expected_label_support,
    expected_stage_indices, heisenberg, make_cover, nullspace, rref,
)

P = 3
OMEGA = np.exp(2j*np.pi/P)
LABEL_BITS = 5                      # f takes values 0..26 (coset minima)
TOL = 1e-9
STATUS = {"status": "gate_level_small_instance_circuit_not_a_coherent_receiver",
          "coherent_receiver_implemented": False}


# ---------------------------------------------------------------- qutrit registers

def qutrit_register(name, n):
    """QuantumRegister of 2n qubits and its qutrits, most significant first.

    Qutrit j uses qubits (2(n-1-j), 2(n-1-j)+1), so listing the register's
    qubits in order gives qubit index sum_j v_j 4^(n-1-j) for values v_j."""
    reg = QuantumRegister(2*n, name)
    return reg, [(reg[2*(n-1-j)], reg[2*(n-1-j)+1]) for j in range(n)]


@lru_cache(maxsize=None)
def canonical_index(n):
    """For each base-3 big-endian index of n qutrits, the base-4 qubit index."""
    digits = np.array(list(product(range(P), repeat=n)), dtype=np.int64).reshape(-1, n)
    return digits @ (4**np.arange(n-1, -1, -1, dtype=np.int64))


def _qft3_matrix(inverse=False):
    F = np.eye(4, dtype=complex)
    F[:3, :3] = OMEGA**np.outer(np.arange(3), np.arange(3))/np.sqrt(3)
    return F.conj().T if inverse else F


def _named_gate(matrix, name):
    sub = QuantumCircuit(2, name=name)
    sub.append(UnitaryGate(matrix), [0, 1])
    return sub.to_gate()


QFT3 = _named_gate(_qft3_matrix(), "qft3")
QFT3_DG = _named_gate(_qft3_matrix(inverse=True), "qft3_dg")


class Builder:
    """Emits mod-3 arithmetic as X/CX/MCX gates and counts the paper's primitives.

    A control (qutrit, v) with v in {1, 2} tests the single bit b0 (v = 1) or
    b1 (v = 2); this is exact on canonical words, which is all the circuit is
    promised (and checked) on."""

    def __init__(self, qc):
        self.qc = qc
        self.counts = Counter()

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

    def increment(self, t, k, controls=()):
        """t += k (mod 3) when every control holds; exact on all four words of t."""
        k %= P
        if not k:
            return
        bits = [(q[v-1], 1) for q, v in controls]
        b0, b1 = t

        def swap12():           # transposition 01 <-> 10 (controlled SWAP)
            self.qc.cx(b1, b0)
            self._x(b1, bits+[(b0, 1)])
            self.qc.cx(b1, b0)

        def swap01():           # transposition 00 <-> 01
            self._x(b0, bits+[(b1, 0)])
        if k == 1:
            swap12(); swap01()
        else:
            swap01(); swap12()

    def add_scaled(self, t, a, coeff, controls=()):
        """t += coeff * a."""
        for v in (1, 2):
            self.increment(t, coeff*v, list(controls)+[(a, v)])

    def add_product(self, t, a, b, coeff):
        """t += coeff * a * b."""
        for va, vb in product((1, 2), repeat=2):
            self.increment(t, coeff*va*vb, [(a, va), (b, vb)])

    def qft(self, q, role, inverse=False):
        self.qc.append(QFT3_DG if inverse else QFT3, list(q))
        self.counts[role] += 1

    def swap(self, a, b):
        for x, y in zip(a, b):
            self.qc.swap(x, y)


# ---------------------------------------------------------------- the instance

@lru_cache(maxsize=None)
def cover():
    return make_cover(heisenberg(P))


def all_subalgebras():
    """All 19 Lie subalgebras of Heis(F_3) as RREF bases (L coordinates)."""
    alg = heisenberg(P)
    vecs = [v for v in product(range(P), repeat=3) if any(v)]
    seen = {(): None}
    for k in (1, 2, 3):
        for gens in product(vecs, repeat=k):
            basis = tuple(rref(list(gens), P))
            if len(basis) == k and basis not in seen and alg.lie_closure(basis) == list(basis):
                seen[basis] = None
    return [list(b) for b in seen]


def hidden_instances():
    alg = heisenberg(P)
    out = []
    for basis in all_subalgebras():
        tag = "normal" if alg.is_ideal(basis) else "non-normal"
        out.append(HiddenInstance(f"Heis(F_3) H=<{basis}> {tag}", alg, tuple(tuple(v) for v in basis)))
    return out


def oracle_gate(inst):
    """U_f |w>|y> = |w>|y xor f(w)> on 3 qutrits + 5 bits, built from the table.
    Padding words of w are left alone. Its gates are the oracle's, not counted."""
    w_reg, w = qutrit_register("w", 3)
    y = QuantumRegister(LABEL_BITS, "y")
    qc = QuantumCircuit(w_reg, y, name="U_f")
    for idx, digits in enumerate(product(range(P), repeat=3)):
        value = int(inst.oracle_table[idx])
        if not value:
            continue
        controls = [qb for q in w for qb in q]
        state = sum(((d >> 0) & 1) << (2*j) | ((d >> 1) & 1) << (2*j+1) for j, d in enumerate(digits))
        for bit in range(LABEL_BITS):
            if value >> bit & 1:
                qc.mcx(controls, y[bit], ctrl_state=state)
    return qc.to_gate()


# ---------------------------------------------------------------- modules

def evaluation_pass(B, a, w, s, inverse=False):
    """w += E_s(a) (or -=): E_s(a1..a4) = (s a1, s a2, s a3 + s^2 a4)."""
    sign = -1 if inverse else 1
    for coord, j in ((0, 0), (1, 1), (2, 2)):
        B.add_scaled(w[coord], a[j], sign*s)
    B.add_scaled(w[2], a[3], sign*s*s)
    B.counts["E_s_uncompute" if inverse else "E_s_compute"] += 1


def source_circuit(inst, points=(1, 2), uncompute=True):
    """One lifted source: uniform address, c evaluations, c oracle calls."""
    a_reg, a = qutrit_register("a", 4)
    w_reg, w = qutrit_register("w", 3)
    labels = [QuantumRegister(LABEL_BITS, f"y{s}") for s in points]
    qc = QuantumCircuit(a_reg, w_reg, *labels, name="source")
    B = Builder(qc)
    for q in a:
        B.qft(q, "qft_leaf")
    U = oracle_gate(inst) if inst is not None else None
    for s, y in zip(points, labels):
        evaluation_pass(B, a, w, s)
        if U is not None:
            qc.append(U, list(w_reg)+list(y))
        B.counts["oracle_calls"] += 1
        if uncompute:
            evaluation_pass(B, a, w, s, inverse=True)
    return qc, B.counts, (a_reg, w_reg)


def instrument_circuit():
    """Complete central instrument on the top grade a4 (g_2 = 1), unmeasured."""
    a_reg, a = qutrit_register("a", 4)
    z_reg, z = qutrit_register("z", 1)
    qc = QuantumCircuit(a_reg, z_reg, name="instrument")
    B = Builder(qc)
    B.qft(z[0], "qft_grade2")
    B.add_scaled(a[3], z[0], -1)            # R_z |x> = |x - z> on the central coordinate
    B.counts["central_subtractions"] += 1
    B.qft(z[0], "qft_grade2", inverse=True)
    return qc, B.counts


def merge_ops(B, Q, x, W, b, s, bennett=True):
    """In place x -> x * g with g = -delta_s(sigma(q)) = (-s q1, -s q2, -s q3, 0).

    Four BCH passes (thm:uniform-compilation(ii)); class-two BCH is
    u * v = u + v + 2 [u, v] over F_3 with [u, v]_4 = u1 v2 - u2 v1, and each
    pass evaluates that one bracket into the workspace b."""
    def bracket(u, coeff):      # b += coeff * [u, g]_4 with g = -s sigma(q)
        B.add_product(b, u[0], Q[1], -s*coeff)
        B.add_product(b, u[1], Q[0], s*coeff)
        B.counts["bracket_evaluations"] += 1
        B.counts["bch_passes"] += 1

    def bch_linear(u, sign_g, sign):  # W += sign * (u + sign_g g + 2 b)
        for j in range(4):
            B.add_scaled(W[j], u[j], sign)
        for j in range(3):
            B.add_scaled(W[j], Q[j], sign*sign_g*(-s))
        B.add_scaled(W[3], b, 2*sign)

    # out of place W = x * g: compute bracket, copy, uncompute (two passes)
    bracket(x, 1)
    bch_linear(x, 1, 1)
    if bennett:
        bracket(x, -1)
    B.swap(x, W)                    # x = x * g, W = old x = x_new * g^-1
    # erase W by recomputing x_new * (-g) the same way (two passes)
    bracket(x, -1)                  # [x_new, -g] = -[x_new, g]
    bch_linear(x, -1, -1)
    bracket(x, 1)
    B.counts["controlled_right_actions"] += 1


def merge_circuit(s, bennett=True):
    Q_reg, Q = qutrit_register("q", 3)
    x_reg, x = qutrit_register("x", 4)
    W_reg, W = qutrit_register("W", 4)
    b_reg, b = qutrit_register("b", 1)
    qc = QuantumCircuit(Q_reg, x_reg, W_reg, b_reg, name=f"merge_s{s}")
    B = Builder(qc)
    merge_ops(B, Q, x, W, b[0], s, bennett=bennett)
    return qc, B.counts, (Q_reg, x_reg, W_reg, b_reg)


def fourier_circuit(role):
    """QFT_3 on every qutrit of a G_1 register (Q preparation or readout)."""
    Q_reg, Q = qutrit_register("q", 3)
    qc = QuantumCircuit(Q_reg, name=role)
    B = Builder(qc)
    for q in Q:
        B.qft(q, role)
    return qc, B.counts


# ---------------------------------------------------------------- exact module simulation

def _aer():
    from qiskit_aer import AerSimulator
    return AerSimulator(method="statevector")


_SOURCE_CACHE = {}


def _source_parts(sv_or_amps, n_rest):
    """(address density on canonical words, P(workspace = 0), padding weight)
    from amplitudes indexed [rest, address] with rest = workspace + labels."""
    M = sv_or_amps.reshape(n_rest, 256)
    rho = M.T @ M.conj()
    work_zero = float(np.sum(np.abs(M.reshape(-1, 64, 256)[:, 0, :])**2))
    idx = canonical_index(4)
    sub = rho[np.ix_(idx, idx)]
    return sub, work_zero, float(abs(1-np.trace(sub).real))


def simulate_source(inst, points=(1, 2), uncompute=True, method="exact"):
    """Simulate the source circuit. Returns (address density 81x81 = partial
    trace over workspace and labels, P(workspace = 0), padding weight).

    method="exact": the circuit is 4 QFT_3 on |0> followed by permutation
    gates only (checked), so the final state is (1/9) sum_a |pi(a, 0)>, with
    pi evaluated bit by bit on all 81 canonical addresses.
    method="aer": Aer statevector run of the same circuit (24 qubits)."""
    key = (inst.name, tuple(points), uncompute, method)
    if key in _SOURCE_CACHE:
        return _SOURCE_CACHE[key]
    qc, _, (a_reg, w_reg) = source_circuit(inst, points, uncompute)
    if list(qc.qubits[:8]) != list(a_reg) or list(qc.qubits[8:14]) != list(w_reg):
        raise AssertionError("register layout changed")
    n_rest = 2**(qc.num_qubits-8)
    if method == "aer":
        sim = _aer()                # importing qiskit_aer adds the save_* methods
        qc = qc.copy()
        qc.save_statevector(label="sv")
        amps = np.asarray(sim.run(transpile(qc, sim, optimization_level=0)).result().data(0)["sv"])
        result = _source_parts(amps, n_rest)
    else:
        head, tail = qc.data[:4], qc.data[4:]
        if [i.operation.name for i in head] != ["qft3"]*4 or \
                {q for i in head for q in i.qubits} != set(a_reg):
            raise AssertionError("source must start with QFT_3 on each address qutrit")
        pos = {q: i for i, q in enumerate(qc.qubits)}
        bits = np.zeros((81, qc.num_qubits), dtype=bool)
        i4 = canonical_index(4)
        for k, q in enumerate(a_reg):
            bits[:, pos[q]] = (i4 >> k) & 1
        apply_permutation_gates(tail, bits, pos)
        out = bits.astype(np.int64) @ (1 << np.arange(qc.num_qubits, dtype=np.int64))
        addr, rest = out & 255, out >> 8               # amplitude 1/9 on each |rest, addr>
        if len(set(out.tolist())) != 81:
            raise ArithmeticError("source map is not injective on addresses")
        rho = np.zeros((256, 256), dtype=complex)
        np.add.at(rho, (addr[:, None], addr[None, :]), (rest[:, None] == rest[None, :])/81)
        idx = canonical_index(4)
        sub = rho[np.ix_(idx, idx)]
        result = (sub, float(np.mean((rest & 63) == 0)), float(abs(1-np.trace(sub).real)))
    _SOURCE_CACHE[key] = result
    return result


@lru_cache(maxsize=None)
def _instrument_operator():
    return Operator(instrument_circuit()[0]).data


def simulate_instrument(rho):
    """Exact complete instrument on an 81x81 source. Returns {lambda: (prob, state)}
    and the post-instrument weight on padding words (address or ancilla)."""
    U = _instrument_operator()
    idx = canonical_index(4)
    full = np.zeros((1024, 1024), dtype=complex)
    full[np.ix_(idx, idx)] = rho                           # ancilla |0> on bits 8, 9
    out = U @ full @ U.conj().T
    branches, kept = {}, 0.0
    for lam in range(P):
        j = idx+256*lam
        block = out[np.ix_(j, j)]
        pr = float(np.trace(block).real)
        kept += pr
        if pr > TOL:
            branches[lam] = (pr, block/pr)
    return branches, 1-kept


def apply_permutation_gates(instructions, bits, pos):
    """Apply X/CX/MCX/SWAP instructions (composite gates such as U_f are
    expanded through their definitions) to the bit table bits[input, qubit].
    Any other gate raises, so a pass certifies the gate list is a permutation
    of basis states. Returns the set of qubit positions ever targeted."""
    targets = set()
    for inst in instructions:
        op, wires = inst.operation, [pos[q] for q in inst.qubits]
        if op.name == "x":
            bits[:, wires[0]] ^= True
        elif op.name == "swap":
            bits[:, [wires[0], wires[1]]] = bits[:, [wires[1], wires[0]]]
        elif isinstance(op, ControlledGate) and op.base_gate.name == "x":
            fire = np.ones(len(bits), dtype=bool)
            for i in range(op.num_ctrl_qubits):
                fire &= bits[:, wires[i]] == bool(op.ctrl_state >> i & 1)
            bits[:, wires[-1]] ^= fire
            wires = wires[-1:]
        elif op.name == "U_f":
            inner = op.definition
            sub = {q: wires[i] for i, q in enumerate(inner.qubits)}
            targets |= apply_permutation_gates(inner.data, bits, sub)
            continue
        else:
            raise ValueError(f"not a permutation gate: {op.name}")
        targets.update(wires)
    return targets


def merge_permutation(s, bennett=True):
    """Exact bit-level evaluation of the merge gate list on all canonical
    (q, x) with zero scratch. Returns perm[q, x] (G_2 index) and flags."""
    qc, _, (Q_reg, x_reg, W_reg, b_reg) = merge_circuit(s, bennett)
    pos = {q: i for i, q in enumerate(qc.qubits)}
    qs, xs = np.meshgrid(np.arange(27), np.arange(81), indexing="ij")
    bits = np.zeros((27*81, qc.num_qubits), dtype=bool)
    i4q, i4x = canonical_index(3)[qs.ravel()], canonical_index(4)[xs.ravel()]
    for k, q in enumerate(Q_reg):
        bits[:, pos[q]] = (i4q >> k) & 1
    for k, q in enumerate(x_reg):
        bits[:, pos[q]] = (i4x >> k) & 1
    targets_q = apply_permutation_gates(qc.data, bits, pos)

    def read(reg):
        return sum(bits[:, pos[q]].astype(np.int64) << k for k, q in enumerate(reg))
    inv4 = {int(v): i for i, v in enumerate(canonical_index(4))}
    x_out = read(x_reg)
    q_targeted = any(pos[q] in targets_q for q in Q_reg)
    flags = {"q_never_targeted": not q_targeted,
             "q_unchanged": bool((read(Q_reg) == i4q).all()),
             "scratch_clean_all_inputs": bool((read(W_reg) == 0).all() and (read(b_reg) == 0).all()),
             "x_canonical": all(int(v) in inv4 for v in x_out)}
    perm = np.array([inv4.get(int(v), -1) for v in x_out]).reshape(27, 81)
    return perm, flags


def bch_reference(s):
    """perm[q, x] = x * (-delta_s(sigma(q))) from the BCH product of the cover."""
    cv = cover()
    G2, G1 = cv.stage_group(2), cv.stage_group(1)
    X = G2.elements()
    out = np.zeros((27, 81), dtype=np.int64)
    for qi, q in enumerate(G1.elements()):
        g = -np.concatenate([q, [0]])*cv.dilation_scales(2, s)
        out[qi] = G2.encode(G2.mul(X, g[None, :] % P))
    return out


@lru_cache(maxsize=None)
def merge_table(s):
    perm, flags = merge_permutation(s)
    if not all(flags.values()):
        raise ArithmeticError(f"merge circuit check failed: {flags}")
    return perm


def schur_factor(rho, s):
    """T[q, r] = tr(U_q rho U_r^dagger) = sum_x rho[x, U_r^-1 U_q x] for the
    compiled merge with scale s (rows/columns indexed by G_1)."""
    perm = merge_table(s)
    inv = np.argsort(perm, axis=1)                      # U_r^-1 as an index map
    T = np.empty((27, 27), dtype=complex)
    xs = np.arange(81)
    for q in range(27):
        y = inv[:, perm[q]]                             # (r, x) -> U_r^-1 U_q x
        T[q] = rho[xs[None, :], y].sum(axis=1)
    return T


def channel_output(states, witness):
    """Output on Q of the merge over all targets: |Q|^-1 prod_(s_i != 0) T_i."""
    sigma = np.full((27, 27), 1/27, dtype=complex)
    if not any(witness):
        raise ValueError("zero witness")
    for rho, s in zip(states, witness):
        if s:
            sigma = sigma*schur_factor(rho, s)
    return sigma


def merge_aer_check(rho_target_pure, s):
    """Aer statevector run of Q-preparation + merge on a pure canonical target;
    returns (Q density, P(scratch = 0))."""
    sim = _aer()
    qc, _, (Q_reg, x_reg, W_reg, b_reg) = merge_circuit(s)
    full = QuantumCircuit(*qc.qregs)
    if list(full.qubits[:6]) != list(Q_reg) or list(full.qubits[6:14]) != list(x_reg):
        raise AssertionError("register layout changed")
    vec = np.zeros(2**full.num_qubits, dtype=complex)      # Q = W = b = 0, x = psi
    vec[canonical_index(4) << 6] = rho_target_pure
    full.set_statevector(vec)               # Aer's initialize is pathologically slow here
    prep = fourier_circuit("qft_grade2")[0]
    full.compose(prep, qubits=list(Q_reg), inplace=True)
    full.compose(qc, inplace=True)
    full.save_statevector(label="sv")       # save_density_matrix is far slower in Aer
    if list(full.qubits[14:]) != list(W_reg)+list(b_reg):
        raise AssertionError("register layout changed")
    sv = np.asarray(sim.run(transpile(full, sim, optimization_level=0)).result().data(0)["sv"])
    M = sv.reshape(-1, 64)                  # rows: x (8 bits) then W, b (10 bits); cols: Q
    rho_q = M.T @ M.conj()
    scratch_zero = float(np.sum(np.abs(M.reshape(1024, 256, 64)[0])**2))
    idx = canonical_index(3)
    return rho_q[np.ix_(idx, idx)], scratch_zero


@lru_cache(maxsize=None)
def _readout_operator():
    return Operator(fourier_circuit("qft_final")[0]).data


def readout_distribution(sigma):
    idx = canonical_index(3)
    full = np.zeros((64, 64), dtype=complex)
    full[np.ix_(idx, idx)] = sigma
    U = _readout_operator()
    diag = np.real(np.diag(U @ full @ U.conj().T))
    if abs(diag.sum()-diag[idx].sum()) > TOL or diag.min() < -TOL:
        raise ArithmeticError("readout leaked to padding or is not a distribution")
    keys = list(product(range(P), repeat=3))
    return {k: float(diag[i]) for k, i in zip(keys, idx) if diag[i] > TOL}


# ---------------------------------------------------------------- references and checks

def coset_density(indices, order):
    """rho_H[q, r] = 1/|G_1| if r - q in H, for a subgroup H of the abelian G_1."""
    G1 = cover().stage_group(1)
    E = G1.elements()
    member = np.zeros(order, dtype=bool)
    member[indices] = True
    diff = G1.encode((E[None, :, :]-E[:, None, :]) % P)
    return member[diff]/order


def witnesses(labels):
    return [s for s in product(range(P), repeat=len(labels))
            if any(s) and sum(si*si*l for si, l in zip(s, labels)) % P == 0]


CHECK_KEYS = ("source_equals_rho_lift", "source_workspace_clean",
              "label_law_uniform_on_K_perp_and_states_match", "all_merge_outputs_equal_rho_H1",
              "all_readouts_uniform_on_h_perp", "nullspace_of_readout_support_equals_log_H")


def check_instance(inst, dense=None):
    """Exhaustive exact check of one hidden subgroup. Every positive-probability
    label triple and EVERY valid witness is pushed through the compiled merge."""
    cv = cover()
    dense = dense or DenseBackend(cv)
    rho, work_clean, leak = simulate_source(inst)
    (_, ref), _ = dense.prepare_source(inst.oracle)
    source_ok = np.abs(rho-ref).max() < TOL
    branches, inst_leak = simulate_instrument(rho)
    allowed = _span_scalars(expected_label_support(cv, inst.log_h, 2))
    law_ok = (sorted(branches) == allowed and
              all(abs(pr-1/len(allowed)) < TOL for pr, _ in branches.values()))
    dlaw = dense.label_probabilities((2, ref))
    for lam, (pr, st) in branches.items():
        dref = dense.condition((2, ref), (lam,), dlaw[(lam,)])[1]
        if np.abs(st-dref).max() > TOL:
            law_ok = False
    target = coset_density(expected_stage_indices(cv, inst.log_h, 1), 27)
    h_perp = set(_span(nullspace(inst.log_h, 3, P), 3))      # {0} when H = G
    cases = merges_ok = readout_ok = 0
    for labels in product(sorted(branches), repeat=3):
        states = [branches[l][1] for l in labels]
        for s in witnesses(labels):
            cases += 1
            sigma = channel_output(states, s)
            merges_ok += np.abs(sigma-target).max() < TOL
            dist = readout_distribution(sigma)
            readout_ok += (set(dist) == h_perp and
                           all(abs(v-1/len(h_perp)) < TOL for v in dist.values()))
    recovered = rref(nullspace(sorted(h_perp), 3, P), P)
    row = {"instance": inst.name, "normal": inst.flags()["normal"], "dim_h": len(inst.log_h),
           "source_equals_rho_lift": bool(source_ok), "source_workspace_clean": abs(work_clean-1) < TOL,
           "source_padding_weight": abs(leak), "instrument_padding_weight": abs(float(inst_leak)),
           "label_law_uniform_on_K_perp_and_states_match": bool(law_ok),
           "label_support": allowed, "branch_witness_cases": cases,
           "all_merge_outputs_equal_rho_H1": bool(merges_ok == cases),
           "all_readouts_uniform_on_h_perp": readout_ok == cases,
           "nullspace_of_readout_support_equals_log_H": recovered == rref(inst.log_h, P)}
    row["passed"] = all(row[k] for k in CHECK_KEYS) and max(abs(leak), abs(inst_leak)) < TOL
    return row


def _span(basis, width):
    if not basis:
        return [(0,)*width]
    return [tuple(sum(c*v[j] for c, v in zip(coef, basis)) % P for j in range(width))
            for coef in product(range(P), repeat=len(basis))]


def _span_scalars(K_perp):
    """Labels in F_3^1 allowed by K_d^perp (g_2 = 1)."""
    return sorted({v[0] for v in _span([tuple(r) for r in K_perp], 1)})


def run_algorithm(inst, seed=0, samples=7):
    """Seeded run from oracle access only: sample labels, solve the SDE
    classically, merge with the compiled circuit, sample the readout."""
    rng = random.Random(seed)
    rho, _, _ = simulate_source(inst)
    branches, _ = simulate_instrument(rho)
    keys = sorted(branches)
    out, queries = [], 0
    for _ in range(samples):
        labels = rng.choices(keys, weights=[branches[k][0] for k in keys], k=3)
        queries += 6
        s, _ = brute_force_sde([(l,) for l in labels], 2, P, rng)
        sigma = channel_output([branches[l][1] for l in labels], s)
        dist = readout_distribution(sigma)
        ks = list(dist)
        out.append(rng.choices(ks, weights=[dist[k] for k in ks], k=1)[0])
    return rref(nullspace(out, 3, P), P), queries


# ---------------------------------------------------------------- assembled circuit and resources

def terminal_sample_circuit(inst=None, witness=(1, 1, 1)):
    """The whole circuit for ONE terminal sample, for a fixed classical record
    (the witness is classical feed-forward). Oracle calls are opaque U_f gates
    when inst is given, else omitted (counted only). 82 qubits, no reuse."""
    regs, addr, labels = [], [], []
    for i in range(3):
        r, a = qutrit_register(f"a{i}", 4)
        regs.append(r); addr.append(a)
    for i in range(3):
        y = [QuantumRegister(LABEL_BITS, f"y{i}{s}") for s in (1, 2)]
        regs += y; labels.append(y)
    w_reg, w = qutrit_register("w", 3)
    anc = []
    for i in range(3):
        r, z = qutrit_register(f"z{i}", 1)
        regs.append(r); anc.append(z[0])
    Q_reg, Q = qutrit_register("q", 3)
    W_reg, W = qutrit_register("W", 4)
    b_reg, b = qutrit_register("b", 1)
    lam_bits, k_bits = ClassicalRegister(6, "lam"), ClassicalRegister(6, "k")
    qc = QuantumCircuit(*regs, w_reg, Q_reg, W_reg, b_reg, lam_bits, k_bits)
    B = Builder(qc)
    U = oracle_gate(inst) if inst is not None else None
    for i in range(3):
        for q in addr[i]:
            B.qft(q, "qft_leaf")
        for s, y in zip((1, 2), labels[i]):
            evaluation_pass(B, addr[i], w, s)
            if U is not None:
                qc.append(U, list(w_reg)+list(y))
            B.counts["oracle_calls"] += 1
            evaluation_pass(B, addr[i], w, s, inverse=True)
        B.qft(anc[i], "qft_grade2")
        B.add_scaled(addr[i][3], anc[i], -1)
        B.counts["central_subtractions"] += 1
        B.qft(anc[i], "qft_grade2", inverse=True)
        qc.measure(list(anc[i]), lam_bits[2*i:2*i+2])
    for q in Q:
        B.qft(q, "qft_grade2")
    for i, s in enumerate(witness):
        if s:
            merge_ops(B, Q, addr[i], W, b[0], s)
    for q in Q:
        B.qft(q, "qft_final")
    qc.measure(list(Q_reg), k_bits)
    return qc, B.counts


def paper_counts(samples=1, c=2, M=3, r2=1, D1=3, D2=4, n=3, bracket_per_bch=4):
    """research/REES_UNIFORM_INSTRUMENT_COMPILATION.md, 'Primitive Counts', with
    v_2 = m, L = m M_2, T = v_2; B(2) = (d-1)d(d+1)(d+2)/6 = 4 at d = 2."""
    m = samples
    L, v2 = m*M, m
    return {"oracle_calls": c*L, "E_s_compute": c*L, "E_s_uncompute": c*L,
            "qft_leaf": D2*L, "qft_grade2": v2*(2*M*r2+D1), "qft_final": m*n,
            "central_subtractions": v2*M*r2, "controlled_right_actions": v2*M,
            "bch_passes": 4*v2*M, "bracket_evaluations_upper_bound": 4*v2*M*bracket_per_bch}


def gate_profile(qc):
    """Logical gate counts (MCX by number of controls) and a {cx, u} transpile."""
    ops = Counter()
    for inst in qc.data:
        op = inst.operation
        if isinstance(op, ControlledGate) and op.base_gate.name == "x":
            ops[f"x_with_{op.num_ctrl_qubits}_controls"] += 1
        else:
            ops[op.name] += 1
    stripped = QuantumCircuit(*qc.qregs)
    for inst in qc.data:
        if inst.operation.name not in ("measure", "U_f", "barrier"):
            stripped.append(inst.operation, inst.qubits)
    t = transpile(stripped, basis_gates=["cx", "u"], optimization_level=1)
    if t.layout is not None and t.layout.final_layout is not None and \
            any(t.layout.final_layout[q] != i for i, q in enumerate(t.qubits)):
        raise AssertionError("transpile elided swaps; counts would omit them")
    return {"qubits": qc.num_qubits, "logical_ops": dict(sorted(ops.items())),
            "transpiled_cx_u_excluding_oracle": dict(t.count_ops()),
            "transpiled_depth_excluding_oracle": t.depth()}


def resource_report():
    modules = {"source_without_oracle": source_circuit(None)[0],
               "instrument": instrument_circuit()[0],
               "merge_s1": merge_circuit(1)[0], "merge_s2": merge_circuit(2)[0],
               "q_preparation": fourier_circuit("qft_grade2")[0],
               "readout": fourier_circuit("qft_final")[0]}
    profiles = {k: gate_profile(v) for k, v in modules.items()}
    qc, counts = terminal_sample_circuit(None, (1, 2, 1))
    total = gate_profile(qc)
    paper = paper_counts(1)
    compare = {k: {"circuit": counts.get(k.replace("_upper_bound", ""), 0), "note_formula": v}
               for k, v in paper.items()}
    return {"modules": profiles, "terminal_sample": {"profile": total, "primitive_counts": dict(counts),
                                                     "versus_compilation_note": compare},
            "run_with_7_samples_primitives": {k: 7*v for k, v in counts.items()},
            "minimal_width_with_reuse": {"qubits": 3*8+6+8+2+5, "note":
                                         "3 addresses, Q, W, b, one 5-bit label register; E_s work"
                                         " in W, instrument ancilla in b, labels measured and reset"},
            "group_registers_live": "3 targets + Q = 4 = 2 + (M_2 - 1), thm:uniform-compilation(iv)"}


def negative_controls():
    """Broken variants that must be caught by the checks above."""
    cv = cover()
    dense = DenseBackend(cv)
    rows = []
    insts = hidden_instances()
    for inst in insts:
        (_, ref), _ = dense.prepare_source(inst.oracle)
        z_in_h = bool(inst.log_h) and len(rref(inst.log_h+[(0, 0, 1)], P)) == len(inst.log_h)
        one, _, _ = simulate_source(inst, points=(1,))
        dirty, work, _ = simulate_source(inst, uncompute=False)
        rows.append({"instance": inst.name, "z_in_h": z_in_h,
                     "one_point_source_wrong": bool(np.abs(one-ref).max() > TOL),
                     "no_uncompute_source_wrong": bool(np.abs(dirty-ref).max() > TOL),
                     "no_uncompute_workspace_clean": abs(work-1) < TOL})
    _, flags = merge_permutation(1, bennett=False)
    nonwit = []
    for inst in insts:
        rho, _, _ = simulate_source(inst)
        branches, _ = simulate_instrument(rho)
        target = coset_density(expected_stage_indices(cv, inst.log_h, 1), 27)
        wrong = 0
        for labels in product(sorted(branches), repeat=3):
            bad = [s for s in product(range(P), repeat=3) if any(s) and s not in witnesses(labels)]
            for s in bad:
                sigma = channel_output([branches[l][1] for l in labels], s)
                wrong += np.abs(sigma-target).max() > TOL
        nonwit.append({"instance": inst.name, "non_witness_cases_with_wrong_output": int(wrong)})
    return {"sources": rows, "merge_without_bennett_uncompute": flags, "non_witness_scales": nonwit}


def report():
    t0 = time.time()
    dense = DenseBackend(cover())
    insts = hidden_instances()
    checks = [check_instance(inst, dense) for inst in insts]
    runs = []
    for inst in insts:
        for seed in range(3):
            got, queries = run_algorithm(inst, seed=20261102+seed)
            runs.append({"instance": inst.name, "seed": seed, "recovered": got == rref(inst.log_h, P),
                         "oracle_queries": queries})
    merge_flags = {s: merge_permutation(s)[1] for s in (1, 2)}
    bch_ok = {s: bool((merge_table(s) == bch_reference(s)).all()) for s in (1, 2)}
    rng = np.random.default_rng(5)
    aer = []
    for s in (1, 2):
        psi = rng.normal(size=81)+1j*rng.normal(size=81)
        psi /= np.linalg.norm(psi)
        qd, clean = merge_aer_check(psi, s)
        aer.append({"s": s, "max_diff_vs_bit_level": float(np.abs(
            qd-channel_output([np.outer(psi, psi.conj())], (s,))).max()), "scratch_clean": clean})
    aer_sources = []
    for inst in (insts[0], next(i for i in insts if not i.flags()["normal"]), insts[-1]):
        exact, _, _ = simulate_source(inst)
        sv, work, leak = simulate_source(inst, method="aer")
        aer_sources.append({"instance": inst.name, "max_diff_vs_exact": float(np.abs(sv-exact).max()),
                            "workspace_zero_probability": work, "padding_weight": leak})
    return {**STATUS, "aer_source_crosscheck": aer_sources, "instance": "Heis(F_3), cover dims (3, 1), c = 2, M_2 = 3",
            "subgroups": len(insts),
            "all_checks_pass": all(c["passed"] for c in checks),
            "all_runs_recover": all(r["recovered"] for r in runs),
            "merge_flags": merge_flags, "merge_equals_bch": bch_ok, "aer_merge_crosscheck": aer,
            "checks": checks, "runs": runs, "resources": resource_report(),
            "negative_controls": negative_controls(), "seconds": round(time.time()-t0, 1)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="write JSON here")
    args = parser.parse_args()
    result = report()
    text = json.dumps(result, indent=1, default=str)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text+"\n")
    for c in result["checks"]:
        print(c["instance"], c["branch_witness_cases"], "cases",
              "OK" if c["passed"] else "FAIL")
    for key in ("subgroups", "all_checks_pass", "all_runs_recover", "merge_flags", "merge_equals_bch",
                "aer_merge_crosscheck", "aer_source_crosscheck", "seconds"):
        print(key, result[key])
    print(json.dumps(result["resources"]["terminal_sample"], indent=1))


if __name__ == "__main__":
    main()
