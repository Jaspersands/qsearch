from fractions import Fraction
import json
import math

import numpy as np
import pytest

from singer_residual_hardness import singer_parameters
from singer_shor_access_closure import (
    _clean_membership_phase, _known_log_table, access_ledger,
    coherent_error_budget, physical_control, public_field, rotation_success,
    run_controls,
)


def exact(record):
    return Fraction(int(record["numerator"]), int(record["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_full_physical_readout_matches_exact_rotations_without_postselection(report):
    assert len(report["physical_controls"]) == 12
    assert sum(len(r["branches"]) for r in report["physical_controls"]) == 38
    for r in report["physical_controls"]:
        q = r["base_prime"]
        assert r["maximum_executed_cleanup_leakage"] < 1e-25
        for b in r["branches"]:
            expected = exact(b["exact_nonzero_fourier_success"])
            assert b["executed_shift_success"] == pytest.approx(float(expected), abs=1e-13)
            assert b["zero_output_failure"] == pytest.approx(float(1-expected), abs=1e-13)
            assert b["total_probability"] == pytest.approx(1)
            assert b["off_annihilator_probability"] < 1e-25
            assert b["unknown_xor_oracle_calls"] == b["grover_steps"]
            assert b["known_dlog_compute_or_uncompute_calls"] == 2*b["grover_steps"]
            assert not b["postselection_or_failure_renormalization"]
            for y in r["annihilator_coordinate_indices"][1:]:
                assert b["all_output_probabilities"][y] == pytest.approx(float(expected)/(q-1), abs=1e-13)
                assert r["decoded_shift_by_fourier_coordinate"][y] == int(r["hidden_shift_calibration"])


@pytest.mark.parametrize("q,m", [(2, 3), (3, 2), (5, 2)])
def test_all_small_shifts_are_retained_and_decoded_with_public_pairing(q, m):
    for shift in range(singer_parameters(q, m)[0]):
        r = physical_control(q, m, shift)
        assert exact(r["exact_schedule_mean_success"]) >= Fraction(1, 4)
        for b in r["branches"]:
            assert b["executed_shift_success"] == pytest.approx(float(rotation_success(q, b["grover_steps"])))


def test_one_binary_query_becomes_bernstein_vazirani_after_paid_coordinate_conversion(report):
    for r in report["physical_controls"]:
        if r["base_prime"] == 2:
            assert r["branches"][0]["zero_output_failure"] == pytest.approx(1)
            assert r["branches"][1]["executed_shift_success"] == pytest.approx(1)
            assert r["branches"][1]["known_dlog_compute_or_uncompute_calls"] == 2
            assert not r["actual_coherent_Shor_implementation"]


def test_uncomputed_workspace_is_essential_and_dual_coordinates_are_not_raw_field_coordinates(report):
    counterexamples = 0
    for r in report["physical_controls"]:
        q, m = r["base_prime"], r["extension_degree"]
        for b in r["branches"]:
            assert b["discarded_injective_log_workspace_fourier_success"] == pytest.approx((q-1)/q**m)
            if b["executed_shift_success"] > b["incorrect_dual_basis_decoder_success"]+0.1:
                counterexamples += 1
    assert counterexamples >= 4


def test_clean_marker_uses_plus_target_at_zero_and_one_xor_even_for_arbitrary_source_bit():
    K, alpha, _ = public_field(3, 2)
    logs = _known_log_table(K, alpha)
    v = singer_parameters(3, 2)[0]
    state = np.array([complex(i, 9-i) for i in range(9)])
    state /= np.linalg.norm(state)
    for source in ([0]*v, [1]*v, [int(i % 2) for i in range(v)]):
        out, leak = _clean_membership_phase(state, logs, source, v)
        expected = state.copy()
        expected[0] *= -1
        for x in range(1, len(state)):
            expected[x] *= (-1)**source[int(logs[x] % v)]
        assert np.max(abs(out-expected)) < 1e-14
        assert leak < 1e-26


def test_discarded_workspace_countercontrol_executes_a_partial_trace_not_a_pure_state():
    from singer_shor_access_closure import _additive_qft
    q, m = 3, 3
    K, alpha, _ = public_field(q, m)
    logs = _known_log_table(K, alpha)
    size, v = q**m, singer_parameters(q, m)[0]
    beta = alpha**4
    source = [int((beta*alpha**k).trace() == 0) for k in range(v)]
    uniform = np.ones(size)/math.sqrt(size)
    phase, _ = _clean_membership_phase(uniform, logs, source, v)
    state = 2*uniform*np.vdot(uniform, phase)-phase
    joint = np.zeros((size, size), complex)
    joint[np.arange(size), logs] = state
    reduced = joint @ joint.conj().T
    assert np.max(abs(reduced-np.diag(abs(state)**2))) < 1e-14
    F = np.column_stack([_additive_qft(e, q, m) for e in np.eye(size)])
    measured = np.diag(F @ reduced @ F.conj().T).real
    assert np.max(abs(measured-1/size)) < 1e-14
    assert sum(abs(_additive_qft(state, q, m))[1:]**2) > .8


def test_exact_randomized_schedule_bound_for_all_bounded_base_orders():
    for q in range(2, 129):
        # Rotation identity holds for any q even without a field promise.
        J = math.isqrt(q*q//(q-1))
        if J*J*(q-1) < q*q:
            J += 1
        mean = sum((rotation_success(q, j) for j in range(J)), Fraction(0))/J
        assert mean >= Fraction(1, 4)


def test_large_q_ledgers_have_exact_sqrt_query_cost_not_polynomial_bit_cost(report):
    for r in report["growing_base_field_ledgers"]:
        q, J = int(r["base_order"]), int(r["random_steps_exclusive_upper"])
        assert J*J*(q-1) >= q*q
        assert (J-1)**2*(q-1) < q*q
        assert int(r["max_total_membership_queries"]) == 16*(J-1)
        assert exact(r["ideal_all_attempts_fail_upper"]) == Fraction(3, 4)**16
        assert not r["total_runtime_polynomial_in_input_without_q_restriction"]
        error = r["coherent_error_budget"]
        Q = int(error["membership_phase_queries"])
        epsilon = exact(error["per_underlying_known_dlog_computation_failure_upper"])
        assert 16*Q*Q*epsilon == Fraction(1, 1000)**2
    assert int(report["growing_base_field_ledgers"][-1]["max_total_membership_queries"]) > 2**64


def test_integer_rotation_matches_trigonometric_controls():
    for q in (2, 3, 5, 7, 13, 127):
        for steps in range(10):
            assert float(rotation_success(q, steps)) == pytest.approx(math.sin(2*steps*math.asin(1/math.sqrt(q)))**2, abs=2e-14)


def test_no_table_is_promoted_to_known_shor_compiler_or_new_algorithm(report):
    roundtrip = json.loads(json.dumps(report, allow_nan=False))
    assert not any(roundtrip["claim_gate"].values())
    for r in roundtrip["physical_controls"]:
        assert type(r["hidden_shift_calibration"]) is str
        assert r["small_table_replaces_known_Shor_only_for_calibration"]
        assert r["hidden_normal_not_given_to_decoder"]
        assert sorted(r["known_log_calibration_permutation"]) == list(range(r["base_prime"]**r["extension_degree"]))


@pytest.mark.parametrize("callback", [lambda: rotation_success(True, 1), lambda: rotation_success(3, -1),
    lambda: rotation_success(3, 129), lambda: access_ledger(6, 3), lambda: access_ledger(2, 1),
    lambda: physical_control(3, 3, 13), lambda: physical_control(2, 9, 1),
    lambda: coherent_error_budget(0, Fraction(1, 100)), lambda: coherent_error_budget(1, .01)])
def test_invalid_or_out_of_scope_inputs_are_rejected(callback):
    with pytest.raises(ValueError):
        callback()
