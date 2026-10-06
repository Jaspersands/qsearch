from fractions import Fraction
from itertools import product
import json
import math

import numpy as np
import pytest

from dcp_projective_code_admission import (
    block_rows, code_distribution, code_signal_certificate, native_pauli_signature,
    physical_control, run_controls, sq_gate, validate_code,
)


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_actual_purified_commuting_pauli_readouts_match_full_likelihood(report):
    assert len(report["physical_controls"]) == 12
    for r in report["physical_controls"]:
        assert r["joint_state_norm"] == pytest.approx(1)
        assert r["output_norm"] == pytest.approx(1)
        assert min(r["full_output_probabilities"]) > -1e-12
        assert r["maximum_probability_identity_error"] < 1e-12
        assert r["source_qubits_consumed"] == len(r["native_labels"])
        assert not r["postselection_or_cloning_used"]


def test_stabilizer_output_loses_odd_secret_but_full_native_measurement_does_not(report):
    signatures = report["odd_secret_signature_controls"]
    assert all(r["all_public_label_signature"] == signatures[0]["all_public_label_signature"] for r in signatures)
    positive = 0
    for first, second in zip(report["physical_controls"][::2], report["physical_controls"][1::2]):
        assert first["native_pauli_signature"] == second["native_pauli_signature"]
        if np.max(abs(np.array(first["full_output_probabilities"])-second["full_output_probabilities"])) > 1e-3:
            positive += 1
    assert positive >= 3


def test_noncentral_dihedral_commutator_cannot_be_cancelled_as_scalar_cocycle():
    X = np.array([[0, 1], [1, 0]], complex)
    for N in (8, 16, 32):
        scalar_count = 0
        for k in range(N):
            z = np.exp(2j*math.pi*k/N)
            R = np.diag([z, z.conjugate()])
            commutator = R @ X @ R.conj().T @ X
            scalar = np.max(abs(commutator-np.eye(2)*commutator[0, 0])) < 1e-12
            assert scalar == (4*k % N == 0)
            scalar_count += scalar
        assert scalar_count == 4


def test_tensor_pauli_signature_matches_actual_pure_state_expectations():
    Z, X = np.diag([1, -1]), np.array([[0, 1], [1, 0]])
    for N in (8, 16):
        for s in range(N):
            for k in range(N):
                state = np.array([1, np.exp(2j*math.pi*k*s/N)])/math.sqrt(2)
                signature = native_pauli_signature(N, s, [k])[0]
                assert (abs(np.vdot(state, X @ state)) > 1-1e-12) == (signature == "X")
                assert (abs(np.vdot(state, Z @ X @ state)) > 1-1e-12) == (signature == "ZX")


def test_linear_two_copy_representation_is_not_automatically_bose_phase_neutral():
    # Same supplied +Y state: (ZX)^tensor2 eigenvalue -1, tensor4 +1.
    two, _ = code_distribution([[1, 1]], 8, 1, [2, 2])
    four, _ = code_distribution([[1, 1, 1, 1]], 8, 1, [2]*4)
    assert not validate_code([[1, 1]])[3]["basis_rows_doubly_even"]
    assert validate_code([[1]*4])[3]["basis_rows_doubly_even"]
    assert np.max(abs(two-four)) > .4
    assert sum(two) == pytest.approx(1)
    assert sum(four) == pytest.approx(1)


@pytest.mark.parametrize("block", [2, 4])
def test_disjoint_repetition_code_kernel_is_exact_and_bell_bound_saturates_only_pairs(block):
    for h in range(1, 5):
        r = code_signal_certificate(block_rows(block, h))
        expected = (1+Fraction(2, 2**block))**h
        assert exact(r["source_averaged_full_collision_kernel"]) == expected
        assert expected <= Fraction(3, 2)**h
        assert (expected == Fraction(3, 2)**h) == (block == 2)


def test_hamming_code_signal_is_not_mistaken_for_more_research_leverage(report):
    r = next(r for r in report["physical_controls"] if r["code_name"] == "extended-hamming-eight")["certificate"]
    assert r["logical_rows"] == 4
    assert exact(r["source_averaged_centered_chi_squared"]) == Fraction(29, 16)
    assert exact(r["matched_logical_row_bell_kernel"])-1 == Fraction(65, 16)
    assert not r["full_transcript_or_classical_time_dominance_proved"]


def test_individual_measurement_baseline_is_stronger_on_this_metric_but_not_a_simulator(report):
    for r in report["physical_controls"]:
        c = r["certificate"]
        h = c["logical_rows"]
        assert exact(c["matched_output_bit_individual_X_kernel"]) == Fraction(3, 2)**(2*h)
        assert c["individual_X_native_qubits"] <= c["consumed_native_phase_qubits"]
        assert exact(c["matched_output_bit_individual_X_kernel"]) >= exact(c["source_averaged_full_collision_kernel"])
        assert not c["individual_X_baseline_is_full_classical_phase_state_simulator"]


def test_full_source_cross_kernel_by_exhaustive_native_labels_not_hidden_label_average():
    for rows, N in (([[1, 1]], 16), ([[1, 1, 1, 1]], 8)):
        same, other = 0.0, 0.0
        count = N**len(rows[0])
        for labels in product(range(N), repeat=len(rows[0])):
            p, _ = code_distribution(rows, N, 1, labels)
            q, _ = code_distribution(rows, N, 3, labels)
            same += len(p)*np.dot(p, p)/count
            other += len(p)*np.dot(p, q)/count
        assert same == pytest.approx(float(exact(code_signal_certificate(rows)["source_averaged_full_collision_kernel"])))
        assert other == pytest.approx(1)


def test_every_small_full_rank_self_orthogonal_code_obeys_systematic_tail_bound():
    # All two-row codes at width6, not just handpicked named codes.
    for x in range(1, 64):
        if x.bit_count() % 2:
            continue
        for y in range(x+1, 64):
            if y.bit_count() % 2 or (x & y).bit_count() % 2:
                continue
            rows = [[(mask >> i) & 1 for i in range(6)] for mask in (x, y)]
            r = code_signal_certificate(rows)
            assert r["tail_rank"] == 2
            assert exact(r["source_averaged_full_collision_kernel"]) <= Fraction(9, 4)


def test_sq_gate_is_scoped_and_can_become_vacuous_as_measurement_dimension_grows(report):
    last = report["scaling_ledgers"][-1]["sq_gate"]
    assert exact(last["uniform_orbit_identification_success_upper"]) < Fraction(1, 10**25)
    assert not last["raw_sample_or_multirecord_inference_covered"]
    assert not last["source_label_adaptive_measurement_covered"]
    assert exact(sq_gate(2**32, 128, 1, Fraction(1, 32))["uniform_orbit_identification_success_upper"]) == 1


def test_worst_gap_does_not_get_reported_as_typical_hardness(report):
    for r in report["scaling_ledgers"]:
        N = 2**r["modulus_bits"]
        assert exact(r["odd_secret_single_state_worst_gap_upper"]) == Fraction(20, N*N)
        assert r["worst_gap_not_a_typical_packet_claim"]
        assert exact(r["native_scalar_commutator_label_fraction"]) == Fraction(4, N)


def test_no_signal_metric_is_promoted_to_runtime_dominance_or_generic_no_go(report):
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))
    for r in report["physical_controls"]:
        assert not r["certificate"]["label_adaptive_code_moment_covered"]
        assert not r["certificate"]["raw_sample_algorithms_excluded"]


def test_quantum_remainder_refutes_protocol_dominance_from_classical_moments(report):
    bell, quartic, *overlapping = report["retained_quantum_register_countercontrols"]
    assert bell["actual_remaining_encoded_qubits"] == 0
    assert quartic["actual_remaining_encoded_qubits"] == 2
    assert bell["classical_full_output_total_variation"] < 1e-12
    assert quartic["classical_full_output_total_variation"] < 1e-12
    assert bell["classical_and_retained_quantum_output_trace_distance"] < 1e-7
    assert quartic["classical_and_retained_quantum_output_trace_distance"] < 1e-12
    assert bell["all_ones_in_code"] and quartic["all_ones_in_code"]
    assert len(overlapping) == 8
    assert {r["unfiltered_label_seed"] for r in overlapping} == set(range(43011, 43019))
    assert all(not r["all_ones_in_code"] and r["actual_remaining_encoded_qubits"] == 2 for r in overlapping)
    assert all(r["classical_full_output_total_variation"] < 1e-12 for r in overlapping)
    assert sum(r["classical_and_retained_quantum_output_trace_distance"] > .1 for r in overlapping) >= 1
    assert quartic["all_classical_branches_retained"]
    assert not quartic["conditional_normalization_used"]
    for r in report["retained_quantum_register_countercontrols"]:
        assert r["classical_and_retained_quantum_output_trace_distance"] <= r["original_native_input_trace_distance"]+1e-12
    for r in report["physical_controls"]:
        c = r["certificate"]
        multiplier = 1 << c["unmeasured_logical_qubits"]
        assert exact(c["retained_register_source_quantum_collision"]) == multiplier*exact(c["source_averaged_full_collision_kernel"])
        assert exact(c["retained_register_source_quantum_collision"]) <= int(c["untouched_native_source_quantum_collision"])
        assert not c["retained_quantum_register_algorithms_covered_by_bell_ceiling"]


def test_overlapping_six_to_two_logical_branch_has_paid_nonlinear_amplitudes(report):
    rows = report["overlapping_native_logical_branch_controls"]
    assert len(rows) == 8
    for r in rows:
        assert r["full_formula_error"] < 1e-12
        amplitude = [complex(*x) for x in r["unnormalized_logical_amplitudes"]]
        assert sum(abs(x)**2 for x in amplitude) == pytest.approx(r["zero_branch_probability"])
        assert r["native_source_qubits"] == 6 and r["retained_logical_qubits"] == 2
        assert r["all_other_measurement_branches_retained_in_parent_countercontrol"]
        assert not r["conditional_success_without_branch_cost_claim"]


@pytest.mark.parametrize("callback", [lambda: validate_code([[0, 0]]), lambda: validate_code([[1, 0]]),
    lambda: validate_code([[1, 1], [1, 1]]), lambda: validate_code([[True, True]]),
    lambda: code_distribution([[1, 1]], 8, 1, [0]), lambda: native_pauli_signature(9, 1, [0]),
    lambda: sq_gate(8, 1, 1, .1), lambda: physical_control("too-large", block_rows(2, 5), 8, 1, [0]*10)])
def test_invalid_nonpreserving_or_unbounded_controls_are_rejected(callback):
    with pytest.raises(ValueError):
        callback()
