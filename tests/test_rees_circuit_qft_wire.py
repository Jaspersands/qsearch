"""Tests for theorems/rees_circuit_qft_wire.py: the explicit QFT over Z/p of
lem:qft-mod as an optional backend of the gate-level Rees circuit generator.
AI-checked, pending human review. Small parameters keep the run under a minute."""
import numpy as np
import pytest
from qiskit.circuit import CircuitInstruction
from qiskit.circuit.library import PhaseGate

import theorems.rees_circuit_arith as A
import theorems.rees_circuit_general as G
import theorems.rees_circuit_qft_wire as W
import theorems.rees_qft_mod as Q
from theorems.rees_end_to_end_sim import filiform4, heisenberg

HEIS = G.Config(heisenberg(3))
SMALL = (5, 5, 20)


def test_status_gates_stay_false():
    for k in ("coherent_receiver_implemented", "general_sde_implemented", "formal_compiler_checked",
              "independent_review", "novelty_established", "speedup_claim_allowed", "fixed_finite_gate_set",
              "monolithic_explicit_simulation"):
        assert W.WIRE_STATUS[k] is False
    assert A.ARITH_STATUS["qft_poly_log_p_implemented"] is False      # other modules untouched
    assert Q.STATUS["rees_generator_uses_this_qft"] is False


def _sig(qc):
    return [(i.operation.name, tuple(qc.find_bit(q).index for q in i.qubits)) for i in qc.data]


def test_default_backend_is_the_original_generator_and_is_restored():
    before = (G.Builder, G.check_macros)
    qc0, _ = G.terminal_sample_circuit(HEIS)
    qc1, _ = W.terminal_sample_circuit(HEIS, arith=False)
    assert _sig(qc0) == _sig(qc1) and qc0.num_qubits == qc1.num_qubits == 82
    with W.explicit_qft_backend(SMALL):
        assert G.Builder is not before[0]
    assert (G.Builder, G.check_macros) == before
    qc2, _ = G.terminal_sample_circuit(HEIS)
    assert _sig(qc2) == _sig(qc0)


def test_explicit_terminal_sample_structure_and_counts():
    qc, B = W.terminal_sample_circuit(HEIS, qft="explicit", params=SMALL)
    W.check_macros_qft(qc, B)
    qce, Be = W.terminal_sample_circuit(HEIS)
    ops, L = W.reference_ops(3, *SMALL)
    assert qc.num_qubits == qce.num_qubits+W.pool_size(2, SMALL[0])
    c = W.circuit_counts(qc, B)
    assert c["qft_calls"] == 24 and c["qft_gates"] == 24*len(ops)
    assert c["arith_gates"] == W.circuit_counts(qce, Be)["arith_gates"]
    names = {i.operation.name for i in qc.data}
    assert names <= {"x", "cx", "ccx", "swap", "h", "p", "cp", "U_f", "measure"}
    calls = W.qft_call_inputs(qc, B)
    assert sum(z for _, _, z in calls) == 18 and len(calls) == 24
    assert len(ops) <= Q.gate_bound(2, *SMALL)


def test_counting_mode_and_fresh_pool():
    qc, B = W.terminal_sample_circuit(HEIS, qft="explicit", params=SMALL)
    qcc, Bc = W.terminal_sample_circuit(HEIS, qft="explicit", params=SMALL, count_only=True)
    a, b = W.circuit_counts(qc, B), W.circuit_counts(qcc, Bc)
    assert {k: a[k] for k in ("qft_gates", "arith_gates", "qubits")} == {k: b[k] for k in ("qft_gates", "arith_gates", "qubits")}
    qcf, Bf = W.terminal_sample_circuit(HEIS, qft="explicit", params=SMALL, pool="fresh")
    W.check_macros_qft(qcf, Bf)
    assert qcf.num_qubits == qc.num_qubits+23*W.pool_size(2, SMALL[0])


def test_negative_corrupted_qft_slice_is_rejected():
    qc, B = W.build(G.fourier_circuit, HEIS, 1, "qft_final", qft="explicit", params=SMALL)
    W.check_macros_qft(qc, B)
    _, _, _, start, end = B.macros[0]
    k = next(i for i in range(start, end) if qc.data[i].operation.name == "p")
    inst = qc.data[k]
    qc.data[k] = CircuitInstruction(PhaseGate(float(inst.operation.params[0])+1e-3), inst.qubits)
    with pytest.raises(AssertionError):
        W.check_macros_qft(qc, B)
    qc.data[k] = inst
    qc.data[k+1], qc.data[k] = qc.data[k], qc.data[k+1]
    if _sig_one(qc.data[k]) != _sig_one(qc.data[k+1]):
        with pytest.raises(AssertionError):
            W.check_macros_qft(qc, B)


def _sig_one(inst):
    return (inst.operation.name, tuple(inst.qubits), tuple(float(x) for x in inst.operation.params))


def test_per_call_operator_error_within_the_proved_bound():
    qc, B, _ = W.build(G.instrument_circuit, HEIS, 2, qft="explicit", params=SMALL)
    W.check_macros_qft(qc, B)
    bd = Q.error_bound(3, *SMALL)
    for m in B.macros:
        if m[0] in ("qft", "qft_dg"):
            r = W.call_operator_error(qc, B, m)
            assert r["sigma_upper"] <= bd["B"]
            if m[0] == "qft":       # input |0>: only the prep error remains (report, Section 4)
                assert abs(r["column_errors"][0]-bd["prep"]) < 1e-9


def test_simulator_reproduces_the_exact_source_permutation():
    inst = G.heis3_instances()[3]
    qc, B, (a_reg, a, w_reg, w, labels) = G.source_circuit(HEIS, inst)
    st = W.simulate_prefix(qc, tol=0.0)
    assert len(st.amps) == 81 and np.allclose(np.abs(st.amps), 1/9)
    pos = {q: i for i, q in enumerate(qc.qubits)}
    X = HEIS.laws[2].elements()
    sim = G.BitSim(qc.num_qubits, len(X))
    sim.load(G.wires_of(a, pos), X)
    sim.run(G.compile_ops(qc.data[len(a):], pos))
    want = set()
    for n in range(len(X)):
        key = 0
        for i in range(qc.num_qubits):
            key |= int(sim._unpack(i)[n]) << i
        want.add(key)
    assert set(int(k) for k in st.key_ints()) == want


def test_instrument_block_explicit_vs_exact():
    r = W.instrument_block_error(HEIS, 2, SMALL)
    assert r["inputs"] == 3
    assert r["max_state_distance"] <= r["hybrid"]["proved_total"]+r["prune_err_max"]


def test_terminal_sample_prefixes_explicit_vs_exact():
    inst = G.heis3_instances()[1]
    src = W.compare_prefix(HEIS, inst, SMALL, end_fn=W.source_prefix_end)
    assert src["hybrid"]["calls"] == {"qft_zero": 4}
    assert src["state_distance"] <= src["hybrid"]["proved_total"]+src["prune_err_explicit"]
    seg = W.compare_prefix(HEIS, inst, SMALL)
    assert seg["hybrid"]["calls"] == {"qft_dg_general": 1, "qft_zero": 5}
    assert seg["state_distance"] <= seg["hybrid"]["proved_total"]+seg["prune_err_explicit"]
    assert seg["label_tv"] <= seg["state_distance"]+seg["prune_err_explicit"]
    assert abs(sum(seg["label_law_exact"].values())-1) < 1e-9


def test_hybrid_and_coupling_bounds_are_monotone_in_eta():
    qc, B = W.terminal_sample_circuit(HEIS)
    calls = W.qft_call_inputs(qc, B)
    prev = None
    for eta in (0.25, 0.05, 0.01):
        t, r, tp = Q.params_for_eta(3, eta)
        bud = W.hybrid_budget(calls, 3, t, min(r, t), tp)["proved_total"]
        assert bud <= 24*eta
        if prev is not None:
            assert bud < prev
        prev = bud
    assert W.coupling_bound(0.5, 7) == 1.0


def test_n4_f5_explicit_counts():
    cfg = G.Config(filiform4(5))
    c = W.terminal_counts(cfg, "explicit", params=(8, 8, 28))
    assert c["qft_calls"] == 148 and c["zero_input_calls"] == {"zero": 124, "general": 24}
    ops, _ = W.reference_ops(5, 8, 8, 28)
    assert c["qft_gates"] == 148*len(ops) and c["pool_qubits"] == W.pool_size(3, 8)
