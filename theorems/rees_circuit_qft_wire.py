"""Explicit QFT over Z/p (lem:qft-mod) wired into the gate-level Rees circuit
generator as an optional backend. AI-checked, pending human review.

Report: research/audits/reviews/2026-11-04-rees-qft-wire.md.
No existing file is edited: like theorems/rees_circuit_arith.py, this module
supplies a Builder subclass and a context manager that rebinds
rees_circuit_general.Builder (and check_macros) for the duration of a block.

Backends (keyword qft= of build_circuit / terminal_sample_circuit below):
* qft="exact" (default, unchanged): QFT_p is one exact b-qubit unitary gate
  "qft{p}" (identity on padding words), as in rees_circuit_general;
* qft="explicit": every QFT macro (and every inverse) is replaced by the gate
  list of theorems/rees_qft_mod.qft_mod_ops(p, t, r, tp) (inverse: the
  reversed list with rotation signs flipped), relabelled onto the macro's
  qudit (register X of the lemma), a QFT pool of 4b+2t+1 ancillas (F, Z, K,
  M, W, a of the lemma) and the 3b+5 arithmetic ancillas of the
  ArithBuilder (shared: the lemma uses the same blocks and layout). Gates:
  X, CX, CCX, SWAP, H, Phase(2 pi s/2^k), CPhase(2 pi s/2^k).
  pool="shared" (default) uses one pool for all calls (ancillas are returned
  to |0> up to the lemma's error); pool="fresh" gives each call its own pool
  (no reuse; used to separate the two error sources).
The arithmetic is always the poly(log p) binary backend (ArithBuilder): the
lemma's circuit needs its ancilla layout, and mixing it with the O(p^3)
value-controlled increments would be pointless.

Semantics. In the explicit backend a QFT call is no longer exact, so the
exact Z[zeta_p] engines (rees_circuit_general.Engine, rees_circuit_sparse)
are NOT applicable (Engine.source refuses a non-exact QFT head). What is
checked instead:
* structure (exact): every qft macro slice of a generated circuit equals the
  reference lem:qft-mod gate list under the qubit relabelling, and touches
  only its qudit, its pool and the arithmetic ancillas; every arithmetic
  macro passes the ArithBuilder checks (all canonical inputs, ancillas 0);
* per call (float): the emitted slice is simulated on every canonical input
  |x>|0> over all its qubits; sigma_max of (V - QFT_p (x) |0>) and the
  column error at x = 0 are reported against the proved bound B of the
  lemma (error_bound) and its exact prep term (the only error at x = 0);
* composites (float, shared pool): prefixes of the generated circuits are
  simulated gate by gate with a sparse state simulator over ALL qubits,
  for the explicit and the exact backend, and compared;
* end to end (proved composition of the above): hybrid argument. With the
  measurements deferred, ||psi_explicit - psi_exact (x) |0>_pool|| <=
  sum_k ||(V_k - U_k) psi_k|| where psi_k is the exact-backend state before
  call k (clean pool); for a call whose qudit is untouched before it
  (input |0>) this is the prep error, otherwise at most B (or sigma_max).
  The output distribution of one terminal sample is then within that
  total variation distance of the exact one, and a seeded run with n
  terminal samples is coupled to the exact run except with probability
  <= n times that.

What this does NOT show: a fixed finite gate set (Phase(2 pi/2^k) with
k <= max(r, tp) are primitives); a monolithic statevector simulation of a
whole terminal sample with the explicit backend (too large; see the report);
a coherent receiver; anything about the oracle cost T_f; noise.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from functools import lru_cache
import json
import math
import time

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import AncillaRegister, CircuitInstruction
from qiskit.circuit.library import CCXGate, CPhaseGate, CXGate, HGate, PhaseGate, SwapGate, XGate

import theorems.rees_circuit_arith as A
import theorems.rees_circuit_general as G
import theorems.rees_qft_mod as Q

WIRE_STATUS = {**G.STATUS,
               "status": "explicit_qft_mod_p_wired_as_optional_backend_finite_checks",
               "explicit_qft_backend_available": True,          # optional; default stays exact
               "default_backend_unchanged": True,
               "poly_log_p_arithmetic_implemented": True,
               "fixed_finite_gate_set": False,
               "monolithic_explicit_simulation": False,          # modules + hybrid bound only
               "coherent_receiver_implemented": False, "general_sde_implemented": False,
               "formal_compiler_checked": False, "independent_review": False,
               "novelty_established": False, "speedup_claim_allowed": False,
               "review": "AI-checked, pending human review"}

QFT_GATE_NAMES = ("x", "cx", "ccx", "swap", "h", "p", "cp")


def pool_size(nb, t):
    """F, Z, K (b each), M (t), W (t+b), a (1)."""
    return 4*nb+2*t+1


@lru_cache(maxsize=None)
def reference_ops(p, t, r, tp, inverse=False):
    """The lem:qft-mod gate list on its own layout (X = 0..b-1, then F, Z, K, M, W, a, arith)."""
    ops, L, _ = Q.qft_mod_ops(p, t, r, tp, inverse)
    return tuple(ops), L


@lru_cache(maxsize=None)
def _gate(name, k=None, s=None):
    if name == "x":
        return XGate()
    if name == "cx":
        return CXGate()
    if name == "ccx":
        return CCXGate()
    if name == "swap":
        return SwapGate()
    if name == "h":
        return HGate()
    ang = s*2*math.pi/2**k
    return PhaseGate(ang) if name == "r" else CPhaseGate(ang)


def _op_of(g):
    return _gate(g[0], g[2], g[3]) if g[0] in ("r", "cr") else _gate(g[0])


def resolve_params(p, params=None, eta=None):
    if params is not None:
        t, r, tp = params
        return int(t), int(min(r, t)), int(tp)
    if eta is not None:
        t, r, tp = Q.params_for_eta(p, eta)
        return t, min(r, t), tp
    raise ValueError("give params=(t, r, tp) or eta")


# ====================================================================== the Builder

class ExplicitQFTBuilder(A.ArithBuilder):
    """ArithBuilder whose qft() emits the lem:qft-mod gate list (with its ancillas)."""

    qft_params = None          # (t, r, tp), set by make_builder
    pool_mode = "shared"

    def __init__(self, qc, enc):
        super().__init__(qc, enc)
        if self.qft_params is None:
            raise ValueError("use make_builder(params) / explicit_qft_backend(...)")
        self.t, self.r, self.tp = self.qft_params
        self.pool_regs = []
        self.qft_gate_counts = Counter()
        self.qft_calls = []        # (macro index, role, inverse)
        self.call_pool = {}        # macro index -> pool register index

    def _pool(self):
        """Index of the pool register for the next call."""
        if self.pool_mode == "shared" and self.pool_regs:
            return 0
        if self.pool_mode not in ("shared", "fresh"):
            raise ValueError(self.pool_mode)
        reg = AncillaRegister(pool_size(self.nb, self.t), f"qftpool{len(self.pool_regs)}")
        self.qc.add_register(reg)
        self.pool_regs.append(reg)
        return len(self.pool_regs)-1

    def qubit_map(self, q, pool_index):
        """Layout index of the lemma -> circuit qubit, for a call on qudit q."""
        pool = list(self.pool_regs[pool_index])
        anc = self._ancillas().all
        qmap = list(q)+pool+list(anc)
        _, L = reference_ops(self.p, self.t, self.r, self.tp)
        if len(qmap) != L.nq:
            raise AssertionError("layout size mismatch")
        return qmap

    def qft(self, q, role, inverse=False):
        ops, _ = reference_ops(self.p, self.t, self.r, self.tp, inverse)
        pidx = self._pool()
        qmap = self.qubit_map(q, pidx)
        start = self._len()
        names = Counter(g[0] for g in ops)
        self.qft_gate_counts.update(names)
        self._n += len(ops)
        if not self.count_only:
            app = self.qc._append
            for g in ops:
                app(CircuitInstruction(_op_of(g), tuple(qmap[i] for i in g[1])))
        self.counts[role] += 1
        self._macro("qft_dg" if inverse else "qft", (q,), None, start)
        self.qft_calls.append((len(self.macros)-1, role, inverse))
        self.call_pool[len(self.macros)-1] = pidx

    def qft_gate_total(self):
        return sum(self.qft_gate_counts[k] for k in ("x", "cx", "ccx", "swap", "h", "r", "cr"))


class CountingExplicitQFTBuilder(ExplicitQFTBuilder):
    count_only = True


def make_builder(params, pool="shared", count_only=False):
    base = CountingExplicitQFTBuilder if count_only else ExplicitQFTBuilder
    return type(f"ExplicitQFTBuilder_{params[0]}_{params[1]}_{params[2]}_{pool}", (base,),
                {"qft_params": tuple(params), "pool_mode": pool})


# ====================================================================== checks

_QFT_SIG_CACHE = {}


def _check_arith_macro(qc, B, kind, qudits, coeff, start, end):
    """The per-macro check of rees_circuit_arith.check_macros_arith (same tests)."""
    p, nb = B.p, B.enc.nb
    data = qc.data
    local = {qb: ("q", r, i) for r, q in enumerate(qudits) for i, qb in enumerate(q)}
    for j, qb in enumerate(B.anc_reg or []):
        local[qb] = ("a", j)
    try:
        sig = (kind, coeff, tuple((inst.operation.name, tuple(local[q] for q in inst.qubits))
                                  for inst in data[start:end]))
    except KeyError:
        raise AssertionError("macro gate touches a qubit outside its qudits and the ancilla register")
    if sig in A._ARITH_CACHE:
        return
    from itertools import product
    vals = np.array(list(product(range(p), repeat=len(qudits))), dtype=np.int64)
    out, anc_out, targets = A._sim_slice(qc, B, start, end, qudits, vals)
    if (out != A._want(kind, coeff, vals, p)).any():
        raise ArithmeticError(f"macro {kind} gate slice is not its declared map")
    if anc_out.any():
        raise ArithmeticError(f"macro {kind} leaves an ancilla dirty")
    if any(r*nb+i in targets for r in range(1, len(qudits)) for i in range(nb)):
        raise ArithmeticError(f"macro {kind} targets an operand")
    A._ARITH_CACHE[sig] = True


def check_qft_slice(qc, B, macro):
    """Exact structural check: the slice is the lem:qft-mod list relabelled onto
    (qudit, pool, arith ancillas); same gate types, angles and qubits, in order."""
    kind, qudits, _, start, end = macro
    inverse = kind == "qft_dg"
    ops, L = reference_ops(B.p, B.t, B.r, B.tp, inverse)
    if end-start != len(ops):
        raise AssertionError("qft slice has the wrong length")
    data = qc.data
    qudit = qudits[0]
    mi = next(i for i, m in enumerate(B.macros) if m[3] == start and m[4] == end and m[0] == kind)
    pool = B.pool_regs[B.call_pool[mi]]
    allowed = set(qudit) | set(B.anc_reg) | set(pool)
    qmap = list(qudit)+list(pool)+list(B.anc_reg)
    key = (B.p, B.t, B.r, B.tp, inverse)
    for k, g in enumerate(ops):
        inst = data[start+k]
        if any(q not in allowed for q in inst.qubits):
            raise AssertionError("qft slice touches a qubit outside its qudit, pool and ancillas")
        if tuple(inst.qubits) != tuple(qmap[i] for i in g[1]):
            raise AssertionError("qft slice qubits differ from the reference list")
        op = inst.operation
        if g[0] in ("r", "cr"):
            want = ("p" if g[0] == "r" else "cp", g[3]*2*math.pi/2**g[2])
            if op.name != want[0] or abs(float(op.params[0])-want[1]) > 1e-15:
                raise AssertionError("qft slice rotation differs from the reference list")
        elif op.name != g[0]:
            raise AssertionError("qft slice gate differs from the reference list")
    _QFT_SIG_CACHE[key] = True
    return True


def check_macros_qft(qc, B):
    """Every gate except a measurement is in exactly one macro; qft macros are the relabelled reference
    list (check_qft_slice); arithmetic macros as in check_macros_arith; swap and
    oracle macros as in the original. Returns the number of macros checked."""
    covered = 0
    data = qc.data
    skip = lambda i: i < len(data) and data[i].operation.name == "measure"
    for macro in B.macros:
        kind, qudits, coeff, start, end = macro
        while covered < start and skip(covered):     # mid-circuit measurements of a terminal sample
            covered += 1
        if start != covered:
            raise AssertionError(f"gate {covered} is outside every macro")
        covered = end
        if kind in ("qft", "qft_dg"):
            check_qft_slice(qc, B, macro)
        elif kind == "oracle":
            if end-start > 1 or (end-start == 1 and data[start].operation.name != "U_f"):
                raise AssertionError("bad oracle macro")
        elif kind == "swap":
            half = len(qudits)//2
            want = [(a, b) for qa, qb in zip(qudits[:half], qudits[half:]) for a, b in zip(qa, qb)]
            got = [tuple(inst.qubits) for inst in data[start:end]]
            if got != want or any(inst.operation.name != "swap" for inst in data[start:end]):
                raise AssertionError("bad swap macro")
        else:
            _check_arith_macro(qc, B, kind, qudits, coeff, start, end)
    while skip(covered):
        covered += 1
    if covered != len(data):
        raise AssertionError("trailing gates outside every macro")
    return len(B.macros)


# ====================================================================== backend selection

@contextmanager
def explicit_qft_backend(params, pool="shared", count_only=False):
    """Rebind rees_circuit_general.Builder / check_macros to the explicit-QFT backend."""
    saved = (G.Builder, G.check_macros)
    G.Builder = make_builder(params, pool, count_only)
    G.check_macros = check_macros_qft
    try:
        yield G.Builder
    finally:
        G.Builder, G.check_macros = saved


@contextmanager
def backend(qft="exact", params=None, eta=None, p=None, pool="shared", arith=True, count_only=False):
    """qft='exact' (default): the generator as it is (with arith=True the ArithBuilder
    arithmetic, else the original value-controlled increments); qft='explicit':
    ArithBuilder arithmetic and the lem:qft-mod transform."""
    if qft == "exact":
        if arith:
            builder = A.CountingArithBuilder if count_only else None
            with A.arith_backend(builder):
                yield
        else:
            yield
    elif qft == "explicit":
        prm = resolve_params(p, params, eta) if (params is not None or p is not None) else None
        if prm is None:
            raise ValueError("explicit backend needs params or (p, eta)")
        with explicit_qft_backend(prm, pool, count_only):
            yield
    else:
        raise ValueError(qft)


def terminal_sample_circuit(cfg, inst=None, witness=None, *, qft="exact", params=None, eta=None,
                            pool="shared", arith=True, count_only=False):
    """rees_circuit_general.terminal_sample_circuit with a QFT backend option.
    qft='exact', arith=False is exactly the original generator."""
    with backend(qft, params, eta, cfg.p, pool, arith, count_only):
        return G.terminal_sample_circuit(cfg, inst, witness)


def build(fn, cfg, *args, qft="exact", params=None, eta=None, pool="shared", arith=True, count_only=False, **kw):
    """Any generator function (source_circuit, instrument_circuit, merge_circuit,
    fourier_circuit, ...) under the chosen backend."""
    with backend(qft, params, eta, cfg.p, pool, arith, count_only):
        return fn(cfg, *args, **kw)


# ====================================================================== sparse simulation of generated circuits

class CircuitState(Q.SparseState):
    """rees_qft_mod.SparseState plus the gates of the exact backend: multi-controlled
    X with control state, a dense unitary on a few qubits (the exact qft{p}) and
    the table oracle U_f (a permutation of basis states)."""

    def run(self, gates):
        for g in gates:
            nm = g[0]
            if nm == "mcx":
                _, ctrls, state, tw, to = g
                m = np.ones(len(self.amps), dtype=bool)
                for i, (w, o) in enumerate(ctrls):
                    m &= self._bit(w, o).astype(bool) == bool(state >> i & 1)
                self.keys[tw] ^= m.astype(np.uint64) << np.uint64(to)
            elif nm == "u":
                self._unitary(g[1], g[2])
            elif nm == "oracle":
                self._oracle(*g[1:])
            else:
                super().run([g])
        return self

    def _local(self, wires):
        v = np.zeros(len(self.amps), dtype=np.int64)
        for i, (w, o) in enumerate(wires):
            v |= self._bit(w, o).astype(np.int64) << i
        return v

    def _unitary(self, wires, U):
        k = len(wires)
        v = self._local(wires)
        base = [kk.copy() for kk in self.keys]
        for w, o in wires:
            base[w] &= ~np.uint64(1 << o)
        new_keys, new_amps = [[] for _ in range(self.W)], []
        for vp in range(1 << k):
            coef = U[vp, v]
            nz = np.abs(coef) > 0
            if not nz.any():
                continue
            ks = [b[nz].copy() for b in base]
            for i, (w, o) in enumerate(wires):
                if vp >> i & 1:
                    ks[w] |= np.uint64(1 << o)
            for i in range(self.W):
                new_keys[i].append(ks[i])
            new_amps.append(coef[nz]*self.amps[nz])
        keys = [np.concatenate(x) for x in new_keys]
        amps = np.concatenate(new_amps)
        self.keys, self.amps = _merge(keys, amps, self.W)
        keep = np.abs(self.amps) >= 1e-15
        pm = float(np.sum(np.abs(self.amps[~keep])**2))
        self.pruned += pm
        self.prune_err += math.sqrt(pm)
        self.keys = [kk[keep] for kk in self.keys]
        self.amps = self.amps[keep]
        self.max_support = max(self.max_support, len(self.amps))

    def _oracle(self, wq, wy, table, p, m):
        idx = np.zeros(len(self.amps), dtype=np.int64)
        canon = np.ones(len(self.amps), dtype=bool)
        for j in range(m):
            d = self._local(wq[j])
            canon &= d < p
            idx = idx*p+np.where(d < p, d, 0)
        val = np.where(canon, np.asarray(table, dtype=np.int64)[idx], 0)
        for bit, (w, o) in enumerate(wy):
            self.keys[w] ^= ((val >> bit) & 1).astype(np.uint64) << np.uint64(o)


def _merge(keys, amps, W):
    if W == 1:
        u, inv = np.unique(keys[0], return_inverse=True)
        uk = [u]
    else:
        arr = np.ascontiguousarray(np.stack(keys, axis=1))
        v = arr.view(np.dtype((np.void, 8*W))).ravel()
        u, inv = np.unique(v, return_inverse=True)
        uu = u.view(np.uint64).reshape(-1, W)
        uk = [np.ascontiguousarray(uu[:, i]) for i in range(W)]
    inv = inv.ravel()
    n = len(uk[0])
    a = np.bincount(inv, weights=amps.real, minlength=n)+1j*np.bincount(inv, weights=amps.imag, minlength=n)
    return uk, a


def compile_instructions(instructions, idx):
    """Qiskit instructions -> CircuitState gate tuples; idx: qubit -> local index."""
    wo = lambda q: (idx[q] // 64, idx[q] % 64)
    out = []
    for inst in instructions:
        op = inst.operation
        nm = op.name
        qs = [wo(q) for q in inst.qubits]
        if nm in ("x", "h"):
            out.append((nm, *qs[0]))
        elif nm == "swap":
            out.append(("swap", *qs[0], *qs[1]))
        elif nm == "cx" and int(getattr(op, "ctrl_state", 1)) == 1:
            out.append(("cx", *qs[0], *qs[1]))
        elif nm == "ccx" and int(getattr(op, "ctrl_state", 3)) == 3:
            out.append(("ccx", *qs[0], *qs[1], *qs[2]))
        elif nm in ("cx", "ccx", "mcx") or (hasattr(op, "base_gate") and op.base_gate.name == "x"):
            out.append(("mcx", qs[:-1], int(op.ctrl_state), *qs[-1]))
        elif nm == "p":
            out.append(("p", *qs[0], np.exp(1j*float(op.params[0]))))
        elif nm == "cp":
            out.append(("cp", *qs[0], *qs[1], np.exp(1j*float(op.params[0]))))
        elif nm.startswith("qft") and op.num_qubits <= 4:
            p = int(nm[3:].split("_")[0])
            out.append(("u", qs, G.qft_matrix(p, nm.endswith("_dg"))))
        elif isinstance(op, G.TableOracle):
            nb, m = op.enc.nb, op.m_coords
            wq = [[qs[nb*(m-1-j)+i] for i in range(nb)] for j in range(m)]
            out.append(("oracle", wq, qs[m*nb:], op.table, op.enc.p, m))
        else:
            raise ValueError(f"unsupported instruction {nm}")
    return out


def simulate_prefix(qc, end=None, tol=1e-10, init=0):
    """Simulate qc.data[:end] (no measurement inside) from |init> over all qubits."""
    idx = {q: i for i, q in enumerate(qc.qubits)}
    data = qc.data[:end] if end is not None else qc.data
    if any(inst.operation.name in ("measure", "reset") for inst in data):
        raise ValueError("prefix contains a measurement")
    st = CircuitState(qc.num_qubits, [init], tol=tol)
    st.run(compile_instructions(data, idx))
    return st


def first_measure(qc):
    for i, inst in enumerate(qc.data):
        if inst.operation.name == "measure":
            return i
    return len(qc.data)


def state_by_register(qc, st):
    """{(register name, index) tuple key -> amplitude}: a backend-independent form
    (qubits identified by register name and index)."""
    names = []
    for q in qc.qubits:
        loc = qc.find_bit(q).registers[0]
        names.append((loc[0].name, loc[1]))
    ks = st.key_ints()
    out = {}
    for k, a in zip(ks, st.amps):
        k = int(k)
        bits = tuple(sorted(names[i] for i in range(len(names)) if k >> i & 1))
        out[bits] = out.get(bits, 0)+a
    return out


def state_distance(d1, d2):
    keys = set(d1) | set(d2)
    return math.sqrt(sum(abs(d1.get(k, 0)-d2.get(k, 0))**2 for k in keys))


# ====================================================================== per-call operator error

def call_operator_error(qc, B, macro, tol=1e-13):
    """Float check of ONE emitted qft macro slice: for every canonical x the full
    output V|x>|0> over all qubits the slice touches, minus (QFT_p^{+-1}|x>)|0>;
    returns sigma_max (operator norm on the canonical subspace), the column
    errors, and the pruning accounting (as rees_qft_mod.operator_error)."""
    kind, qudits, _, start, end = macro
    p, nb = B.p, B.enc.nb
    q = qudits[0]
    insts = qc.data[start:end]
    others = sorted({qb for inst in insts for qb in inst.qubits} - set(q), key=lambda x: qc.find_bit(x).index)
    idx = {qb: i for i, qb in enumerate(q)}
    for i, qb in enumerate(others):
        idx[qb] = nb+i
    nq = nb+len(others)
    gates = compile_instructions(insts, idx)
    sign = -1 if kind == "qft_dg" else 1
    rows_k, rows_v, cols = [], [], []
    perr, maxsup, col_err = 0.0, 0, []
    W = (nq+63)//64
    for x in range(p):
        st = CircuitState(nq, [x], tol=tol).run(gates)
        perr = max(perr, st.prune_err)
        maxsup = max(maxsup, st.max_support)
        stk = np.stack(st.keys, axis=1)
        ideal = np.zeros((p, W), dtype=np.uint64)
        ideal[:, 0] = np.arange(p, dtype=np.uint64)
        iamp = np.exp(sign*2j*math.pi*x*np.arange(p)/p)/math.sqrt(p)
        rows_k.append(np.concatenate([stk, ideal]))
        rows_v.append(np.concatenate([st.amps, -iamp]))
        cols.append(np.full(len(st.amps)+p, x))
    allk = np.ascontiguousarray(np.concatenate(rows_k))
    v = allk.view(np.dtype((np.void, 8*allk.shape[1]))).ravel()
    _, rid = np.unique(v, return_inverse=True)
    rid = rid.ravel()
    from scipy.sparse import coo_matrix
    E = coo_matrix((np.concatenate(rows_v), (rid, np.concatenate(cols))), shape=(rid.max()+1, p)).tocsc()
    Gm = (E.conj().T @ E).toarray()
    ev = np.linalg.eigvalsh((Gm+Gm.conj().T)/2)
    sigma = float(math.sqrt(max(ev[-1], 0.0)))
    col_err = [float(math.sqrt(max(Gm[x, x].real, 0.0))) for x in range(p)]
    return {"kind": kind, "p": p, "t": B.t, "r": B.r, "tp": B.tp, "qubits_touched": nq, "gates": len(insts),
            "sigma_max": sigma, "sigma_upper": sigma+math.sqrt(p)*perr, "column_errors": col_err,
            "prune_err_max": perr, "max_support": maxsup, "bound": Q.error_bound(p, B.t, B.r, B.tp)}


# ====================================================================== hybrid accounting

def qft_call_inputs(qc, B):
    """For each qft macro (in circuit order): (macro index, kind, zero_input), where
    zero_input means no earlier gate touches the macro's qudit, so in the exact-
    backend run its input is |0> (exact computation on the gate list)."""
    first = {}
    for i, inst in enumerate(qc.data):
        for qb in inst.qubits:
            first.setdefault(qb, i)
    out = []
    for mi, (kind, qudits, _, start, end) in enumerate(B.macros):
        if kind in ("qft", "qft_dg"):
            zero = all(first.get(qb, start) >= start for qb in qudits[0])
            out.append((mi, kind, zero))
    return out


def hybrid_budget(calls, p, t, r, tp, sim=None):
    """Upper bound on ||psi_explicit - psi_exact (x) |0>|| for a circuit with the
    given qft calls. 'proved': zero-input forward calls cost the exact prep error
    (the only nonzero term of Theorem 6 at x = 0: the phase is exact on xy = 0 and
    the phase estimation of the eigenvalue 1 is exact for every r), every other
    call costs B. 'float': the same with the simulated column error at x = 0 and
    sigma_max (sim = {'qft': call_operator_error(...), 'qft_dg': ...})."""
    bd = Q.error_bound(p, t, r, tp)
    n = Counter()
    for _, kind, zero in calls:
        n[(kind, "zero" if zero else "general")] += 1
    proved = 0.0
    for (kind, inp), k in n.items():
        proved += k*(bd["prep"] if (kind == "qft" and inp == "zero") else bd["B"])
    out = {"calls": {f"{a}_{b}": v for (a, b), v in sorted(n.items())}, "n_calls": sum(n.values()),
           "proved_total": proved, "B": bd["B"], "prep": bd["prep"]}
    if sim is not None:
        fl = 0.0
        for (kind, inp), k in n.items():
            s = sim[kind]
            fl += k*(s["column_errors"][0] if inp == "zero" else s["sigma_upper"])
        out["float_total"] = fl
    return out


def coupling_bound(budget_per_sample, n_samples):
    """P(a seeded explicit run differs from the coupled exact run) <= n * delta,
    delta = TV of one terminal sample <= ||psi - psi'|| (deferred measurement)."""
    return min(1.0, n_samples*budget_per_sample)


# ====================================================================== counts

def circuit_counts(qc, B):
    arith = {k: v for k, v in B.gate_counts.items() if v}
    q = dict(getattr(B, "qft_gate_counts", {}))
    out = {"qubits": qc.num_qubits, "ancillas_arith": len(B.anc_reg) if getattr(B, "anc_reg", None) else 0,
           "pool_qubits": sum(len(r) for r in getattr(B, "pool_regs", [])),
           "arith_gates": sum(arith.get(k, 0) for k in ("x", "cx", "ccx", "swap")),
           "swap_macro_gates": arith.get("swap_macro", 0),
           "qft_calls": sum(v for k, v in B.counts.items() if k.startswith("qft")),
           "oracle_calls": B.counts.get("oracle_calls", 0)}
    if q:
        out["qft_gates"] = sum(q.get(k, 0) for k in ("x", "cx", "ccx", "swap", "h", "r", "cr"))
        out["qft_gate_types"] = {k: q.get(k, 0) for k in ("x", "cx", "ccx", "swap", "h", "r", "cr")}
        out["qft_gates_per_call"] = out["qft_gates"]/max(out["qft_calls"], 1)
    else:
        out["qft_gates"] = arith.get("qft_unitary", 0) or out["qft_calls"]
    out["total_gates_excl_oracle"] = out["arith_gates"]+out["swap_macro_gates"]+out["qft_gates"]
    return out


def terminal_counts(cfg, qft="exact", params=None, eta=None, pool="shared"):
    """Gate and qubit counts of ONE terminal sample (count-only emission)."""
    t0 = time.time()
    qc, B = terminal_sample_circuit(cfg, qft=qft, params=params, eta=eta, pool=pool, count_only=True)
    out = circuit_counts(qc, B)
    if qft == "explicit":
        out["params"] = {"t": B.t, "r": B.r, "tp": B.tp}
        out["max_rotation_index"] = max(B.r, B.tp)
        calls = qft_call_inputs_counted(cfg, B)
        out["zero_input_calls"] = calls
    out["seconds"] = round(time.time()-t0, 2)
    return out


def qft_call_inputs_counted(cfg, B):
    """Zero-input classification needs the gate list; in count-only mode it is
    recomputed from a full emission with the exact backend (same macro order)."""
    with backend("exact"):
        qc, Bx = G.terminal_sample_circuit(cfg)
    calls = qft_call_inputs(qc, Bx)
    return {"zero": sum(1 for c in calls if c[2]), "general": sum(1 for c in calls if not c[2])}


# ====================================================================== composite runs

def compare_prefix(cfg, inst, params, end_fn=first_measure, tol=1e-10, pool="shared", log=None):
    """Gate-by-gate sparse simulation of the same prefix of the terminal-sample
    circuit under the exact backend (ArithBuilder + exact QFT) and the explicit
    one; returns the full-state distance, the label law of the first measured
    register (if the prefix ends at a measurement) and the hybrid budget."""
    t0 = time.time()
    with backend("exact"):
        qc0, B0 = G.terminal_sample_circuit(cfg, inst)
    with backend("explicit", params=params, pool=pool):
        qc1, B1 = G.terminal_sample_circuit(cfg, inst)
        check_macros_qft(qc1, B1)
    e0, e1 = end_fn(qc0), end_fn(qc1)
    # the prefixes must contain the same macros
    nm0 = [m for m in B0.macros if m[4] <= e0]
    nm1 = [m for m in B1.macros if m[4] <= e1]
    if [m[:3] for m in nm0] != [m[:3] for m in nm1]:
        raise AssertionError("prefixes differ in their macros")
    s0 = simulate_prefix(qc0, e0, tol=tol)
    if log:
        log("exact prefix", len(s0.amps), round(time.time()-t0, 1))
    s1 = simulate_prefix(qc1, e1, tol=tol)
    if log:
        log("explicit prefix", len(s1.amps), s1.max_support, round(time.time()-t0, 1))
    d0, d1 = state_by_register(qc0, s0), state_by_register(qc1, s1)
    dist = state_distance(d0, d1)
    calls = [c for c in qft_call_inputs(qc1, B1) if B1.macros[c[0]][4] <= e1]
    out = {"instance": inst.name, "prefix_gates_exact": e0, "prefix_gates_explicit": e1,
           "qubits_exact": qc0.num_qubits, "qubits_explicit": qc1.num_qubits,
           "support_exact": len(s0.amps), "support_explicit": len(s1.amps), "max_support_explicit": s1.max_support,
           "prune_err_explicit": s1.prune_err, "state_distance": dist,
           "norm_explicit": float(np.sum(np.abs(s1.amps)**2))}
    # label law of the measured register at the end of the prefix
    if e1 < len(qc1.data) and qc1.data[e1].operation.name == "measure":
        mq, mq0 = _measured_block(qc1, e1), _measured_block(qc0, e0)
        out["measured_register"] = sorted({qc1.find_bit(q).registers[0][0].name for q in mq})
        out["label_law_exact"] = _law(qc0, s0, mq0)
        out["label_law_explicit"] = _law(qc1, s1, mq)
        keys = set(out["label_law_exact"]) | set(out["label_law_explicit"])
        out["label_tv"] = 0.5*sum(abs(out["label_law_exact"].get(k, 0)-out["label_law_explicit"].get(k, 0))
                                  for k in keys)
    out["hybrid"] = hybrid_budget(calls, cfg.p, *B1.qft_params)
    out["seconds"] = round(time.time()-t0, 1)
    return out


def _measured_block(qc, e):
    """Qubits of the consecutive single-qubit measurements starting at gate e."""
    out = []
    while e < len(qc.data) and qc.data[e].operation.name == "measure":
        out += list(qc.data[e].qubits)
        e += 1
    return out


def _law(qc, st, qubits):
    idx = {q: i for i, q in enumerate(qc.qubits)}
    ks = st.key_ints()
    law = Counter()
    for k, a in zip(ks, st.amps):
        k = int(k)
        lab = "".join(str(k >> idx[q] & 1) for q in qubits)
        law[lab] += abs(a)**2
    return {k: float(v) for k, v in sorted(law.items())}


def instrument_block_error(cfg, d, params, tol=1e-12, pool="shared"):
    """The instrument of grade d, explicit vs exact backend, simulated over ALL its
    qubits on every canonical input of its address qudits (the instrument only
    touches the top coordinates and z): max over inputs of the output-state
    distance, and its hybrid budget (one zero-input call and one general call
    per top coordinate)."""
    t0 = time.time()
    with backend("exact"):
        qc0, B0, _ = G.instrument_circuit(cfg, d)
    with backend("explicit", params=params, pool=pool):
        qc1, B1, (a_reg, a, z_reg, z) = G.instrument_circuit(cfg, d)
        check_macros_qft(qc1, B1)
    p, nb = cfg.p, cfg.enc.nb
    top = cfg.top(d)
    from itertools import product
    worst, rows = 0.0, 0
    pos1 = {q: i for i, q in enumerate(qc1.qubits)}
    pos0 = {q: i for i, q in enumerate(qc0.qubits)}
    worst_err = 0.0
    for vals in product(range(p), repeat=len(top)):
        # qudit j of register a is qubits nb(n-1-j)+i; same register names in both circuits
        k0 = sum(((v >> i) & 1) << _pos_by_name(qc0, a_reg.name, nb*(cfg.width[d]-1-tcoord)+i)
                 for v, tcoord in zip(vals, top) for i in range(nb))
        k1 = sum(((v >> i) & 1) << _pos_by_name(qc1, a_reg.name, nb*(cfg.width[d]-1-tcoord)+i)
                 for v, tcoord in zip(vals, top) for i in range(nb))
        s0 = CircuitState(qc0.num_qubits, [k0], tol=0.0).run(compile_instructions(qc0.data, pos0))
        s1 = CircuitState(qc1.num_qubits, [k1], tol=tol).run(compile_instructions(qc1.data, pos1))
        dist = state_distance(state_by_register(qc0, s0), state_by_register(qc1, s1))
        worst = max(worst, dist)
        worst_err = max(worst_err, s1.prune_err)
        rows += 1
    calls = qft_call_inputs(qc1, B1)
    return {"d": d, "p": p, "top_coordinates": len(top), "inputs": rows, "qubits_exact": qc0.num_qubits,
            "qubits_explicit": qc1.num_qubits, "gates_explicit": len(qc1.data), "max_state_distance": worst,
            "prune_err_max": worst_err, "hybrid": hybrid_budget(calls, p, *B1.qft_params),
            "seconds": round(time.time()-t0, 1)}


def _pos_by_name(qc, reg_name, index):
    for i, q in enumerate(qc.qubits):
        reg, j = qc.find_bit(q).registers[0]
        if reg.name == reg_name and j == index:
            return i
    raise KeyError((reg_name, index))


def source_prefix_end(qc):
    """End of the first top source (before its instrument): the gate after the
    last U_f / evaluation macro that precedes the first measurement."""
    m = first_measure(qc)
    last = 0
    for i, inst in enumerate(qc.data[:m]):
        if inst.operation.name == "U_f":
            last = i
    return last+1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", default="counts")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    from theorems.rees_end_to_end_sim import filiform4, heisenberg
    res = {"status": WIRE_STATUS}
    if args.job == "counts":
        for name, alg in (("heis_f3", heisenberg(3)), ("n4_f5", filiform4(5))):
            cfg = G.Config(alg)
            res[name] = {"exact": terminal_counts(cfg),
                         "explicit_sim": terminal_counts(cfg, "explicit", params=(cfg.enc.nb+5,)*2+(28,))}
    print(json.dumps(res, indent=1, default=str))
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
