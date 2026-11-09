"""Tests for theorems/rees_qft_mod.py (approximate QFT over Z/N with clean workspace).
Fast tests take well under a minute; the N in {9, 11, 13, 25, 27} full-operator
checks are slow (REES_SLOW=1)."""
import math
import os
import random

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from theorems.rees_qft_mod import (
    STATUS, SparseState, aqft_inv_ops, classical_eval, compile_qiskit, decoder_ops, error_bound, gate_bound,
    gate_counts, make_layout, operator_error, ops_to_gates, params_for_eta, pe_tail_float, phase_numerators,
    prep_ops, qft_mod_circuit, qft_mod_ops, QOps,
)
from theorems.rees_circuit_arith import Anc, add_product_ops, load_const, mod_add_reg

slow = pytest.mark.skipif(os.environ.get("REES_SLOW") != "1", reason="slow; set REES_SLOW=1")
NS = (3, 5, 7, 9, 11, 13, 25, 27)


def test_status_gates_stay_false():
    for k in ("coherent_receiver_implemented", "general_sde_implemented", "formal_compiler_checked",
              "independent_review", "novelty_established", "speedup_claim_allowed",
              "rees_generator_uses_this_qft", "fixed_finite_gate_set"):
        assert STATUS[k] is False


def test_sparse_simulator_matches_qiskit_statevector():
    rng = random.Random(7)
    for trial in range(6):
        n = 7
        qc = QuantumCircuit(n)
        for _ in range(60):
            g = rng.choice(["x", "cx", "ccx", "swap", "h", "p", "cp"])
            qs = rng.sample(range(n), 3)
            if g == "x":
                qc.x(qs[0])
            elif g == "cx":
                qc.cx(qs[0], qs[1])
            elif g == "ccx":
                qc.ccx(*qs)
            elif g == "swap":
                qc.swap(qs[0], qs[1])
            elif g == "h":
                qc.h(qs[0])
            elif g == "p":
                qc.p(2*math.pi*rng.choice([1, -1])/2**rng.randint(1, 6), qs[0])
            else:
                qc.cp(2*math.pi*rng.choice([1, -1])/2**rng.randint(1, 6), qs[0], qs[1])
        init = rng.randrange(2**n)
        st = SparseState(n, [init], tol=0.0).run(compile_qiskit(qc))
        vec = np.zeros(2**n, complex)
        for k, a in zip(st.key_ints(), st.amps):
            vec[int(k)] += a
        ref = Statevector.from_int(init, 2**n).evolve(qc).data
        assert np.allclose(vec, ref, atol=1e-12)


def test_aqft_block_matches_inverse_qft_and_drop_bound():
    for t in (3, 5, 6):
        D = 2**t
        for r in range(1, t+1):
            gates = ops_to_gates(aqft_inv_ops(list(range(t)), r), t)
            U = np.zeros((D, D), complex)
            for m in range(D):
                st = SparseState(t, [m], tol=0.0).run(gates)
                for k, a in zip(st.key_ints(), st.amps):
                    l = sum(((int(k) >> (t-1-i)) & 1) << i for i in range(t))   # bit-reversed output
                    U[l, m] += a
            F = np.exp(-2j*math.pi*np.outer(np.arange(D), np.arange(D))/D)/math.sqrt(D)
            err = np.linalg.norm(U-F, 2)
            bound = sum((t-k+1)*2*math.sin(math.pi/2**k) for k in range(r+1, t+1))
            assert err <= bound+1e-12
            if r == t:
                assert err < 1e-12


@pytest.mark.parametrize("N", NS)
def test_multiplier_exhaustive_on_canonical_inputs(N):
    """Exact computation: Z += x*y mod N with all ancillas clean, all x, y < N."""
    L = make_layout(N, 2)
    A = Anc(L.anc, L.b)
    ops = QOps()
    ops += add_product_ops(N, L.Z, L.X, L.F, 1, A)
    ins, want = [], []
    for x in range(N):
        for y in range(N):
            for z in (0, (x+2*y) % N):
                ins.append(sum(((x >> i) & 1) << L.X[i] for i in range(L.b)) |
                           sum(((y >> i) & 1) << L.F[i] for i in range(L.b)) |
                           sum(((z >> i) & 1) << L.Z[i] for i in range(L.b)))
                zz = (z+x*y) % N
                want.append(ins[-1] & ~sum(1 << q for q in L.Z) | sum(((zz >> i) & 1) << L.Z[i] for i in range(L.b)))
    out = classical_eval(ops_to_gates(ops, L.nq), L.nq, ins)
    assert [int(o) for o in out] == want


@pytest.mark.parametrize("N", NS)
def test_controlled_shift_exhaustive(N):
    """Exact computation: F += 2^j mod N controlled on m_j, identity when m_j = 0."""
    L = make_layout(N, 4)
    A = Anc(L.anc, L.b)
    for j in range(L.t):
        ops = QOps()
        cj = pow(2, j, N)
        load_const(ops, cj, A.Y, (L.M[j],))
        mod_add_reg(ops, N, A.Y, L.F, A, L.M[j])
        load_const(ops, cj, A.Y, (L.M[j],))
        ins, want = [], []
        for y in range(N):
            for m in (0, 1):
                k = sum(((y >> i) & 1) << L.F[i] for i in range(L.b)) | (m << L.M[j])
                ins.append(k)
                yy = (y+m*cj) % N
                want.append((m << L.M[j]) | sum(((yy >> i) & 1) << L.F[i] for i in range(L.b)))
        assert [int(o) for o in classical_eval(ops_to_gates(ops, L.nq), L.nq, ins)] == want


@pytest.mark.parametrize("N,t", [(3, 4), (5, 6), (7, 7), (9, 8), (13, 8), (25, 9), (27, 10)])
def test_decoder_exhaustive(N, t):
    """Exact computation: K = round(l N / 2^t) mod N for every l, everything else clean."""
    L = make_layout(N, t)
    ops = decoder_ops(L)
    D = 2**t
    ins = [sum(((l >> i) & 1) << L.M[t-1-i] for i in range(t)) for l in range(D)]
    out = classical_eval(ops_to_gates(ops, L.nq), L.nq, ins)
    mask_mw = sum(1 << q for q in L.M)
    for l, o in zip(range(D), out):
        o = int(o)
        kt = ((l*N + D//2)//D) % N
        K = sum(((o >> q) & 1) << i for i, q in enumerate(L.K))
        assert K == kt
        W = sum(((o >> q) & 1) << i for i, q in enumerate(L.W))
        assert W == l*N + D//2
        rest = o & ~mask_mw & ~sum(1 << q for q in L.K) & ~sum(1 << q for q in L.W)
        assert rest == 0
    back = classical_eval(ops_to_gates(ops+ops.inverse(), L.nq), L.nq, ins)
    assert [int(b) for b in back] == ins


@pytest.mark.parametrize("N,tp", [(3, 6), (5, 10), (7, 4), (13, 12), (27, 8)])
def test_prep_error_equals_formula(N, tp):
    """Float check of the exact prep error formula 2 sin((pi/2 - 3 alpha~)/2)."""
    L = make_layout(N, 2)
    st = SparseState(L.nq, [0], tol=0.0).run(ops_to_gates(prep_ops(L, tp), L.nq))
    vec = {int(k): a for k, a in zip(st.key_ints(), st.amps)}
    ideal = {sum(((y >> i) & 1) << L.F[i] for i in range(L.b)): 1/math.sqrt(N) for y in range(N)}
    err = math.sqrt(sum(abs(vec.get(k, 0)-ideal.get(k, 0))**2 for k in set(vec) | set(ideal)))
    bd = error_bound(N, 4, 4, tp)
    assert abs(err-bd["prep"]) < 1e-9
    assert bd["prep"] <= bd["prep_linear_bound"]+1e-15 <= 3*math.pi/2**tp+1e-15


@pytest.mark.parametrize("N", NS)
def test_phase_numerators_and_bound(N):
    for tp in (3, 6, 10, 20):
        bd = error_bound(N, 6, 6, tp)
        assert bd["phase_max"] <= bd["phase_sum_bound"]+1e-12
        assert bd["phase_sum_bound"] <= ((N-1).bit_length())*math.pi/2**tp+1e-12
        assert all(0 <= c < 2**tp for c in phase_numerators(N, tp))


@pytest.mark.parametrize("N", NS)
def test_gate_count_formula_and_qubits(N):
    b = (N-1).bit_length()
    for t, r, tp in ((b+1, 2, 3), (b+4, 3, 8), (b+6, b+6, 12), (2*b+10, 9, 20)):
        ops, L, _ = qft_mod_ops(N, t, r, tp)
        c = gate_counts(ops)
        assert c["total"] <= gate_bound(b, t, r, tp)
        assert L.nq == 8*b+2*t+6
        assert c["max_k"] <= max(r, tp)


@pytest.mark.parametrize("N", NS)
def test_params_for_eta_meet_eta(N):
    for eta in (0.5, 1e-2, 1e-4, 1e-8):
        t, r, tp = params_for_eta(N, eta)
        bd = error_bound(N, t, r, tp)
        assert bd["B"] <= bd["B_simple"]+1e-12
        assert bd["B_simple"] <= eta


def test_pe_tail_float_below_bound():
    for N, t, r in ((3, 4, 4), (5, 7, 3), (7, 8, 8), (13, 9, 4)):
        bd = error_bound(N, t, r, 20)
        assert pe_tail_float(N, t, r) <= bd["pe_tail"]+bd["aqft"]+1e-12


def _check(N, t, r, tp, inverse=False):
    d = operator_error(N, t, r, tp, inverse=inverse, tol=1e-11)
    assert d["prune_err_max"] < 1e-6
    assert d["sigma_upper"] <= d["bound"]["B"]
    assert d["gates"]["total"] <= d["gate_bound"]
    return d


@pytest.mark.parametrize("N,t,r,tp", [(3, 3, 3, 4), (3, 6, 2, 8), (3, 8, 8, 12), (5, 5, 5, 6),
                                      (5, 8, 3, 10), (7, 7, 7, 8), (7, 9, 4, 14)])
def test_operator_error_fast(N, t, r, tp):
    _check(N, t, r, tp)


def test_operator_error_inverse_fast():
    _check(5, 7, 7, 12, inverse=True)


def test_circuit_registers_and_gate_names():
    qc, L = qft_mod_circuit(5, 6, 3, 8)
    assert qc.num_qubits == L.nq
    assert qc.qregs[0].name == "x" and qc.qregs[0].size == L.b
    assert set(qc.count_ops()) <= {"x", "cx", "ccx", "swap", "h", "p", "cp"}


@slow
@pytest.mark.parametrize("N,t,r,tp", [(9, 6, 6, 24), (9, 9, 4, 24), (11, 8, 8, 24), (11, 10, 5, 24),
                                      (13, 7, 7, 24), (13, 10, 4, 24), (25, 7, 7, 28), (25, 9, 5, 28),
                                      (27, 8, 8, 28), (27, 10, 4, 28), (9, 8, 8, 6), (13, 8, 8, 8)])
def test_operator_error_slow(N, t, r, tp):
    _check(N, t, r, tp)


def test_cuccaro_adder_exhaustive_small_widths():
    """Exact computation: (B, z) += A mod 2^(n+1), A and c0 restored, for all inputs, n <= 6."""
    from theorems.rees_circuit_arith import cuccaro_add
    for n in range(1, 7):
        A, B, c0, z = list(range(n)), list(range(n, 2*n)), 2*n, 2*n+1
        ops = QOps()
        cuccaro_add(ops, A, B, c0, z)
        ins, want = [], []
        for a in range(2**n):
            for bb in range(2**n):
                for zz in (0, 1):
                    ins.append(a | bb << n | zz << (2*n+1))
                    s = (bb + (zz << n) + a) % 2**(n+1)
                    want.append(a | (s % 2**n) << n | (s >> n) << (2*n+1))
        assert [int(o) for o in classical_eval(ops_to_gates(ops, 2*n+2), 2*n+2, ins)] == want


@pytest.mark.parametrize("N", NS)
def test_less_than_on_every_word(N):
    """Exact computation: out ^= [w < N] on every b-bit word w, ancillas restored."""
    from theorems.rees_circuit_arith import less_than_p
    L = make_layout(N, 2)
    A = Anc(L.anc, L.b)
    ops = QOps()
    less_than_p(ops, N, L.F, A, A.h)
    ins = [sum(((w >> i) & 1) << L.F[i] for i in range(L.b)) for w in range(2**L.b)]
    out = classical_eval(ops_to_gates(ops, L.nq), L.nq, ins)
    for w, k, o in zip(range(2**L.b), ins, out):
        assert int(o) == k | (int(w < N) << A.h)
