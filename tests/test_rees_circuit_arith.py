"""Tests for theorems/rees_circuit_arith.py (poly(log p) binary arithmetic backend
for the gate-level Rees circuit generator). Fast tests take about a minute;
the full n4(F_5) backend comparison and the large-p sampled runs are slow
(REES_SLOW=1)."""
import os

import numpy as np
import pytest
from qiskit.circuit import CircuitInstruction
from qiskit.circuit.library import XGate

import theorems.rees_circuit_general as G
import theorems.rees_circuit_sparse as S
from theorems.rees_circuit_arith import (
    ARITH_STATUS, ArithBuilder, CountingArithBuilder, anc_size, arith_backend, arith_gate_counts,
    check_macros_arith, compare_backends, count_config, exhaustive_macro_check, formula_counts, macro_circuit,
    merge_bitlevel_arith, multiplication_counts, primitive_checks, sampled_macro_check, sampled_merge_check,
)
from theorems.rees_end_to_end_sim import filiform4, filiform5, heisenberg

slow = pytest.mark.skipif(os.environ.get("REES_SLOW") != "1", reason="slow; set REES_SLOW=1")
PRIMES = (3, 5, 7, 11, 13)


def test_status_gates_stay_false():
    for k in ("coherent_receiver_implemented", "general_sde_implemented", "formal_compiler_checked",
              "independent_review", "novelty_established", "speedup_claim_allowed", "qft_poly_log_p_implemented"):
        assert ARITH_STATUS[k] is False


def test_builder_is_restored_after_the_context():
    before = (G.Builder, G.check_macros, G.instrument_semantics, S.instrument_semantics)
    with arith_backend():
        assert G.Builder is ArithBuilder
    assert (G.Builder, G.check_macros, G.instrument_semantics, S.instrument_semantics) == before


# ---------------------------------------------------------------- exhaustive macro checks

@pytest.mark.parametrize("p", PRIMES)
def test_primitives_exhaustive(p):
    out = primitive_checks(p)
    assert out["ok"], out


@pytest.mark.parametrize("p", PRIMES)
def test_every_macro_every_coefficient_all_words(p):
    rows = exhaustive_macro_check(p)
    assert len(rows) == 2*(p-1)
    for r in rows:
        assert r["ok"], r
        assert r["canonical_inputs"] == p**(2 if r["kind"] == "add_scaled" else 3)


def test_only_x_cx_ccx_swap_are_emitted():
    for kind in ("add_scaled", "add_product"):
        qc, B, _ = macro_circuit(7, kind, 3)
        assert {inst.operation.name for inst in qc.data} <= {"x", "cx", "ccx", "swap"}
        assert qc.num_ancillas == anc_size(3)


def test_value_controlled_increment_is_not_offered():
    qc, B, (t, a) = macro_circuit(5, "add_scaled", 1)
    with pytest.raises(NotImplementedError):
        B.increment(t, 1, [(a, 2)])


# ---------------------------------------------------------------- negative controls

def test_negative_corrupted_macro_slice_is_rejected():
    with arith_backend():
        qc, B, _ = G.merge_circuit(G.Config(filiform4(5)), 3, 1)
    start, end = next(m[3:] for m in B.macros if m[0] == "add_scaled")
    i = next(j for j in range((start+end)//2, end) if qc.data[j].operation.name == "ccx")
    qc.data[i] = CircuitInstruction(XGate(), (qc.data[i].qubits[-1],))
    with pytest.raises(ArithmeticError):
        check_macros_arith(qc, B)


def test_negative_dropped_gate_leaves_ancilla_dirty_or_wrong():
    qc, B, qds = macro_circuit(5, "add_product", 2)
    del qc.data[len(qc.data)//2]
    kind, q, c, s, e = B.macros[0]
    B.macros[0] = (kind, q, c, s, e-1)
    with pytest.raises(ArithmeticError):
        check_macros_arith(qc, B)


def test_negative_original_check_cannot_see_the_ancillas():
    """Why check_macros is rebound: the original has no wires for the ancilla register."""
    with arith_backend():
        qc, B, _ = G.merge_circuit(G.Config(heisenberg(3)), 2, 1)
    assert G.check_macros is not check_macros_arith
    with pytest.raises(KeyError):
        G.check_macros(qc, B)


# ---------------------------------------------------------------- integration

@pytest.mark.parametrize("alg", [heisenberg(3), filiform4(5)], ids=["heis_f3", "n4_f5"])
def test_merges_proved_with_new_backend(alg):
    cfg = G.Config(alg)
    with arith_backend():
        for d in range(2, cfg.c+1):
            for s in range(1, cfg.p):
                flags = G.prove_merge(cfg, d, s)
                assert flags["proved"], (d, s, flags)


def test_heis_bitlevel_perm_equals_old_and_ancilla_clean():
    cfg = G.Config(heisenberg(3))
    for s in (1, 2):
        perm_old, _ = G.merge_bitlevel(cfg, 2, s)
        with arith_backend():
            perm_new, flags = merge_bitlevel_arith(cfg, 2, s)
        assert np.array_equal(perm_old, perm_new)
        assert all(v for k, v in flags.items() if k != "inputs"), flags


def test_instrument_kernels_equal_old():
    for alg in (heisenberg(3), filiform4(5)):
        cfg = G.Config(alg)
        old = G.Engine(cfg).kernels
        with arith_backend():
            new = G.Engine(cfg).kernels
        for d in old:
            assert new[d][1]["ok"]
            assert all(np.array_equal(x, y) for x, y in zip(old[d][0], new[d][0]))


def test_heis_f3_sparse_backends_agree_state_by_state():
    rec = compare_backends("heis_f3", log=lambda *a: None)
    assert len(rec["instances"]) == 19
    for k in ("all_merges_proved_new", "all_bitlevel_new_ok", "all_bitlevel_perm_equal_old",
              "all_instances_equal", "all_runs_recover_new"):
        assert rec[k], k


def test_n4_f5_one_subgroup_dense_and_sparse_with_new_backend():
    cfg = G.Config(filiform4(5))
    inst = next(i for i in G.n4_instances(5) if i.name.endswith("<e2> non-normal"))
    with arith_backend():
        sparse = S.SparseEngine(cfg, chunk=4096)
        row = S.check_instance_sparse(cfg, inst, sparse, max_cases=400, sample_tuples=3)
        got, info = S.run_algorithm_sparse(cfg, inst, sparse, seed=20261103)
    assert row["passed"] and row["source_workspace_clean"]
    assert info["recovered"]


# ---------------------------------------------------------------- gate counts

def test_counting_mode_equals_full_emission():
    for p in (11, 101):
        cfg = count_config(filiform4(p))
        for d in (2, 3):
            with arith_backend(CountingArithBuilder):
                _, Bc, _ = G.merge_circuit(cfg, d, 1)
            with arith_backend():
                qc, Bf, _ = G.merge_circuit(cfg, d, 1)
            assert arith_gate_counts(Bc) == arith_gate_counts(Bf)
            assert Bc._n == len(qc.data)
            assert [m[2:] for m in Bc.macros] == [m[2:] for m in Bf.macros]


@pytest.mark.parametrize("p", [3, 5, 101, 1031, 65537, 2**61-1])
def test_toffoli_count_of_a_multiplication_is_40b2_plus_2b(p):
    b = (p-1).bit_length()
    mc = multiplication_counts(p)
    assert all(r["ccx"] == 40*b*b+2*b for r in mc["add_product"]["rows"])
    assert mc["add_product"]["max_total"] <= 158*b*b+46*b-4    # quadratic in b = ceil(log2 p)


@pytest.mark.parametrize("p", [3, 7, 13, 101, 1031, 65537, 1000003, 2**31-1, 2**61-1])
def test_counted_gates_equal_the_closed_form(p):
    mc = multiplication_counts(p, seed=p)
    for kind in ("add_scaled", "add_product"):
        for r in mc[kind]["rows"]:
            f = formula_counts(p, r["coeff"])
            assert (r["arith_total"], r["ccx"]) == (f[kind+"_total"], f[kind+"_ccx"])
            assert r["arith_total"] <= f[kind+"_bound"]


# ---------------------------------------------------------------- slow

@slow
def test_slow_n4_f5_sparse_backends_agree_state_by_state():
    rec = compare_backends("n4_f5", log=lambda *a: None)
    assert len(rec["instances"]) == 9
    for k in ("all_merges_proved_new", "all_bitlevel_new_ok", "all_bitlevel_perm_equal_old",
              "all_instances_equal", "all_runs_recover_new"):
        assert rec[k], k


@slow
@pytest.mark.parametrize("p", [101, 1031, 65537, 2**61-1])
def test_slow_sampled_macros_large_p(p):
    for r in sampled_macro_check(p, n=512, n_coeffs=1):
        assert r["map_ok"] and r["ancilla_clean"], r


@slow
def test_slow_sampled_merge_n4_f101():
    flags = sampled_merge_check(filiform4(101), 3, 1, rows=2, xs=256)
    assert all(v for k, v in flags.items() if k not in ("inputs", "algebra", "d", "s")), flags
