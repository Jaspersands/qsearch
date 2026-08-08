import math

from representation_obstruction import integer_partitions
from self_dual_wreath_augmented_h0_dimension_obstruction import (
    augmented_h0_scaling_record,
    audit_pair_budget_expectation,
    information_threshold_copy_count,
    run_augmented_h0_dimension_obstruction,
    two_adic_factorial_valuation,
)


def test_two_adic_valuation_forces_a_minimal_binary_gap() -> None:
    for n in range(3, 51):
        order = math.factorial(n)
        copies = information_threshold_copy_count(n)
        difference = (1 << copies) - order
        valuation = two_adic_factorial_valuation(n)

        assert difference > 0
        assert difference % (1 << valuation) == 0
        assert difference >= 1 << valuation


def test_total_pair_budget_expectation_matches_direct_enumeration() -> None:
    controls = [
        audit_pair_budget_expectation(3, 2, target)
        for target in integer_partitions(3)
    ]

    assert all(control.exact_formula_match for control in controls)
    assert len(
        {
            control.formula_expected_total_pair_rank_relative_to_carrier
            for control in controls
        }
    ) == 2


def test_minimal_copy_h0_lower_bound_is_positive() -> None:
    record = augmented_h0_scaling_record(48, 0)

    assert record.binary_rounding_gap_ratio > 0
    assert (
        record.binary_rounding_gap_ratio
        >= record.two_adic_gap_lower_bound
    )
    assert record.guaranteed_h0_dimension_relative_to_carrier > 0
    assert record.pair_budget_to_rounding_gap_ratio < 0.01


def test_one_extra_copy_makes_h0_obstruction_macroscopic() -> None:
    record = augmented_h0_scaling_record(48, 1)

    assert record.orientation_oversampling_ratio >= 2
    assert record.guaranteed_h0_dimension_relative_to_carrier >= 0.5
    assert record.h0_lower_bound_is_macroscopic
    assert record.expected_total_pair_budget_relative_upper_bound < 1e-50


def test_report_falsifies_pair_cech_but_not_hierarchical_resolution() -> None:
    report = run_augmented_h0_dimension_obstruction()

    assert report.headline_metrics["expectation_control_failure_count"] == 0
    assert report.claim_gate[
        "minimal_copy_augmented_h0_nonzero_with_high_probability"
    ]
    assert report.claim_gate[
        "one_extra_copy_augmented_h0_macroscopic_with_high_probability"
    ]
    assert not report.claim_gate[
        "pair_common_relations_asymptotically_exhaust_leaf_synthesis_kernel"
    ]
    assert not report.claim_gate[
        "direct_common_core_cech_is_complete_polar_sampler"
    ]
    assert not report.claim_gate[
        "hierarchical_span_level_dependency_resolution_ruled_out"
    ]
    assert report.claim_gate[
        "hierarchical_span_level_dependency_resolver_proved"
    ]
    assert not report.claim_gate[
        "hierarchical_span_level_dependency_resolver_coherent"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
