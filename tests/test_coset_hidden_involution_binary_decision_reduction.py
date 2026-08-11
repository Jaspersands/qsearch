import math

import numpy as np
import pytest

from coset_hidden_involution_binary_decision_reduction import (
    audit_dense_binary_control,
    build_hidden_involution_binary_decision_report,
    conjugation_symmetrize_binary_effect,
    dense_binary_states,
    dense_hidden_coset_state,
    exact_class_mixture_chi_square,
    fixed_point_free_decision_scaling_record,
    involution_conjugacy_class,
    involution_class_size,
    minimum_copies_for_bayes_advantage,
    one_copy_label_helstrom_trace_distance,
    product_weak_fourier_trace_distance,
    two_copy_target_label_helstrom_trace_distance,
    write_hidden_involution_binary_decision_report,
)


def test_exact_class_size_chi_square_and_copy_threshold():
    assert involution_class_size(6, 3) == 15
    assert involution_class_size(8, 4) == 105
    assert exact_class_mixture_chi_square(15, 3) == pytest.approx(7 / 15)
    lower = minimum_copies_for_bayes_advantage(105, 0.1)
    assert lower == math.ceil(math.log2(1 + 16 * 0.1**2 * 105))
    with pytest.raises(ValueError, match="cycle type"):
        involution_class_size(4, 0)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (3, 1, 3), (4, 2, 1)),
)
def test_dense_controls_verify_exact_chi_square_identity(
    n, transpositions, copies
):
    row = audit_dense_binary_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.chi_square_identity_residual < 1e-9
    assert (
        row.helstrom_trace_distance
        <= row.chi_square_trace_distance_upper_bound + 1e-10
    )
    assert row.average_conjugation_invariance_residual < 1e-9
    assert row.helstrom_conjugation_invariance_residual < 1e-8


def test_one_copy_weak_fourier_labels_are_exactly_helstrom_optimal():
    for n, transpositions in ((3, 1), (4, 2)):
        dense = audit_dense_binary_control(n, transpositions, 1)
        exact = float(
            one_copy_label_helstrom_trace_distance(n, transpositions)
        )
        assert dense.helstrom_trace_distance == pytest.approx(exact)
        assert dense.product_weak_fourier_trace_distance == pytest.approx(exact)


def test_effect_symmetrization_preserves_average_test_and_equalizes_conjugates():
    null, alternative = dense_binary_states(3, 1, 1)
    diagonal = np.linspace(0.05, 0.95, 6)
    effect = np.diag(diagonal)
    symmetrized = conjugation_symmetrize_binary_effect(3, 1, effect)

    assert np.trace(symmetrized @ null).real == pytest.approx(
        np.trace(effect @ null).real
    )
    assert np.trace(symmetrized @ alternative).real == pytest.approx(
        np.trace(effect @ alternative).real
    )
    acceptances = [
        np.trace(symmetrized @ dense_hidden_coset_state(3, hidden, 1)).real
        for hidden in involution_conjugacy_class(3, 1)
    ]
    assert max(acceptances) - min(acceptances) < 1e-12


def test_two_copy_target_label_is_optimal_and_beats_product_labels():
    row = audit_dense_binary_control(3, 1, 2)
    target = float(two_copy_target_label_helstrom_trace_distance(3, 1))
    product = float(product_weak_fourier_trace_distance(3, 1, 2))
    assert row.helstrom_trace_distance == pytest.approx(target)
    assert target == pytest.approx(5 / 12)
    assert product == pytest.approx(11 / 36)
    assert target > product
    assert row.entangled_target_gain_over_product_labels == pytest.approx(1 / 9)


def test_fixed_point_free_scaling_blocks_constant_copy_but_not_polynomial_copies():
    small = fixed_point_free_decision_scaling_record(8)
    large = fixed_point_free_decision_scaling_record(128)
    assert small.matching_count == 105
    assert large.log2_matching_count > small.log2_matching_count
    assert large.information_theoretic_copy_lower_bound > 1
    assert not large.constant_copy_signal_can_remain_constant
    assert not large.polynomial_measurement_compiler_known
    assert 0.8 < large.copy_lower_bound_over_log2_class_size < 1.1


def test_report_preserves_threshold_compiler_and_gi_claim_gates(tmp_path):
    report = build_hidden_involution_binary_decision_report(
        finite_specs=((3, 1, 1), (3, 1, 2), (4, 2, 1)),
        scaling_n_values=(8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_chi_square_proved
    assert report.theorem.one_copy_weak_fourier_helstrom_optimal
    assert report.theorem.two_copy_target_label_helstrom_optimal
    assert not report.theorem.threshold_trace_distance_lower_bound_proved
    assert not report.theorem.scalable_block_sign_compiler_constructed
    assert not report.claim_gate["graph_isomorphism_algorithm_constructed"]
    assert not report.claim_gate["sample_complexity_result_new_to_literature"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hidden_involution_binary_decision_report(
        tmp_path / "binary.json",
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(8, 16),
    )
    assert payload["status"] == (
        "binary-decision-copy-threshold-and-two-copy-normal-form-proved"
    )
