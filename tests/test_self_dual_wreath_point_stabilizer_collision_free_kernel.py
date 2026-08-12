from __future__ import annotations

from fractions import Fraction

import pytest

from self_dual_wreath_point_stabilizer_collision_free_kernel import (
    audit_collision_free_point_signal,
    collision_free_annealed_overlap_kernel,
    collision_free_point_scaling_record,
    compressed_injective_plancherel_transform,
    compressed_repeated_point_factor,
    point_overlap_components,
    run_collision_free_point_kernel,
    validate_point_overlap_components,
)
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_global_distinct_joint_kernel import (
    injective_plancherel_transform,
    structured_global_distinct_joint_factor,
)
from self_dual_wreath_joint_character_correlation_decoder import _permutations


def test_four_term_point_overlap_factorization_is_exact() -> None:
    control = validate_point_overlap_components(3)
    assert control.checked_local_factor_count == 6**3 * 3**2
    assert control.maximum_absolute_residual == 0
    assert control.exact_four_term_rank_one_expansion_verified


def test_count_state_injective_dp_preserves_labeled_slot_multiplicity() -> None:
    weights = plancherel_weights(4)
    features = (
        tuple(Fraction(index + 1, 3) for index in range(len(weights))),
        tuple(Fraction((-1) ** index, 2) for index in range(len(weights))),
        tuple(Fraction(index - 2, 5) for index in range(len(weights))),
    )
    multiplicities = ((features[0], 2), (features[1], 1), (features[2], 1))
    expanded = (features[0], features[0], features[1], features[2])
    assert compressed_injective_plancherel_transform(
        weights,
        multiplicities,
    ) == injective_plancherel_transform(weights, expanded)


def test_k_plus_one_profile_compression_matches_naive_four_power_expansion() -> None:
    permutations = _permutations(4)
    for source, target, hidden in (
        (permutations[0], permutations[3], permutations[7]),
        (permutations[5], permutations[11], permutations[19]),
    ):
        components = point_overlap_components(4, source, target, hidden)
        naive = structured_global_distinct_joint_factor(4, (components,) * 2)
        compressed = compressed_repeated_point_factor(
            4,
            2,
            source,
            target,
            hidden,
        )
        assert compressed == naive


def test_collision_free_point_kernel_rejects_impossible_source_count() -> None:
    with pytest.raises(ValueError, match="global distinctness is impossible"):
        collision_free_annealed_overlap_kernel(4, 3)


def test_s4_collision_free_kernel_matches_all_dense_source_assignments() -> None:
    control = audit_collision_free_point_signal(4, 2, dense_validation=True)
    assert control.exact_collision_free_point_kernel_verified
    assert control.ordered_distinct_source_assignment_count == 120
    assert control.exact_conditioned_centered_signal == str(Fraction(7, 3888))
    assert control.injective_to_direct_dense_residual < 1e-12
    assert control.standard_character_coefficient_residual == "0"
    assert control.conditioned_normalized_centered_signal == pytest.approx(
        14 / 81
    )
    assert control.conditioned_to_unrestricted_signal_ratio > 2.6
    assert not control.information_threshold_reached


def test_threshold_scaling_keeps_asymptotic_signal_gate_open() -> None:
    impossible = collision_free_point_scaling_record(8)
    possible = collision_free_point_scaling_record(12)
    assert not impossible.enough_distinct_partitions_exist
    assert possible.enough_distinct_partitions_exist
    assert not possible.exact_threshold_kernel_computationally_compiled
    assert not possible.asymptotic_conditioned_point_signal_bound_proved
    assert possible.exponential_source_component_expansion_removed
    assert possible.source_contraction_polynomial_in_partition_and_copy_count
    assert not possible.factorial_group_sum_compressed
    assert possible.compressed_profile_count == (
        possible.information_threshold_copy_count + 1
    )
    assert possible.rank_one_expansion_term_count_log2 == 2 * (
        possible.information_threshold_copy_count
    )


def test_report_closes_source_formula_without_claiming_decoder() -> None:
    report = run_collision_free_point_kernel()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "point_overlap_four_term_rank_one_factorization_proved"
    ]
    assert report.claim_gate["collision_free_point_overlap_kernel_proved"]
    assert report.claim_gate["collision_free_standard_signal_coefficient_proved"]
    assert report.claim_gate["exponential_source_component_expansion_removed"]
    assert not report.claim_gate["factorial_group_sum_compressed"]
    assert not report.claim_gate["unrestricted_signal_transfer_sufficient"]
    assert not report.claim_gate[
        "threshold_collision_free_point_signal_bound_proved"
    ]
    assert not report.claim_gate[
        "efficient_collision_free_point_measurement_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
