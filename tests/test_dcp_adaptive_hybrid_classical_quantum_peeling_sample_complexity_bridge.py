"""Native physical falsifiers, legal measurement competitors and erasure costs."""
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pytest

from theorems.dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_bridge import (
    erasure_fisher_accounting,
    evaluate_matched_branch_accounting,
    generate_dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_certificate,
    native_gate_plan,
    physical_packet_law,
    realized_effective_label,
)
from theorems.dcp_correlated_phase_block import density

ROOT = Path(__file__).resolve().parents[1]


def test_product_X_is_not_an_unattenuated_sum_frequency_measurement():
    row = physical_packet_law([[1, 1]], [1, 1], 3, 1, (2,))
    assert row["independent_X_parity_mean"] == pytest.approx(0, abs=1e-14)
    assert row["hypothetical_modular_sample_target_cosine_mean"] == pytest.approx(-1)
    assert row["random_even_XY_signed_parity_mean"] == pytest.approx(-.5)
    assert row["matched_flag_conditional_mean"] == pytest.approx(-1)
    assert row["matched_flag_probability"] == pytest.approx(.5)
    assert row["X_parity_is_target_cosine_counterexample"]


def test_realizable_Pauli_competitor_cannot_be_renamed_unattenuated_classical_samples():
    record = evaluate_matched_branch_accounting([[1, 1, 1]], [1, 1, 1], 3, Fraction(4, 5))
    assert record["p_match_up_to_sign_exact"] == "1/4"
    assert record["conditional_visibility_exact"] == "64/125"
    assert record["native_syndromes_enumerated"] == 4
    assert not record["classical_phase_bearing_modular_samples_supplied"]
    assert not record["classical_dominance_established"]
    assert "classical_dominates_or_equals_quantum" not in record
    assert "sample_complexity_inflation_factor" not in record
    accounting = record["flagged_vs_forgotten_accounting"]
    assert accounting["at_zero_cosine_flagged_acceptance_penalty"] == "4"
    assert accounting["at_zero_cosine_fair_coin_acceptance_penalty"] == "16"


@pytest.mark.parametrize("p,g,mu", [(Fraction(1, 4), Fraction(64, 125), Fraction(0)),
                                    (Fraction(1, 2), Fraction(3, 4), Fraction(1, 3)),
                                    (Fraction(1), Fraction(1), Fraction(-1, 2)),
                                    (Fraction(0), Fraction(3, 4), Fraction(0)),
                                    (Fraction(1, 4), Fraction(0), Fraction(0))])
def test_Fisher_costs_follow_the_actual_flagged_and_fair_coin_laws(p, g, mu):
    flagged = ((p*(1+g*mu)/2, p*g/2), (p*(1-g*mu)/2, -p*g/2), (1-p, 0))
    replaced = (((1+p*g*mu)/2, p*g/2), ((1-p*g*mu)/2, -p*g/2))
    actual_flagged = sum(derivative**2/mass for mass, derivative in flagged if mass)
    actual_replaced = sum(derivative**2/mass for mass, derivative in replaced if mass)
    row = erasure_fisher_accounting(p, g, target_cosine=mu)
    assert Fraction(row["flagged_local_Fisher_exact"]) == actual_flagged
    assert Fraction(row["fair_coin_replacement_local_Fisher_exact"]) == actual_replaced
    if not g or not p:
        assert row["flagged_inverse_local_Fisher_exact"] is None
    assert not row["discrete_secret_recovery_complexity_or_global_lower_bound"]


@pytest.mark.parametrize("A,v,t", [([[1, 1]], [1, 1], 3),
                                   ([[1, 2, 5], [3, 5, 7]], [1, 1, 1], 3),
                                   ([[1, 3, 5, 7]], [1, 0, 1, 1], 3)])
def test_every_secret_native_density_actual_CNOT_H_gates_and_all_Born_outcomes(A, v, t):
    h = sum(v)
    size, q = 1 << h, 1 << t
    selected = [[a for a, bit in zip(row, v) if bit] for row in A]
    # Independently construct the complete gate matrix, then read Z populations.
    cx = np.eye(size, dtype=complex)
    for j in range(1, h):
        gate = np.zeros((size, size), dtype=complex)
        for x in range(size):
            gate[x ^ ((x & 1) << j), x] = 1
        cx = gate@cx
    H = np.kron(np.eye(size//2), np.array([[1, 1], [1, -1]])/math.sqrt(2))
    circuit = H@cx
    for gamma in (Fraction(0), Fraction(1, 2), Fraction(1)):
        for secret in product(range(q), repeat=len(A)):
            original = density(selected, t, secret, gamma)
            probabilities = np.diag(circuit@original@circuit.conj().T).real
            row = physical_packet_law(A, v, t, gamma, secret)
            assert row["max_native_branch_law_residual"] < 2e-14
            assert row["separable_protocol_formula_residual"] < 2e-14
            assert row["matched_branch_formula_residual"] < 2e-14
            for branch in row["branches"]:
                d = branch["syndrome"]
                assert probabilities[2*d] == pytest.approx(branch["joint_X_plus_probability"], abs=2e-14)
                assert probabilities[2*d+1] == pytest.approx(branch["joint_X_minus_probability"], abs=2e-14)
                assert branch["probability"] == pytest.approx(1/(size//2))
            assert sum(probabilities) == pytest.approx(1)
            assert row["total_Born_probability"] == pytest.approx(1)
            assert not row["secret_used_to_choose_circuit_or_measurement"]


def test_even_XY_rule_is_an_actual_separable_Pauli_protocol():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    A, v, secret, gamma = [[1, 2, 5]], [1, 1, 1], (3,), Fraction(3, 4)
    rho = density(A, 3, secret, gamma)
    values = []
    for axes in product((0, 1), repeat=3):
        if sum(axes) % 2:
            continue
        operator = np.array([[1]], dtype=complex)
        for axis in reversed(axes):
            operator = np.kron(operator, Y if axis else X)
        values.append((-1)**(sum(axes)//2)*np.trace(rho@operator).real)
    record = physical_packet_law(A, v, 3, gamma, secret)
    assert record["random_even_XY_signed_parity_mean"] == pytest.approx(sum(values)/len(values))


def test_native_mod2_control_really_is_classical_but_does_not_transfer_to_mod8():
    for secret in (0, 1):
        row = physical_packet_law([[1, 1, 1]], [1, 1, 1], 1, Fraction(4, 5), (secret,))
        assert row["independent_X_parity_mean"] == pytest.approx(row["matched_flag_conditional_mean"])
        assert row["matched_flag_probability"] == pytest.approx(1)
    record = evaluate_matched_branch_accounting([[1, 1]], [1, 1], 1, 1)
    assert record["zero_target_is_secret_independent"]
    assert record["flagged_vs_forgotten_accounting"] is None


def test_realized_labels_agree_with_every_original_anchor_without_counting_idle_wires():
    A, v, t = [[3, 2, 5, 7, 4]], [1, 0, 1, 1, 0], 3
    support = [i for i, x in enumerate(v) if x]
    target = sum(A[0][i] for i in support) % 8
    hits = 0
    for bits in product((0, 1), repeat=5):
        actual = sum((1-2*bits[i])*A[0][i] for i in support) % 8
        syndrome = sum((bits[support[0]] ^ bits[j]) << k for k, j in enumerate(support[1:]))
        label = realized_effective_label(A, v, t, syndrome)[0]
        assert actual == ((1-2*bits[support[0]])*label) % 8
        hits += actual in (target, -target % 8)
    record = evaluate_matched_branch_accounting(A, v, t, 1)
    assert Fraction(hits, 32) == Fraction(record["p_match_up_to_sign_exact"])
    assert record["native_syndromes_enumerated"] == 4


def test_circuit_is_linear_size_and_needs_no_exponential_branch_table():
    A, v = [[1]*64], [1]*64
    plan = native_gate_plan(A, v, 128, Fraction(99, 100))
    assert len(plan["gates"]) == 64
    assert plan["source_phase_qubits_consumed_per_packet"] == 64
    assert not plan["full_exponential_syndrome_table_needed_by_circuit"]
    assert len(realized_effective_label(A, v, 128, 0)) == 1
    with pytest.raises(ValueError, match="calibration cap"):
        evaluate_matched_branch_accounting(A, v, 128, 1)


@pytest.mark.parametrize("A,v,t,g", [([], [1], 3, 1), ([[1]], [0], 3, 1),
                                      ([[8]], [1], 3, 1), ([[1]], [2], 3, 1),
                                      ([[1]], [1], True, 1), ([[1]], [1], 3, Fraction(3, 2))])
def test_invalid_access_models_rejected(A, v, t, g):
    with pytest.raises(ValueError):
        native_gate_plan(A, v, t, g)


def test_certificate_and_reduction_artifact_match():
    cert = generate_dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_certificate()
    assert cert["all_checks_passed"]
    assert cert["v1_classical_dominance_and_16x_sample_penalty_retracted"]
    on_disk = json.loads((ROOT/"research/reductions"/(cert["theorem_id"]+".json")).read_text())
    assert cert == on_disk


def test_nodejs_independent_counterexample():
    script = ROOT/"research/certificates/dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_bridge_crosscheck.js"
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    assert json.loads(proc.stdout)["status"] == "OK"
