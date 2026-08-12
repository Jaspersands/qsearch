import numpy as np
import pytest

from self_dual_wreath_component_dependency_ridge_physical_hamming import (
    _random_leaf_isometry_synthesis,
    audit_dependency_ridge_physical_hamming,
    dependency_ridge_physical_hamming_theorem,
    physical_leaf_ridge_normal_form,
    run_component_dependency_ridge_physical_hamming,
    typical_physical_ridge_pair_target,
)


def test_physical_leaf_words_and_leaf_marked_words_are_exact() -> None:
    synthesis, common = _random_leaf_isometry_synthesis(
        10,
        4,
        3,
        4,
        seed=201,
    )
    row = audit_dependency_ridge_physical_hamming(
        "WORDS",
        synthesis,
        common,
        4,
        1e-2,
    )
    assert row.exact_physical_leaf_word_reduction_verified
    assert row.maximum_leaf_isometry_residual < 1e-9
    assert row.maximum_coefficient_to_physical_leaf_word_residual < 1e-8
    assert row.maximum_physical_to_leaf_marked_word_residual < 1e-8
    assert row.maximum_pair_commutator_residual < 1e-8


def test_walsh_parity_curl_equals_physical_leaf_pair_sum() -> None:
    synthesis, common = _random_leaf_isometry_synthesis(
        12,
        8,
        2,
        4,
        seed=203,
    )
    row = audit_dependency_ridge_physical_hamming(
        "CURL",
        synthesis,
        common,
        8,
        3e-3,
    )
    assert row.exact_physical_leaf_word_reduction_verified
    assert row.coefficient_normalized_parity_curl == pytest.approx(
        row.physical_leaf_normalized_parity_curl,
        abs=1e-8,
    )
    assert row.physical_leaf_pair_curl_positive


def test_leaf_kernel_is_positive_and_normal_form_shapes_match() -> None:
    synthesis, common = _random_leaf_isometry_synthesis(
        9,
        4,
        3,
        3,
        seed=207,
    )
    ridge, kernel, blocks, frames, effects = physical_leaf_ridge_normal_form(
        synthesis,
        common,
        4,
        1e-3,
    )
    assert ridge.shape == (12, 12)
    assert kernel.shape == (9, 9)
    assert np.linalg.eigvalsh(kernel)[0] > -1e-9
    assert len(blocks) == len(frames) == len(effects) == 4


def test_typical_hamming_target_has_m_strata_and_correct_implication() -> None:
    row = typical_physical_ridge_pair_target(296, 1 / 64**2)
    assert row.typical_hamming_mass_lower_bound > 0.99
    assert row.hamming_stratum_count == 296
    assert row.parity_mask_pair_stratum_count == pytest.approx(
        297 * 298 * 299 / 6
    )
    assert row.implied_bounded_ridge_curl_lower_bound == pytest.approx(
        row.typical_hamming_mass_lower_bound / (2 * 64**2)
    )
    assert row.physical_hamming_reduction_is_stronger_than_mask_stratification
    assert not row.natural_rescaled_pair_gap_proved


def test_invalid_coordinate_partition_is_rejected() -> None:
    synthesis, common = _random_leaf_isometry_synthesis(
        8,
        4,
        2,
        2,
        seed=211,
    )
    with pytest.raises(ValueError, match="power of two"):
        physical_leaf_ridge_normal_form(synthesis, common, 3, 1e-2)


def test_report_keeps_natural_pair_tail_M4_and_speedup_open() -> None:
    report = run_component_dependency_ridge_physical_hamming()
    assert report.headline_metrics[
        "exact_physical_leaf_word_reduction_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "walsh_mask_to_leaf_pair_reduction_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["bounded_ridge_curl_is_physical_leaf_pair_sum"]
    assert report.claim_gate["annealed_target_has_only_m_hamming_strata"]
    assert not report.claim_gate[
        "natural_typical_rescaled_ridge_pair_gap_positive"
    ]
    assert not report.claim_gate["natural_support_ridge_tail_small"]
    assert not report.claim_gate["natural_exact_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_states_exact_typical_pair_target_and_scope() -> None:
    theorem = dependency_ridge_physical_hamming_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_equal_block_synthesis
    assert theorem.source_relabeling_invariant_event_required_for_hamming_reduction
    assert "Bin(m,1/2)" in theorem.annealed_hamming_identity
    assert "q^2" in theorem.exact_typical_pair_target
